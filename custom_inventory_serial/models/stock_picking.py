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

    
    # def _generate_serials_for_picking(self, raise_on_missing_prefix=True):
    #     """Generate and assign missing serials to done/reserved move lines.

    #     For validation-time processing, this method assigns lot_name to move lines
    #     before the standard stock validation so tracked products can be validated.
    #     It only creates serials for products with tracking == 'serial'.
    #     Existing lot_id/lot_name values are never overwritten.
    #     """
    #     StockProductionLot = self.env['stock.production.lot'].sudo()
    #     processed = False

    #     _logger.info("Skipping StockProductionLot11111111112222222222222333333333333 %s", StockProductionLot)

    #     for picking in self:
    #         if not picking._is_internal_transfer_for_serials():
    #             _logger.info("Skipping picking11111111111111111111 %s", picking.name)
    #             continue

    #         # Only outgoing move lines from the source to the destination location
    #         # of this internal picking are candidates.
    #         for move in picking.move_lines.filtered(lambda m: m.product_id and m.product_id.tracking == 'serial'):
    #             lines = move.move_line_ids.sorted(key=lambda l: l.id)
    #             destination = move.location_dest_id or picking.location_dest_id

    #             # If there are no move lines yet, create enough lines for the
    #             # planned quantity. Odoo normally creates these during reservation.
    #             _logger.info("move.product_uom_qty 22222222222222222%s", move.product_uom_qty)
    #             if not lines and move.product_uom_qty:
    #                 qty = int(move.product_uom_qty)
    #                 if qty != move.product_uom_qty:
    #                     raise ValidationError(_(
    #                         'Serial-tracked product "%s" has a non-integer quantity (%s). '
    #                         'Serial tracking requires one serial per unit.'
    #                     ) % (move.product_id.display_name, move.product_uom_qty))
    #                 vals = []
    #                 for _i in range(qty):
    #                     vals.append({
    #                         'picking_id': picking.id,
    #                         'move_id': move.id,
    #                         'product_id': move.product_id.id,
    #                         'product_uom_id': move.product_uom.id,
    #                         'location_id': move.location_id.id,
    #                         'location_dest_id': destination.id,
    #                         'qty_done': 1.0,
    #                     })
    #                 lines = self.env['stock.move.line'].create(vals)
    #                 _logger.info("lines 3333333333333333333%s", lines)

    #             for line in lines:
    #                 # Ignore already identified serials.
    #                 if line.lot_id or line.lot_name:
    #                     _logger.info("Skipping line %s because it already has a lot/serial assigned.4444444444444444", line.id)
    #                     continue
    #                 if line.qty_done <= 0 and not picking._context.get('generate_for_planned_qty'):
    #                     _logger.info("Skipping line %s because qty_done is 0 and generate_for_planned_qty is not set.5555555555555555", line.id)
    #                     continue

    #                 try:
    #                     serial = picking._next_serial(destination, line.product_id)
    #                 except ValidationError:
    #                     if raise_on_missing_prefix:
    #                         raise
    #                     continue

    #                 existing = StockProductionLot.search([
    #                     ('name', '=', serial),
    #                     ('product_id', '=', line.product_id.id),
    #                 ], limit=1)
    #                 _logger.info("existing 66666666666666666%s", existing)
    #                 if existing:
    #                     # This should be extremely unlikely because the sequence is
    #                     # independent per prefix, but never duplicate a lot.
    #                     raise ValidationError(_(
    #                         'Generated serial "%s" already exists for product "%s".'
    #                     ) % (serial, line.product_id.display_name))

    #                 # Odoo 13's stock.move.line supports lot_name for entering a
    #                 # new lot/serial during transfer validation.
    #                 line.write({'lot_name': serial})
    #                 _logger.info("line.write 77777777777777777%s", serial)
    #                 processed = True

    #     if processed:
    #         self.write({'serial_prefix_generated': True})
    #     return processed

    def _generate_serials_for_picking(self, raise_on_missing_prefix=True):
        StockProductionLot = self.env['stock.production.lot'].sudo()
        processed = False

        _logger.info("========== SERIAL GENERATION START ==========")
        _logger.info("Picking recordset: %s", self)
        _logger.info("Picking IDs: %s", self.ids)
        _logger.info("StockProductionLot model: %s", StockProductionLot)

        for picking in self:

            _logger.info("------------------------------------------------")
            _logger.info("PROCESSING PICKING")
            _logger.info("Picking ID: %s", picking.id)
            _logger.info("Picking Name: %s", picking.name)
            _logger.info("Picking State: %s", picking.state)
            _logger.info(
                "Picking Type: %s",
                picking.picking_type_id.name
            )
            _logger.info(
                "Picking Type Code: %s",
                picking.picking_type_id.code
            )

            # --------------------------------------------------
            # INTERNAL TRANSFER CHECK
            # --------------------------------------------------

            is_internal = picking._is_internal_transfer_for_serials()

            _logger.info(
                "Is Internal Transfer: %s",
                is_internal
            )

            if not is_internal:

                _logger.warning(
                    "STOPPED: Picking %s is NOT an internal transfer",
                    picking.name
                )

                continue

            # --------------------------------------------------
            # MOVE COUNT
            # --------------------------------------------------

            _logger.info(
                "Total Moves: %s",
                len(picking.move_lines)
            )

            _logger.info(
                "Move IDs: %s",
                picking.move_lines.ids
            )

            # --------------------------------------------------
            # CHECK EVERY MOVE
            # --------------------------------------------------

            for move in picking.move_lines:

                product = move.product_id

                _logger.info("==============================================")
                _logger.info("PROCESSING MOVE")
                _logger.info("Move ID: %s", move.id)
                _logger.info("Product: %s", product.display_name)
                _logger.info("Product ID: %s", product.id)
                _logger.info(
                    "Product Tracking: %s",
                    product.tracking
                )
                _logger.info(
                    "Product Prefix Code: %s",
                    product.product_tmpl_id.prefix_code
                )
                _logger.info(
                    "Planned Quantity: %s",
                    move.product_uom_qty
                )
                _logger.info(
                    "Move Location: %s",
                    move.location_id.display_name
                )
                _logger.info(
                    "Destination Location: %s",
                    move.location_dest_id.display_name
                )

                # --------------------------------------------------
                # TRACKING CHECK
                # --------------------------------------------------

                if product.tracking != 'serial':

                    _logger.warning(
                        "STOPPED MOVE %s: Product tracking is '%s', "
                        "not 'serial'",
                        move.id,
                        product.tracking
                    )

                    continue

                _logger.info(
                    "Product IS serial tracked. Continuing..."
                )

                # --------------------------------------------------
                # MOVE LINES
                # --------------------------------------------------

                lines = move.move_line_ids.sorted(
                    key=lambda l: l.id
                )

                _logger.info(
                    "Move Line Count: %s",
                    len(lines)
                )

                _logger.info(
                    "Move Line IDs: %s",
                    lines.ids
                )

                destination = (
                    move.location_dest_id
                    or picking.location_dest_id
                )

                _logger.info(
                    "Final Destination: %s",
                    destination.display_name
                )

                # --------------------------------------------------
                # LOCATION PREFIX
                # --------------------------------------------------

                _logger.info(
                    "Building Code: %s",
                    destination.building_code
                )

                _logger.info(
                    "Floor Code: %s",
                    destination.floor_code
                )

                _logger.info(
                    "Hall Code: %s",
                    destination.hall_code
                )

                _logger.info(
                    "Location Prefix: %s",
                    destination.location_prefix
                )

                # --------------------------------------------------
                # CREATE MOVE LINES IF REQUIRED
                # --------------------------------------------------

                if not lines and move.product_uom_qty:

                    _logger.info(
                        "No move lines. Creating move lines."
                    )

                    qty = int(move.product_uom_qty)

                    if qty != move.product_uom_qty:

                        raise ValidationError(_(
                            'Serial-tracked product "%s" has '
                            'a non-integer quantity (%s).'
                        ) % (
                            product.display_name,
                            move.product_uom_qty,
                        ))

                    vals = []

                    for _i in range(qty):

                        vals.append({
                            'picking_id': picking.id,
                            'move_id': move.id,
                            'product_id': product.id,
                            'product_uom_id': move.product_uom.id,
                            'location_id': move.location_id.id,
                            'location_dest_id': destination.id,
                            'qty_done': 1.0,
                        })

                    lines = self.env[
                        'stock.move.line'
                    ].create(vals)

                    _logger.info(
                        "Created Move Lines: %s",
                        lines.ids
                    )

                # --------------------------------------------------
                # PROCESS MOVE LINES
                # --------------------------------------------------

                for line in lines:

                    _logger.info(
                        "--------------------------------------------"
                    )

                    _logger.info(
                        "PROCESSING MOVE LINE: %s",
                        line.id
                    )

                    _logger.info(
                        "Qty Done: %s",
                        line.qty_done
                    )

                    _logger.info(
                        "Lot ID: %s",
                        line.lot_id
                    )

                    _logger.info(
                        "Lot Name: %s",
                        line.lot_name
                    )

                    # --------------------------------------------------
                    # EXISTING SERIAL
                    # --------------------------------------------------

                    if line.lot_id or line.lot_name:

                        _logger.warning(
                            "STOPPED LINE %s: Already has serial/lot. "
                            "Lot ID=%s Lot Name=%s",
                            line.id,
                            line.lot_id,
                            line.lot_name,
                        )

                        continue

                    # --------------------------------------------------
                    # QTY DONE
                    # --------------------------------------------------

                    if (
                        line.qty_done <= 0
                        and not picking._context.get(
                            'generate_for_planned_qty'
                        )
                    ):

                        _logger.warning(
                            "STOPPED LINE %s: qty_done is 0",
                            line.id
                        )

                        continue

                    # --------------------------------------------------
                    # GENERATE SERIAL
                    # --------------------------------------------------

                    _logger.info(
                        "Calling _next_serial()..."
                    )

                    try:

                        serial = picking._next_serial(
                            destination,
                            line.product_id
                        )

                    except Exception as e:

                        _logger.exception(
                            "ERROR generating serial for line %s",
                            line.id
                        )

                        if raise_on_missing_prefix:
                            raise

                        continue

                    _logger.info(
                        "GENERATED SERIAL: %s",
                        serial
                    )

                    # --------------------------------------------------
                    # DUPLICATE CHECK
                    # --------------------------------------------------

                    existing = StockProductionLot.search([
                        ('name', '=', serial),
                        ('product_id', '=', line.product_id.id),
                    ], limit=1)

                    _logger.info(
                        "Existing Lot Search Result: %s",
                        existing
                    )

                    if existing:

                        _logger.error(
                            "SERIAL ALREADY EXISTS: %s",
                            serial
                        )

                        raise ValidationError(_(
                            'Generated serial "%s" already exists '
                            'for product "%s".'
                        ) % (
                            serial,
                            line.product_id.display_name,
                        ))

                    # --------------------------------------------------
                    # ASSIGN SERIAL
                    # --------------------------------------------------

                    _logger.info(
                        "Writing lot_name = %s to line %s",
                        serial,
                        line.id
                    )

                    line.write({
                        'lot_name': serial
                    })

                    _logger.info(
                        "SUCCESS: Serial %s assigned to line %s",
                        serial,
                        line.id
                    )

                    processed = True

        # --------------------------------------------------
        # FINAL RESULT
        # --------------------------------------------------

        _logger.info(
            "========== SERIAL GENERATION END =========="
        )

        _logger.info(
            "Processed: %s",
            processed
        )

        if processed:

            self.write({
                'serial_prefix_generated': True
            })

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
