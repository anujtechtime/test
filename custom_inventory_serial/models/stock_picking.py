# -*- coding: utf-8 -*-

import re

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import logging

_logger = logging.getLogger(__name__)


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    serial_prefix_generated = fields.Boolean(
        string='Serial Prefix Generated',
        copy=False,
        readonly=True,
    )

    # ---------------------------------------------------------
    # INTERNAL TRANSFER CHECK
    # ---------------------------------------------------------

    def _is_internal_transfer_for_serials(self):
        self.ensure_one()
        return self.picking_type_id.code == 'internal'

    # ---------------------------------------------------------
    # LOCATION PREFIX
    # ---------------------------------------------------------

    def _get_location_prefix(self, location):

        if not location:
            return ''

        prefix = location.get_serial_prefix()

        return (prefix or '').strip()

    # ---------------------------------------------------------
    # PRODUCT PREFIX
    # ---------------------------------------------------------

    def _get_product_prefix(self, product):

        prefix = product.product_tmpl_id.prefix_code

        return (prefix or '').strip()

    # ---------------------------------------------------------
    # PREFIX VALIDATION
    # ---------------------------------------------------------

    def _validate_prefix(self, prefix, label):

        if not prefix:

            raise ValidationError(
                _('%s prefix code is required.') % label
            )

        if not re.match(r'^[A-Za-z0-9_-]+$', prefix):

            raise ValidationError(
                _(
                    '%s prefix "%s" contains unsupported characters. '
                    'Use only letters, numbers, underscore or hyphen.'
                ) % (label, prefix)
            )

    # ---------------------------------------------------------
    # GET / CREATE SEQUENCE
    # ---------------------------------------------------------

    @api.model
    def _get_serial_sequence(self, prefix):

        Sequence = self.env['ir.sequence'].sudo()

        code = 'custom_inventory_serial.%s' % prefix

        sequence = Sequence.search(
            [('code', '=', code)],
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

    # ---------------------------------------------------------
    # GENERATE NEXT SERIAL
    # ---------------------------------------------------------

    @api.model
    def _next_serial(self, location, product):

        location_prefix = self._get_location_prefix(location)

        product_prefix = self._get_product_prefix(product)

        self._validate_prefix(
            location_prefix,
            _('Location')
        )

        self._validate_prefix(
            product_prefix,
            _('Product')
        )

        full_prefix = '%s%s' % (
            location_prefix,
            product_prefix
        )

        _logger.info(
            "SERIAL PREFIX => Location=%s Product=%s Full=%s",
            location_prefix,
            product_prefix,
            full_prefix
        )

        sequence = self._get_serial_sequence(
            full_prefix
        )

        serial = sequence.next_by_id()

        _logger.info(
            "GENERATED SERIAL => %s",
            serial
        )

        return serial

    # =========================================================
    # MAIN SERIAL GENERATOR
    # =========================================================

    def _generate_serials_for_picking(
        self,
        raise_on_missing_prefix=True
    ):

        _logger.info(
            "================================================="
        )
        _logger.info(
            "SERIAL GENERATION START"
        )
        _logger.info(
            "================================================="
        )

        processed = False

        Lot = self.env[
            'stock.production.lot'
        ].sudo()

        MoveLine = self.env[
            'stock.move.line'
        ]

        for picking in self:

            _logger.info(
                "PICKING: %s | ID: %s | STATE: %s",
                picking.name,
                picking.id,
                picking.state
            )

            # -------------------------------------------------
            # CHECK INTERNAL TRANSFER
            # -------------------------------------------------

            if picking.picking_type_id.code != 'internal':

                _logger.warning(
                    "NOT INTERNAL TRANSFER: %s",
                    picking.name
                )

                continue

            # -------------------------------------------------
            # IMPORTANT:
            # TRANSFER MUST HAVE MOVES
            # -------------------------------------------------

            moves = picking.move_lines

            _logger.info(
                "MOVE IDS: %s",
                moves.ids
            )

            _logger.info(
                "NUMBER OF MOVES: %s",
                len(moves)
            )

            if not moves:

                raise ValidationError(
                    _(
                        'No stock moves exist on transfer "%s". '
                        'Please add a product and confirm the transfer '
                        'before generating serial numbers.'
                    ) % picking.name
                )

            # -------------------------------------------------
            # PROCESS EACH MOVE
            # -------------------------------------------------

            for move in moves:

                product = move.product_id

                _logger.info(
                    "---------------------------------------------"
                )

                _logger.info(
                    "MOVE ID: %s",
                    move.id
                )

                _logger.info(
                    "PRODUCT: %s",
                    product.display_name
                )

                _logger.info(
                    "PRODUCT ID: %s",
                    product.id
                )

                _logger.info(
                    "TRACKING: %s",
                    product.tracking
                )

                _logger.info(
                    "PRODUCT PREFIX: %s",
                    product.product_tmpl_id.prefix_code
                )

                _logger.info(
                    "SOURCE: %s",
                    move.location_id.complete_name
                )

                _logger.info(
                    "DESTINATION: %s",
                    move.location_dest_id.complete_name
                )

                _logger.info(
                    "DEMAND QTY: %s",
                    move.product_uom_qty
                )

                _logger.info(
                    "RESERVED QTY: %s",
                    move.reserved_availability
                )

                _logger.info(
                    "DONE QTY: %s",
                    move.quantity_done
                )

                # -------------------------------------------------
                # PRODUCT MUST BE SERIAL TRACKED
                # -------------------------------------------------

                if product.tracking != 'serial':

                    raise ValidationError(
                        _(
                            'Product "%s" is not configured for '
                            'Unique Serial Number tracking.'
                        ) % product.display_name
                    )

                # -------------------------------------------------
                # DESTINATION
                # -------------------------------------------------

                destination = move.location_dest_id

                if not destination:

                    raise ValidationError(
                        _(
                            'Destination location is missing for '
                            'product "%s".'
                        ) % product.display_name
                    )

                # -------------------------------------------------
                # LOCATION PREFIX
                # -------------------------------------------------

                location_prefix = (
                    self._get_location_prefix(
                        destination
                    )
                )

                _logger.info(
                    "LOCATION PREFIX: %s",
                    location_prefix
                )

                # -------------------------------------------------
                # PRODUCT PREFIX
                # -------------------------------------------------

                product_prefix = (
                    self._get_product_prefix(
                        product
                    )
                )

                _logger.info(
                    "PRODUCT PREFIX: %s",
                    product_prefix
                )

                # -------------------------------------------------
                # VALIDATE PREFIXES
                # -------------------------------------------------

                self._validate_prefix(
                    location_prefix,
                    _('Location')
                )

                self._validate_prefix(
                    product_prefix,
                    _('Product')
                )

                # -------------------------------------------------
                # EXISTING MOVE LINES
                # -------------------------------------------------

                move_lines = move.move_line_ids

                _logger.info(
                    "EXISTING MOVE LINE IDS: %s",
                    move_lines.ids
                )

                # -------------------------------------------------
                # QUANTITY
                # -------------------------------------------------

                demand_qty = int(
                    move.product_uom_qty
                )

                if demand_qty <= 0:

                    raise ValidationError(
                        _(
                            'Quantity must be greater than zero '
                            'for product "%s".'
                        ) % product.display_name
                    )

                # -------------------------------------------------
                # CREATE MOVE LINES IF NECESSARY
                # -------------------------------------------------

                if not move_lines:

                    _logger.info(
                        "NO MOVE LINES FOUND."
                    )

                    vals_list = []

                    for i in range(demand_qty):

                        vals_list.append({
                            'picking_id': picking.id,
                            'move_id': move.id,
                            'product_id': product.id,
                            'product_uom_id': move.product_uom.id,
                            'location_id': move.location_id.id,
                            'location_dest_id': destination.id,
                            'qty_done': 1.0,
                        })

                    move_lines = MoveLine.create(
                        vals_list
                    )

                    _logger.info(
                        "CREATED MOVE LINES: %s",
                        move_lines.ids
                    )

                # -------------------------------------------------
                # PROCESS MOVE LINES
                # -------------------------------------------------

                for line in move_lines:

                    _logger.info(
                        "============================================="
                    )

                    _logger.info(
                        "MOVE LINE ID: %s",
                        line.id
                    )

                    _logger.info(
                        "LOT ID: %s",
                        line.lot_id.id if line.lot_id else False
                    )

                    _logger.info(
                        "LOT NAME: %s",
                        line.lot_name
                    )

                    _logger.info(
                        "QTY DONE: %s",
                        line.qty_done
                    )

                    # ---------------------------------------------
                    # ALREADY HAS SERIAL
                    # ---------------------------------------------

                    if line.lot_id:

                        _logger.info(
                            "SERIAL ALREADY EXISTS: %s",
                            line.lot_id.name
                        )

                        continue

                    if line.lot_name:

                        _logger.info(
                            "LOT NAME ALREADY EXISTS: %s",
                            line.lot_name
                        )

                        continue

                    # ---------------------------------------------
                    # GENERATE SERIAL
                    # ---------------------------------------------

                    serial = self._next_serial(
                        destination,
                        product
                    )

                    _logger.info(
                        "SERIAL GENERATED: %s",
                        serial
                    )

                    # ---------------------------------------------
                    # CHECK EXISTING LOT
                    # ---------------------------------------------

                    existing_lot = Lot.search([
                        ('name', '=', serial),
                        ('product_id', '=', product.id),
                    ], limit=1)

                    if existing_lot:

                        raise ValidationError(
                            _(
                                'Serial "%s" already exists for '
                                'product "%s".'
                            ) % (
                                serial,
                                product.display_name
                            )
                        )

                    # ---------------------------------------------
                    # CREATE ACTUAL LOT/SERIAL RECORD
                    # ---------------------------------------------

                    lot = Lot.create({
                        'name': serial,
                        'product_id': product.id,
                        'company_id': (
                            picking.company_id.id
                            or self.env.company.id
                        ),
                    })

                    _logger.info(
                        "LOT CREATED: ID=%s NAME=%s",
                        lot.id,
                        lot.name
                    )

                    # ---------------------------------------------
                    # ASSIGN LOT DIRECTLY
                    # ---------------------------------------------

                    line.write({
                        'lot_id': lot.id,
                        'lot_name': serial,
                        'qty_done': 1.0,
                    })

                    # ---------------------------------------------
                    # FORCE CACHE REFRESH
                    # ---------------------------------------------

                    line.invalidate_cache()

                    _logger.info(
                        "AFTER WRITE:"
                    )

                    _logger.info(
                        "MOVE LINE LOT ID: %s",
                        line.lot_id.id
                    )

                    _logger.info(
                        "MOVE LINE LOT NAME: %s",
                        line.lot_id.name
                    )

                    _logger.info(
                        "MOVE LINE QTY DONE: %s",
                        line.qty_done
                    )

                    processed = True

            # -------------------------------------------------
            # MARK PICKING
            # -------------------------------------------------

            if processed:

                picking.write({
                    'serial_prefix_generated': True
                })

        _logger.info(
            "================================================="
        )

        _logger.info(
            "SERIAL GENERATION END | PROCESSED=%s",
            processed
        )

        _logger.info(
            "================================================="
        )

        return processed

    # =========================================================
    # BUTTON
    # =========================================================

    def action_generate_serial_prefix(self):

        self.ensure_one()

        self._generate_serials_for_picking(
            raise_on_missing_prefix=True
        )

        return True

    # =========================================================
    # VALIDATE
    # =========================================================

    def button_validate(self):

        _logger.info(
            "========== BUTTON VALIDATE =========="
        )

        for picking in self:

            if (
                picking.picking_type_id.code == 'internal'
                and picking.state not in ('done', 'cancel')
            ):

                picking._generate_serials_for_picking(
                    raise_on_missing_prefix=True
                )

        return super(
            StockPicking,
            self
        ).button_validate()