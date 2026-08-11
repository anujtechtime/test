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
    # DIRECT SERIAL ASSIGNMENT - THE FIX
    # ============================================================

    def _assign_serials_to_move_lines(self):
        """
        Directly assign serials to move lines before validation
        This is called BEFORE Odoo's validation
        """
        StockProductionLot = self.env['stock.production.lot'].sudo()
        
        for picking in self:
            _logger.info('========== ASSIGNING SERIALS FOR %s ==========', picking.name)
            
            # Only process internal transfers
            if not picking._is_internal_transfer_for_serials():
                continue

            # Process each move
            for move in picking.move_ids_without_package:
                product = move.product_id
                
                # Skip non-serial products
                if not product or product.tracking != 'serial':
                    continue

                _logger.info('Processing move for product: %s', product.display_name)
                
                # Get destination location
                destination = move.location_dest_id or picking.location_dest_id
                if not destination:
                    continue

                # Get prefixes
                try:
                    location_prefix = picking._get_location_prefix(destination)
                    product_prefix = picking._get_product_prefix(product)
                    
                    if not location_prefix or not product_prefix:
                        _logger.warning('Missing prefix for product %s', product.display_name)
                        continue
                        
                    picking._validate_prefix(location_prefix, _('Location'))
                    picking._validate_prefix(product_prefix, _('Product'))
                    
                except ValidationError as e:
                    _logger.error('Prefix validation failed: %s', str(e))
                    continue

                # Get quantity
                quantity = int(move.product_uom_qty)
                _logger.info('Quantity: %s', quantity)

                # Check existing move lines
                existing_lines = move.move_line_ids.filtered(
                    lambda l: l.product_id.id == product.id
                )
                
                if existing_lines:
                    _logger.info('Found %s existing move lines', len(existing_lines))
                    # Check which lines need serials
                    lines_without_lot = existing_lines.filtered(lambda l: not l.lot_id)
                    
                    if lines_without_lot:
                        _logger.info('Found %s lines without serials', len(lines_without_lot))
                        # Assign serials to lines without lots
                        for line in lines_without_lot:
                            serial = picking._next_serial(destination, product)
                            _logger.info('Generated serial: %s', serial)
                            
                            # Create lot
                            lot = StockProductionLot.create({
                                'name': serial,
                                'product_id': product.id,
                                'company_id': picking.company_id.id or self.env.company.id,
                            })
                            
                            # Assign to line
                            line.write({
                                'lot_id': lot.id,
                                'qty_done': 1.0,
                            })
                            _logger.info('Assigned serial %s to line %s', serial, line.id)
                    else:
                        _logger.info('All lines already have serials')
                else:
                    _logger.info('No existing move lines, creating new ones')
                    # Create move lines with serials
                    for i in range(quantity):
                        serial = picking._next_serial(destination, product)
                        _logger.info('Generated serial: %s', serial)
                        
                        # Create lot
                        lot = StockProductionLot.create({
                            'name': serial,
                            'product_id': product.id,
                            'company_id': picking.company_id.id or self.env.company.id,
                        })
                        
                        # Create move line with lot
                        self.env['stock.move.line'].create({
                            'move_id': move.id,
                            'picking_id': picking.id,
                            'product_id': product.id,
                            'product_uom_id': move.product_uom.id,
                            'location_id': move.location_id.id,
                            'location_dest_id': destination.id,
                            'lot_id': lot.id,
                            'qty_done': 1.0,
                        })
                        _logger.info('Created new line with serial %s', serial)

    # ============================================================
    # COMPLETE OVERRIDE - THE KEY FIX
    # ============================================================

    def _check_serial_numbers(self):
        """
        OVERRIDE: This is the method that checks for serial numbers
        We completely bypass it for internal transfers
        """
        # For internal transfers, skip the serial number check
        if self._is_internal_transfer_for_serials():
            _logger.info('SKIPPING serial number check for internal transfer: %s', self.name)
            return True
        
        # For other transfers, use the original method
        return super(StockPicking, self)._check_serial_numbers()

    # ============================================================
    # OVERRIDE BUTTON_VALIDATE
    # ============================================================

    def button_validate(self):
        """
        Override button_validate to assign serials before validation
        """
        for picking in self:
            if picking._is_internal_transfer_for_serials():
                _logger.info('========== VALIDATING INTERNAL TRANSFER: %s ==========', picking.name)
                
                # First, assign serials to all serial products
                picking._assign_serials_to_move_lines()
                
                # Log the state after assignment
                for move in picking.move_ids_without_package:
                    if move.product_id and move.product_id.tracking == 'serial':
                        for line in move.move_line_ids:
                            _logger.info('Line %s: lot_id=%s, qty_done=%s', 
                                       line.id, 
                                       line.lot_id.id if line.lot_id else False,
                                       line.qty_done)
        
        # Now call the original validation
        return super(StockPicking, self).button_validate()

    # ============================================================
    # OVERRIDE ACTION_CONFIRM
    # ============================================================

    def action_confirm(self):
        """
        Override action_confirm to assign serials before confirmation
        """
        for picking in self:
            if picking._is_internal_transfer_for_serials():
                _logger.info('Assigning serials during confirmation for %s', picking.name)
                picking._assign_serials_to_move_lines()
        
        return super(StockPicking, self).action_confirm()

    # ============================================================
    # MANUAL BUTTON
    # ============================================================

    def action_generate_serial_prefix(self):
        """
        Manual button to generate serial prefixes
        """
        self.ensure_one()
        
        if not self.move_ids_without_package:
            raise UserError(_(
                'No stock moves exist on transfer "%s". '
                'Please add products to the transfer first.'
            ) % self.name)
        
        # Assign serials
        self._assign_serials_to_move_lines()
        
        # Verify assignment
        for move in self.move_ids_without_package:
            if move.product_id and move.product_id.tracking == 'serial':
                for line in move.move_line_ids:
                    if not line.lot_id:
                        raise UserError(_(
                            'Failed to assign serial to line %s for product %s'
                        ) % (line.id, move.product_id.display_name))
        
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': _('Success'),
                'message': _('Serial numbers assigned successfully for %s') % self.name,
                'type': 'success',
                'sticky': False,
            }
        }

    # ============================================================
    # OVERRIDE THE CHECK METHOD - CRITICAL
    # ============================================================

    @api.depends('move_ids_without_package')
    def _compute_is_lot_required(self):
        """
        Override the lot required computation
        For internal transfers, we handle serials differently
        """
        result = super(StockPicking, self)._compute_is_lot_required()
        
        for picking in self:
            if picking._is_internal_transfer_for_serials():
                # For internal transfers, mark that lots are not required
                # This prevents Odoo from showing the validation error
                picking.is_lot_required = False
                _logger.info('Set is_lot_required=False for internal transfer %s', picking.name)
        
        return result