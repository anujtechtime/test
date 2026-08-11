# -*- coding: utf-8 -*-
import re

from odoo import models, api, fields, _
from odoo.exceptions import UserError, ValidationError
import logging
_logger = logging.getLogger(__name__)


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    serial_prefix_generated = fields.Boolean(
        string='Serial Prefix Generated',
        copy=False,
        readonly=True,
        help='Technical flag indicating that this picking has been processed by '
             'the custom serial generator.',
    )

    
    def _is_internal_transfer_for_serials(self):
        self.ensure_one()
        return self.picking_type_id.code == 'internal'

    
    def _get_location_prefix(self, location):
        if not location:
            return ''
        return location.get_serial_prefix()

    
    def _get_product_prefix(self, product):
        prefix = product.product_tmpl_id.prefix_code or ''
        return prefix.strip()

    
    def _validate_prefix(self, prefix, label):
        if not prefix:
            raise ValidationError(_('%s prefix code is required before generating a serial number.') % label)
        # Keep generated identifiers simple and predictable.
        if not re.match(r'^[A-Za-z0-9_-]+$', prefix):
            raise ValidationError(_('%s prefix "%s" contains unsupported characters. '
                                    'Use only letters, numbers, underscore or hyphen.') % (label, prefix))

    @api.model
    def _get_serial_sequence(self, prefix):
        """Get/create an Odoo sequence for a generated serial prefix.

        A separate sequence is maintained for every complete prefix, e.g.
        NF5x -> NF5x0001, NF5x0002...
        """
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
        return sequence.next_by_id()

    
    def _generate_serials_for_picking(self, raise_on_missing_prefix=True):
        """Generate and assign missing serials to done/reserved move lines.

        For validation-time processing, this method assigns lot_name to move lines
        before the standard stock validation so tracked products can be validated.
        It only creates serials for products with tracking == 'serial'.
        Existing lot_id/lot_name values are never overwritten.
        """
        StockProductionLot = self.env['stock.production.lot'].sudo()
        processed = False

        for picking in self:
            if not picking._is_internal_transfer_for_serials():
                _logger.info("Skipping picking11111111111111111111 %s", picking.name)
                continue

            # Only outgoing move lines from the source to the destination location
            # of this internal picking are candidates.
            for move in picking.move_lines.filtered(lambda m: m.product_id and m.product_id.tracking == 'serial'):
                lines = move.move_line_ids.sorted(key=lambda l: l.id)
                destination = move.location_dest_id or picking.location_dest_id

                # If there are no move lines yet, create enough lines for the
                # planned quantity. Odoo normally creates these during reservation.
                _logger.info("move.product_uom_qty 22222222222222222%s", move.product_uom_qty)
                if not lines and move.product_uom_qty:
                    qty = int(move.product_uom_qty)
                    if qty != move.product_uom_qty:
                        raise ValidationError(_(
                            'Serial-tracked product "%s" has a non-integer quantity (%s). '
                            'Serial tracking requires one serial per unit.'
                        ) % (move.product_id.display_name, move.product_uom_qty))
                    vals = []
                    for _i in range(qty):
                        vals.append({
                            'picking_id': picking.id,
                            'move_id': move.id,
                            'product_id': move.product_id.id,
                            'product_uom_id': move.product_uom.id,
                            'location_id': move.location_id.id,
                            'location_dest_id': destination.id,
                            'qty_done': 1.0,
                        })
                    lines = self.env['stock.move.line'].create(vals)
                    _logger.info("lines 3333333333333333333%s", lines)

                for line in lines:
                    # Ignore already identified serials.
                    if line.lot_id or line.lot_name:
                        _logger.info("Skipping line %s because it already has a lot/serial assigned.4444444444444444", line.id)
                        continue
                    if line.qty_done <= 0 and not picking._context.get('generate_for_planned_qty'):
                        _logger.info("Skipping line %s because qty_done is 0 and generate_for_planned_qty is not set.5555555555555555", line.id)
                        continue

                    try:
                        serial = picking._next_serial(destination, line.product_id)
                    except ValidationError:
                        if raise_on_missing_prefix:
                            raise
                        continue

                    existing = StockProductionLot.search([
                        ('name', '=', serial),
                        ('product_id', '=', line.product_id.id),
                    ], limit=1)
                    _logger.info("existing 66666666666666666%s", existing)
                    if existing:
                        # This should be extremely unlikely because the sequence is
                        # independent per prefix, but never duplicate a lot.
                        raise ValidationError(_(
                            'Generated serial "%s" already exists for product "%s".'
                        ) % (serial, line.product_id.display_name))

                    # Odoo 13's stock.move.line supports lot_name for entering a
                    # new lot/serial during transfer validation.
                    line.write({'lot_name': serial})
                    _logger.info("line.write 77777777777777777%s", serial)
                    processed = True

        if processed:
            self.write({'serial_prefix_generated': True})
        return processed

    
    def button_validate(self):
        # Generate missing serials before standard validation. This is required
        # for serial-tracked products because Odoo 13 may reject validation if a
        # serial number is missing.
        self._generate_serials_for_picking(raise_on_missing_prefix=True)
        return super(StockPicking, self).button_validate()

    
    def action_generate_serial_prefix(self):
        """Server-action friendly method.

        This is intentionally conservative: it only processes internal pickings
        and only fills missing lot/serial names. It does not overwrite existing
        serials. Run it on a completed picking only for lines where your workflow
        allows the lot to be added after completion.
        """
        self._generate_serials_for_picking(raise_on_missing_prefix=True)
        return True
