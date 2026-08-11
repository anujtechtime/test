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
        Generate / rename serial numbers for internal transfers.

        Example:

            Existing serial:
                T000

            Destination:
                Building = N
                Floor    = F
                Hall     = 5

            Location prefix:
                NF5

            Product prefix:
                x

            New serial:
                NF5x0001

        IMPORTANT:
            If a move line already has a serial, that serial is RENAMED.
            We do not create an additional stock quantity.
        """

        StockProductionLot = self.env[
            'stock.production.lot'
        ].sudo()

        processed = False

        _logger.info(
            '================================================='
        )
        _logger.info(
            'SERIAL GENERATION / RENAME START'
        )
        _logger.info(
            '================================================='
        )

        for picking in self:

            _logger.info(
                'Processing Picking: %s | ID: %s | State: %s',
                picking.name,
                picking.id,
                picking.state
            )

            # ==========================================================
            # 1. INTERNAL TRANSFER CHECK
            # ==========================================================

            if not picking._is_internal_transfer_for_serials():

                _logger.info(
                    'Skipping %s - not an internal transfer.',
                    picking.name
                )

                continue

            # ==========================================================
            # 2. GET MOVES
            # ==========================================================

            moves = picking.move_ids_without_package

            if not moves:

                self.action_done()


            # ==========================================================
            # 3. PROCESS EACH MOVE
            # ==========================================================

            for move in moves:

                product = move.product_id

                if not product:
                    continue

                _logger.info(
                    '----------------------------------------------'
                )

                _logger.info(
                    'Move ID: %s',
                    move.id
                )

                _logger.info(
                    'Product: %s',
                    product.display_name
                )

                _logger.info(
                    'Product ID: %s',
                    product.id
                )

                _logger.info(
                    'Tracking: %s',
                    product.tracking
                )

                _logger.info(
                    'Quantity: %s',
                    move.product_uom_qty
                )

                # ======================================================
                # 4. SERIAL TRACKING CHECK
                # ======================================================

                if product.tracking != 'serial':

                    _logger.warning(
                        'Skipping %s because tracking is "%s".',
                        product.display_name,
                        product.tracking
                    )

                    continue

                # ======================================================
                # 5. PRODUCT PREFIX
                # ======================================================

                product_prefix = (
                    product.product_tmpl_id.prefix_code or ''
                ).strip()

                if not product_prefix:

                    raise ValidationError(_(
                        'Product "%s" does not have a '
                        'Product Prefix Code.'
                    ) % product.display_name)

                # ======================================================
                # 6. DESTINATION
                # ======================================================

                destination = (
                    move.location_dest_id
                    or picking.location_dest_id
                )

                if not destination:

                    raise ValidationError(_(
                        'Destination location is missing for '
                        'product "%s".'
                    ) % product.display_name)

                _logger.info(
                    'Destination: %s',
                    destination.display_name
                )

                # ======================================================
                # 7. LOCATION PREFIX
                # ======================================================

                location_prefix = (
                    picking._get_location_prefix(
                        destination
                    )
                )

                if not location_prefix:

                    raise ValidationError(_(
                        'Destination Location "%s" does not '
                        'have a Location Prefix.'
                    ) % destination.display_name)

                # ======================================================
                # 8. VALIDATE PREFIX
                # ======================================================

                picking._validate_prefix(
                    location_prefix,
                    _('Location')
                )

                picking._validate_prefix(
                    product_prefix,
                    _('Product')
                )

                # ======================================================
                # 9. FULL PREFIX
                # ======================================================

                full_prefix = '%s%s' % (
                    location_prefix,
                    product_prefix
                )

                _logger.info(
                    'Location Prefix: %s',
                    location_prefix
                )

                _logger.info(
                    'Product Prefix: %s',
                    product_prefix
                )

                _logger.info(
                    'FULL PREFIX: %s',
                    full_prefix
                )

                # ======================================================
                # 10. GET SEQUENCE
                # ======================================================

                sequence = picking._get_serial_sequence(
                    full_prefix
                )

                # ======================================================
                # 11. GET MOVE LINES
                # ======================================================

                lines = move.move_line_ids.sorted(
                    key=lambda line: line.id
                )

                _logger.info(
                    'Move Lines: %s',
                    lines.ids
                )

                # ======================================================
                # 12. IMPORTANT
                #
                # We should NOT blindly create move lines here.
                # The transfer should already have its move lines
                # after confirmation/reservation.
                # ======================================================

                if not lines:

                    _logger.warning(
                        'No move lines found for move %s.',
                        move.id
                    )

                    if raise_on_missing_prefix:

                        raise ValidationError(_(
                            'No stock move lines exist for product "%s". '
                            'Please confirm and reserve the transfer first.'
                        ) % product.display_name)

                    continue

                # ======================================================
                # 13. PROCESS MOVE LINES
                # ======================================================

                for line in lines:

                    _logger.info(
                        '=============================================='
                    )

                    _logger.info(
                        'Processing Move Line: %s',
                        line.id
                    )

                    _logger.info(
                        'Qty Done: %s',
                        line.qty_done
                    )

                    _logger.info(
                        'Current lot_id: %s',
                        line.lot_id.name
                        if line.lot_id
                        else False
                    )

                    _logger.info(
                        'Current lot_name: %s',
                        line.lot_name
                    )

                    # ==================================================
                    # 14. FIND EXISTING SERIAL
                    # ==================================================

                    old_lot = line.lot_id

                    if not old_lot and line.lot_name:

                        old_lot = StockProductionLot.search([
                            ('name', '=', line.lot_name),
                            ('product_id', '=', product.id),
                        ], limit=1)

                    # ==================================================
                    # 15. GENERATE NEW SERIAL
                    # ==================================================

                    new_serial = sequence.next_by_id()

                    if not new_serial:

                        raise ValidationError(_(
                            'Unable to generate serial number '
                            'for prefix "%s".'
                        ) % full_prefix)

                    _logger.info(
                        'Generated New Serial: %s',
                        new_serial
                    )

                    # ==================================================
                    # 16. CHECK NEW SERIAL DUPLICATE
                    # ==================================================

                    existing_new_lot = StockProductionLot.search([
                        ('name', '=', new_serial),
                        ('product_id', '=', product.id),
                    ], limit=1)

                    if existing_new_lot:

                        raise ValidationError(_(
                            'Generated serial "%s" already exists '
                            'for product "%s".'
                        ) % (
                            new_serial,
                            product.display_name
                        ))

                    # ==================================================
                    # 17. EXISTING SERIAL FOUND
                    #
                    # Rename the existing lot.
                    # DO NOT create another quantity.
                    # ==================================================

                    if old_lot:

                        _logger.info(
                            'Existing Serial Found: %s',
                            old_lot.name
                        )

                        _logger.info(
                            'Renaming Serial %s -> %s',
                            old_lot.name,
                            new_serial
                        )

                        old_lot.write({
                            'name': new_serial,
                        })

                        # Keep the existing lot_id.
                        line.write({
                            'lot_id': old_lot.id,
                            'lot_name': False,
                        })

                        _logger.info(
                            'SUCCESS: Existing serial renamed.'
                        )

                    # ==================================================
                    # 18. NO EXISTING SERIAL
                    #
                    # This normally happens when the transfer was
                    # created without an existing serial.
                    # ==================================================

                    else:

                        _logger.info(
                            'No existing serial found.'
                        )

                        # Find/create the new lot.

                        new_lot = StockProductionLot.create({
                            'name': new_serial,
                            'product_id': product.id,
                            'company_id': picking.company_id.id,
                        })

                        line.write({
                            'lot_id': new_lot.id,
                            'lot_name': False,
                        })

                        _logger.info(
                            'Created new serial: %s',
                            new_serial
                        )

                    processed = True

        # ==============================================================
        # 19. MARK PICKING
        # ==============================================================

        if processed:

            self.write({
                'serial_prefix_generated': True
            })

        _logger.info(
            '================================================='
        )

        _logger.info(
            'SERIAL GENERATION / RENAME END | PROCESSED=%s',
            processed
        )

        _logger.info(
            '================================================='
        )

        return processed

    # ============================================================
    # BUTTON / SERVER ACTION
    # ============================================================

    def action_generate_serial_prefix(self):
        self.ensure_one()

        _logger.info("========== DEBUG TRANSFER ==========")
        _logger.info("Picking: %s", self.name)
        _logger.info("State: %s", self.state)
        _logger.info("Picking Type: %s", self.picking_type_id.code)

        _logger.info(
            "picking.move_lines: %s",
            self.move_lines
        )

        _logger.info(
            "picking.move_ids_without_package: %s",
            self.move_ids_without_package
        )

        _logger.info(
            "picking.move_line_ids: %s",
            self.move_line_ids
        )

        _logger.info(
            "move_ids_without_package IDs: %s",
            self.move_ids_without_package.ids
        )

        _logger.info(
            "move_lines IDs: %s",
            self.move_lines.ids
        )

        _logger.info(
            "move_line_ids IDs: %s",
            self.move_line_ids.ids
        )

        _logger.info("===================================")

        return self._generate_serials_for_picking(
            raise_on_missing_prefix=True
        )

    # ============================================================
    # VALIDATE
    # ============================================================

    def button_validate(self):

        self._generate_serials_for_picking(
            raise_on_missing_prefix=True
        )

        return super(
            StockPicking,
            self
        ).button_validate()