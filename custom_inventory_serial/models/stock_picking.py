# -*- coding: utf-8 -*-

import re

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError
import logging

_logger = logging.getLogger(__name__)


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    serial_prefix_generated = fields.Boolean(
        string='Serial Prefix Generated',
        copy=False,
        readonly=True,
        help='Technical flag indicating that serial numbers '
             'have been generated for this transfer.'
    )

    # ============================================================
    # CHECK INTERNAL TRANSFER
    # ============================================================

    def _is_internal_transfer_for_serials(self):
        self.ensure_one()
        return self.picking_type_id.code == 'internal'

    # ============================================================
    # GET LOCATION PREFIX
    # ============================================================

    def _get_location_prefix(self, location):
        """
        Get the serial prefix from destination location.

        Example:
            Building = N
            Floor = F
            Hall = 5

            Location Prefix = NF5
        """

        if not location:
            return ''

        # Your custom location module has get_serial_prefix()
        prefix = location.get_serial_prefix()

        if not prefix:
            return ''

        return prefix.strip()

    # ============================================================
    # GET PRODUCT PREFIX
    # ============================================================

    def _get_product_prefix(self, product):
        """
        Get product prefix.

        Example:
            Product Prefix = x
        """

        if not product:
            return ''

        prefix = product.product_tmpl_id.prefix_code or ''

        return prefix.strip()

    # ============================================================
    # VALIDATE PREFIX
    # ============================================================

    def _validate_prefix(self, prefix, label):

        if not prefix:
            raise ValidationError(
                _(
                    '%s prefix code is required before '
                    'generating a serial number.'
                ) % label
            )

        if not re.match(
            r'^[A-Za-z0-9_-]+$',
            prefix
        ):
            raise ValidationError(
                _(
                    '%s prefix "%s" contains unsupported '
                    'characters. Use only letters, numbers, '
                    'underscore or hyphen.'
                ) % (
                    label,
                    prefix
                )
            )

    # ============================================================
    # GET / CREATE SEQUENCE
    # ============================================================

    @api.model
    def _get_serial_sequence(self, prefix):

        Sequence = self.env[
            'ir.sequence'
        ].sudo()

        code = (
            'custom_inventory_serial.%s'
            % prefix
        )

        sequence = Sequence.search(
            [
                ('code', '=', code)
            ],
            limit=1
        )

        if not sequence:

            sequence = Sequence.create({
                'name': 'Serial Sequence %s' % prefix,
                'code': code,
                'implementation': 'no_gap',
                'active': True,
                'prefix': prefix,
                'padding': 4,
                'number_next_actual': 1,
            })

        return sequence

    # ============================================================
    # GENERATE NEXT SERIAL
    # ============================================================

    @api.model
    def _next_serial(self, location, product):

        location_prefix = self._get_location_prefix(
            location
        )

        product_prefix = self._get_product_prefix(
            product
        )

        self._validate_prefix(
            location_prefix,
            _('Location')
        )

        self._validate_prefix(
            product_prefix,
            _('Product')
        )

        full_prefix = (
            '%s%s'
            % (
                location_prefix,
                product_prefix
            )
        )

        sequence = self._get_serial_sequence(
            full_prefix
        )

        serial = sequence.next_by_id()

        return serial

    # ============================================================
    # MAIN SERIAL GENERATION METHOD
    # ============================================================

    def _generate_serials_for_picking(
        self,
        raise_on_missing_prefix=True
    ):
        """
        Generate serial numbers for internal transfers.
        """

        StockProductionLot = self.env['stock.production.lot'].sudo()
        processed = False

        _logger.info('========== SERIAL GENERATION START ==========')

        for picking in self:
            _logger.info('Processing Picking: %s | ID: %s', picking.name, picking.id)
            _logger.info('Picking State: %s', picking.state)
            _logger.info('Picking Type: %s', picking.picking_type_id.name)
            _logger.info('Picking Type Code: %s', picking.picking_type_id.code)

            # ----------------------------------------------------
            # INTERNAL TRANSFER CHECK
            # ----------------------------------------------------

            if not picking._is_internal_transfer_for_serials():
                _logger.info('Skipping %s because it is not an internal transfer.', picking.name)
                continue

            # ----------------------------------------------------
            # GET MOVES
            # ----------------------------------------------------

            moves = picking.move_ids_without_package

            if not moves:
                moves = self.env['stock.move'].search([('picking_id', '=', picking.id)])

            if not moves:
                _logger.warning('NO STOCK MOVES FOUND FOR PICKING %s', picking.name)
                continue

            # ====================================================
            # PROCESS EACH MOVE
            # ====================================================

            for move in moves:
                product = move.product_id

                if not product:
                    _logger.warning('Skipping move %s because product is missing.', move.id)
                    continue

                if product.tracking != 'serial':
                    _logger.warning('Skipping product %s because tracking is "%s", not "serial".', 
                                  product.display_name, product.tracking)
                    continue

                destination = move.location_dest_id or picking.location_dest_id

                if not destination:
                    raise ValidationError(_('Destination location is missing for product "%s".') % product.display_name)

                # ------------------------------------------------
                # GET PREFIXES
                # ------------------------------------------------

                location_prefix = picking._get_location_prefix(destination)
                product_prefix = picking._get_product_prefix(product)

                picking._validate_prefix(location_prefix, _('Location'))
                picking._validate_prefix(product_prefix, _('Product'))

                # ------------------------------------------------
                # GET OR CREATE MOVE LINES
                # ------------------------------------------------

                lines = move.move_line_ids

                if not lines:
                    quantity = move.product_uom_qty

                    if quantity <= 0:
                        _logger.warning('Skipping move %s because quantity is zero.', move.id)
                        continue

                    if int(quantity) != quantity:
                        raise ValidationError(
                            _('Serial-tracked product "%s" has a non-integer quantity (%s).') % (
                                product.display_name, quantity
                            )
                        )

                    vals = []
                    for index in range(int(quantity)):
                        vals.append({
                            'picking_id': picking.id,
                            'move_id': move.id,
                            'product_id': product.id,
                            'product_uom_id': move.product_uom.id,
                            'location_id': move.location_id.id,
                            'location_dest_id': destination.id,
                            'qty_done': 1.0,
                        })

                    lines = self.env['stock.move.line'].create(vals)

                # =================================================
                # PROCESS EACH MOVE LINE
                # =================================================

                for line in lines:
                    _logger.info('Processing Move Line ID: %s', line.id)
                    _logger.info('Qty Done: %s', line.qty_done)
                    _logger.info('Lot ID: %s', line.lot_id.id if line.lot_id else False)

                    # Skip if serial already exists
                    if line.lot_id:
                        _logger.info('Skipping line %s because serial already exists.', line.id)
                        continue

                    # ----------------------------------------------------
                    # GENERATE SERIAL
                    # ----------------------------------------------------

                    try:
                        serial = picking._next_serial(destination, product)
                        _logger.info('Generated Serial: %s', serial)
                    except ValidationError:
                        _logger.exception('Prefix validation failed for move line %s.', line.id)
                        if raise_on_missing_prefix:
                            raise
                        continue

                    # ----------------------------------------------------
                    # CHECK FOR DUPLICATES
                    # ----------------------------------------------------

                    existing = StockProductionLot.search([
                        ('name', '=', serial),
                        ('product_id', '=', product.id),
                    ], limit=1)

                    if existing:
                        raise ValidationError(
                            _('Generated serial "%s" already exists for product "%s".') % (
                                serial, product.display_name
                            )
                        )

                    # ----------------------------------------------------
                    # CREATE AND ASSIGN SERIAL
                    # ----------------------------------------------------

                    try:
                        # Create the lot/serial record
                        lot = StockProductionLot.create({
                            'name': serial,
                            'product_id': product.id,
                            'company_id': picking.company_id.id or self.env.company.id,
                        })

                        _logger.info('Created Lot: %s (ID: %s)', lot.name, lot.id)

                        # CRITICAL FIX: Update the move line with the lot
                        # Make sure we're updating the right fields
                        line.write({
                            'lot_id': lot.id,
                            'qty_done': 1.0,
                        })

                        # Force flush to database
                        line.flush()

                        _logger.info('Assigned lot %s to line %s', lot.name, line.id)
                        
                        # Verify the assignment
                        line.refresh()
                        _logger.info('VERIFICATION - Line %s now has lot_id: %s', line.id, line.lot_id.id if line.lot_id else False)

                        processed = True

                    except Exception as e:
                        _logger.error('Failed to create/assign serial %s: %s', serial, str(e))
                        raise ValidationError(_('Failed to assign serial number: %s') % str(e))

            # ----------------------------------------------------
            # FORCE UPDATE OF MOVE LINES IN THE PICKING
            # ----------------------------------------------------
            
            # Refresh the picking to ensure all changes are visible
            picking.refresh()
            
            # Log the final state
            for move in moves:
                for line in move.move_line_ids:
                    _logger.info('FINAL STATE - Line %s: lot_id=%s, lot_name=%s', 
                               line.id, 
                               line.lot_id.id if line.lot_id else False,
                               line.lot_name)

        # ============================================================
        # MARK PICKING AS PROCESSED
        # ============================================================

        if processed:
            self.write({'serial_prefix_generated': True})

        _logger.info('========== SERIAL GENERATION END | PROCESSED=%s ==========', processed)
        return processed

    # ============================================================
    # OVERRIDE VALIDATE - FIXED VERSION
    # ============================================================

    def button_validate(self):
        """
        Override button_validate to generate serials before validation
        """
        # Generate serials before validation
        for picking in self:
            if picking._is_internal_transfer_for_serials():
                try:
                    # Generate serials
                    self._generate_serials_for_picking(raise_on_missing_prefix=True)
                    
                    # Force a refresh to ensure all changes are loaded
                    picking.refresh()
                    
                    # Explicitly check if all serial-tracked products have lots assigned
                    for move in picking.move_ids_without_package:
                        if move.product_id.tracking == 'serial':
                            for line in move.move_line_ids:
                                if not line.lot_id:
                                    _logger.error('Line %s still has no lot_id!', line.id)
                                    # Try to assign a default serial if missing
                                    # You might want to handle this differently
                                    raise ValidationError(
                                        _('Line %s for product %s has no serial number assigned.') % (
                                            line.id, move.product_id.display_name
                                        )
                                    )
                    
                except Exception as e:
                    _logger.error('Error generating serials: %s', str(e))
                    raise UserError(_('Failed to generate serial numbers: %s') % str(e))

        # Call the original button_validate
        return super(StockPicking, self).button_validate()

    # ============================================================
    # BUTTON / SERVER ACTION
    # ============================================================

    def action_generate_serial_prefix(self):
        self.ensure_one()

        _logger.info("========== DEBUG TRANSFER ==========")
        _logger.info("Picking: %s", self.name)
        _logger.info("State: %s", self.state)
        _logger.info("Picking Type: %s", self.picking_type_id.code)
        _logger.info("move_ids_without_package IDs: %s", self.move_ids_without_package.ids)
        _logger.info("move_line_ids IDs: %s", self.move_line_ids.ids)
        _logger.info("===================================")

        result = self._generate_serials_for_picking(raise_on_missing_prefix=True)
        
        # Verify after generation
        _logger.info("========== VERIFICATION ==========")
        for move in self.move_ids_without_package:
            for line in move.move_line_ids:
                _logger.info("Line %s: lot_id=%s, lot_name=%s", 
                           line.id, 
                           line.lot_id.id if line.lot_id else False,
                           line.lot_name)
        _logger.info("===================================")
        
        return result