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
    )

    def _is_internal_transfer_for_serials(self):
        self.ensure_one()
        return self.picking_type_id.code == 'internal'

    def _get_location_prefix(self, location):
        if not location:
            return ''
        prefix = location.get_serial_prefix()
        if not prefix:
            return ''
        return prefix.strip()

    def _get_product_prefix(self, product):
        if not product:
            return ''
        prefix = product.product_tmpl_id.prefix_code or ''
        return prefix.strip()

    def _validate_prefix(self, prefix, label):
        if not prefix:
            raise ValidationError(_('%s prefix code is required.') % label)
        if not re.match(r'^[A-Za-z0-9_-]+$', prefix):
            raise ValidationError(_('%s prefix "%s" contains unsupported characters.') % (label, prefix))

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

    def _generate_serials_for_picking(self):
        """
        Generate serials and assign them directly
        """
        processed = False
        StockProductionLot = self.env['stock.production.lot'].sudo()

        for picking in self:
            if not picking._is_internal_transfer_for_serials():
                continue

            for move in picking.move_ids_without_package:
                product = move.product_id
                if not product or product.tracking != 'serial':
                    continue

                destination = move.location_dest_id or picking.location_dest_id
                if not destination:
                    continue

                location_prefix = picking._get_location_prefix(destination)
                product_prefix = picking._get_product_prefix(product)
                
                if not location_prefix or not product_prefix:
                    _logger.warning('Missing prefix for product %s', product.display_name)
                    continue

                quantity = int(move.product_uom_qty)
                
                # If no move lines, create them with lots
                if not move.move_line_ids:
                    for i in range(quantity):
                        serial = picking._next_serial(destination, product)
                        
                        lot = StockProductionLot.create({
                            'name': serial,
                            'product_id': product.id,
                            'company_id': picking.company_id.id or self.env.company.id,
                        })
                        
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
                        processed = True
                else:
                    # Existing move lines - assign lots to them
                    for line in move.move_line_ids:
                        if not line.lot_id:
                            serial = picking._next_serial(destination, product)
                            lot = StockProductionLot.create({
                                'name': serial,
                                'product_id': product.id,
                                'company_id': picking.company_id.id or self.env.company.id,
                            })
                            line.write({
                                'lot_id': lot.id,
                                'qty_done': 1.0,
                            })
                            processed = True

        if processed:
            self.write({'serial_prefix_generated': True})

        return processed

    # ============================================================
    # SIMPLE APPROACH - OVERRIDE VALIDATION ONLY
    # ============================================================

    def button_validate(self):
        """
        Generate serials before validation
        """
        # Generate serials for all internal transfers
        for picking in self:
            if picking._is_internal_transfer_for_serials():
                picking._generate_serials_for_picking()
        
        # Now proceed with normal validation
        return super(StockPicking, self).button_validate()

    def action_generate_serial_prefix(self):
        self.ensure_one()
        return self._generate_serials_for_picking()