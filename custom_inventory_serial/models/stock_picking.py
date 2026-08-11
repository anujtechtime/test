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
        if not location:
            return ''
        prefix = location.get_serial_prefix()
        if not prefix:
            return ''
        return prefix.strip()

    # ============================================================
    # GET PRODUCT PREFIX
    # ============================================================

    def _get_product_prefix(self, product):
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
                _('%s prefix code is required before generating a serial number.') % label
            )
        if not re.match(r'^[A-Za-z0-9_-]+$', prefix):
            raise ValidationError(
                _('%s prefix "%s" contains unsupported characters. Use only letters, numbers, underscore or hyphen.') % (
                    label, prefix
                )
            )

    # ============================================================
    # GET / CREATE SEQUENCE
    # ============================================================

    @api.model
    def _get_serial_sequence(self, prefix):
        Sequence = self.env['ir.sequence'].sudo()
        code = 'custom_inventory_serial.%s' % prefix
        
        sequence = Sequence.search([('code', '=', code)], limit=1)
        
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
        location_prefix = self._get_location_prefix(location)
        product_prefix = self._get_product_prefix(product)
        
        self._validate_prefix(location_prefix, _('Location'))
        self._validate_prefix(product_prefix, _('Product'))
        
        full_prefix = '%s%s' % (location_prefix, product_prefix)
        sequence = self._get_serial_sequence(full_prefix)
        serial = sequence.next_by_id()
        
        return serial

    # ============================================================
    # GENERATE SERIALS FOR MOVES - THIS RUNS BEFORE CONFIRMATION
    # ============================================================

    def _generate_serials_for_moves(self):
        """
        Generate serial numbers for moves BEFORE confirmation
        This is called during button_validate
        """
        StockProductionLot = self.env['stock.production.lot'].sudo()
        processed = False

        for picking in self:
            _logger.info('Generating serials for picking: %s', picking.name)
            
            # Check if internal transfer
            if not picking._is_internal_transfer_for_serials():
                continue

            # Check if there are moves
            if not picking.move_ids_without_package:
                _logger.warning('No moves in picking %s', picking.name)
                continue

            # Check if moves have serial products
            for move in picking.move_ids_without_package:
                product = move.product_id
                
                if not product or product.tracking != 'serial':
                    continue

                destination = move.location_dest_id or picking.location_dest_id
                
                if not destination:
                    raise ValidationError(
                        _('Destination location is missing for product "%s".') % product.display_name
                    )

                # Get prefixes
                try:
                    location_prefix = picking._get_location_prefix(destination)
                    product_prefix = picking._get_product_prefix(product)
                    
                    picking._validate_prefix(location_prefix, _('Location'))
                    picking._validate_prefix(product_prefix, _('Product'))
                except ValidationError as e:
                    # If prefixes are missing, we can't generate serials
                    raise UserError(_(
                        'Cannot generate serial numbers for product "%s". '
                        'Please ensure both location and product prefixes are configured.\n'
                        'Error: %s'
                    ) % (product.display_name, str(e)))

                quantity = int(move.product_uom_qty)
                _logger.info('Generating %s serials for product %s', quantity, product.display_name)
                
                # Create move lines with serial numbers BEFORE confirmation
                for i in range(quantity):
                    serial = picking._next_serial(destination, product)
                    _logger.info('Generated serial: %s', serial)
                    
                    # Check if serial already exists
                    existing_lot = StockProductionLot.search([
                        ('name', '=', serial),
                        ('product_id', '=', product.id)
                    ], limit=1)
                    
                    if existing_lot:
                        # If serial exists, try to generate a new one with a suffix
                        # Or simply skip this one and continue
                        _logger.warning('Serial %s already exists, generating alternative', serial)
                        continue
                    
                    # Create the lot
                    lot = StockProductionLot.create({
                        'name': serial,
                        'product_id': product.id,
                        'company_id': picking.company_id.id or self.env.company.id,
                    })
                    
                    # Create move line with the lot assigned
                    move_line_vals = {
                        'move_id': move.id,
                        'picking_id': picking.id,
                        'product_id': product.id,
                        'product_uom_id': move.product_uom.id,
                        'location_id': move.location_id.id,
                        'location_dest_id': destination.id,
                        'lot_id': lot.id,
                        'qty_done': 1.0,
                    }
                    
                    self.env['stock.move.line'].create(move_line_vals)
                    processed = True

        if processed:
            self.write({'serial_prefix_generated': True})

        return processed

    # ============================================================
    # OVERRIDE BUTTON_VALIDATE - GENERATE SERIALS FIRST
    # ============================================================

    def button_validate(self):
        """
        Override button_validate:
        1. First generate serial numbers for all serial-tracked products
        2. Then call the original validation
        """
        for picking in self:
            if picking._is_internal_transfer_for_serials():
                # Generate serials BEFORE validation
                _logger.info('Generating serials for %s before validation', picking.name)
                picking._generate_serials_for_moves()
        
        # Now call the original validation
        return super(StockPicking, self).button_validate()

    # ============================================================
    # MANUAL SERIAL GENERATION BUTTON
    # ============================================================

    def action_generate_serial_prefix(self):
        """
        Manual button to generate serial prefixes
        Can be called before confirmation
        """
        self.ensure_one()
        
        if not self.move_ids_without_package:
            raise UserError(_(
                'No stock moves exist on transfer "%s". '
                'Please add products to the transfer first.'
            ) % self.name)
        
        # Check if there are serial products
        has_serial = False
        for move in self.move_ids_without_package:
            if move.product_id and move.product_id.tracking == 'serial':
                has_serial = True
                break
        
        if not has_serial:
            raise UserError(_(
                'Transfer "%s" does not contain any serial-tracked products.'
            ) % self.name)
        
        result = self._generate_serials_for_moves()
        
        if result:
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': _('Success'),
                    'message': _('Serial numbers generated successfully for %s') % self.name,
                    'type': 'success',
                    'sticky': False,
                }
            }
        else:
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': _('Warning'),
                    'message': _('No serial numbers were generated. Please check the products in the transfer.'),
                    'type': 'warning',
                    'sticky': False,
                }
            }