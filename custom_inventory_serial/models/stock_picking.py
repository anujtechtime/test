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
    # PREPARE STOCK MOVE VALS - CREATE MOVE FROM MOVE LINE
    # ============================================================

    def _prepare_stock_move_vals(self, line, picking):
        """
        Prepare values for creating a stock.move from a stock.move.line
        This is copied from Odoo's native action_done method
        """
        return {
            'name': _('New Move:') + line.product_id.display_name,
            'product_id': line.product_id.id,
            'product_uom_qty': line.qty_done,
            'product_uom': line.product_uom_id.id,
            'description_picking': line.description_picking,
            'location_id': picking.location_id.id,
            'location_dest_id': picking.location_dest_id.id,
            'picking_id': picking.id,
            'picking_type_id': picking.picking_type_id.id,
            'restrict_partner_id': picking.owner_id.id,
            'company_id': picking.company_id.id,
        }

    # ============================================================
    # CREATE MOVES FROM MOVE LINES (IF NO MOVES EXIST)
    # ============================================================

    def _create_moves_from_move_lines(self, picking):
        """
        Create stock.moves from stock.move.lines that don't have a move_id
        This is the exact logic from Odoo's action_done method
        """
        moves_created = False
        
        # Process move lines that don't have a move_id
        for ops in picking.move_line_ids.filtered(lambda x: not x.move_id):
            _logger.info(
                'Creating move from move line %s for product %s',
                ops.id,
                ops.product_id.display_name
            )
            
            # Create new move from move line
            new_move = self.env['stock.move'].create(
                self._prepare_stock_move_vals(ops, picking)
            )
            ops.move_id = new_move.id
            new_move = new_move._action_confirm()
            _logger.info('Created new move: %s', new_move.id)
            moves_created = True
        
        return moves_created

    # ============================================================
    # MAIN SERIAL GENERATION METHOD - UPDATED
    # ============================================================

    def _generate_serials_for_picking(
        self,
        raise_on_missing_prefix=True
    ):
        """
        Generate serial numbers for internal transfers.

        Example:

            Destination:
                Building = N
                Floor    = F
                Hall     = 5
                Prefix   = NF5

            Product:
                Prefix   = x

            Generated:
                NF5x0001
                NF5x0002
                NF5x0003

        Important:
            - Only internal transfers are processed.
            - Only serial-tracked products are processed.
            - Existing lot/serial numbers are never overwritten.
            - One serial is generated for each unit.
        """

        StockProductionLot = self.env[
            'stock.production.lot'
        ].sudo()

        processed = False

        _logger.info(
            '========== SERIAL GENERATION START =========='
        )

        for picking in self:

            _logger.info(
                'Processing Picking: %s | ID: %s',
                picking.name,
                picking.id
            )

            _logger.info(
                'Picking State: %s',
                picking.state
            )

            _logger.info(
                'Picking Type: %s',
                picking.picking_type_id.name
            )

            _logger.info(
                'Picking Type Code: %s',
                picking.picking_type_id.code
            )

            # ----------------------------------------------------
            # INTERNAL TRANSFER CHECK
            # ----------------------------------------------------

            if not picking._is_internal_transfer_for_serials():

                _logger.info(
                    'Skipping %s because it is not an '
                    'internal transfer.',
                    picking.name
                )

                continue

            # ----------------------------------------------------
            # CHECK FOR MOVE LINES AND CREATE MOVES IF NEEDED
            # ----------------------------------------------------
            
            # First, check if there are move lines without moves
            move_lines_without_move = picking.move_line_ids.filtered(
                lambda x: not x.move_id
            )
            
            if move_lines_without_move:
                _logger.info(
                    'Found %s move lines without moves. Creating moves...',
                    len(move_lines_without_move)
                )
                # Create moves from move lines
                self._create_moves_from_move_lines(picking)
                
                # Refresh the picking to get the new moves
                picking.refresh()
            
            # ----------------------------------------------------
            # GET MOVES
            # ----------------------------------------------------

            moves = picking.move_ids_without_package

            _logger.info(
                'Move IDs: %s',
                moves.ids
            )

            _logger.info(
                'Total Moves: %s',
                len(moves)
            )

            # ----------------------------------------------------
            # FALLBACK: DIRECT SEARCH IN STOCK.MOVE
            # ----------------------------------------------------

            if not moves:

                moves = self.env[
                    'stock.move'
                ].search(
                    [
                        ('picking_id', '=', picking.id)
                    ]
                )

                _logger.info(
                    'Fallback stock.move search IDs: %s',
                    moves.ids
                )

            # ----------------------------------------------------
            # STILL NO MOVES - CHECK MOVE LINES
            # ----------------------------------------------------

            if not moves:
                _logger.warning(
                    'NO STOCK MOVES FOUND FOR PICKING %s',
                    picking.name
                )
                
                # Check if there are move lines that can be used
                if picking.move_line_ids:
                    _logger.info(
                        'Found %s move lines. Creating moves from them...',
                        len(picking.move_line_ids)
                    )
                    self._create_moves_from_move_lines(picking)
                    
                    # Refresh and try again
                    picking.refresh()
                    moves = picking.move_ids_without_package
                    
                    if moves:
                        _logger.info(
                            'Successfully created moves from move lines: %s',
                            moves.ids
                        )
                    else:
                        _logger.warning(
                            'Failed to create moves from move lines for %s',
                            picking.name
                        )
                        continue
                else:
                    _logger.warning(
                        'No move lines or moves found for picking %s',
                        picking.name
                    )
                    continue

            # ====================================================
            # PROCESS EACH MOVE
            # ====================================================

            for move in moves:

                product = move.product_id

                _logger.info(
                    '--------------------------------------------'
                )

                _logger.info(
                    'Processing Move ID: %s',
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
                    'Product Tracking: %s',
                    product.tracking
                )

                _logger.info(
                    'Product Prefix: %s',
                    product.product_tmpl_id.prefix_code
                )

                _logger.info(
                    'Demand Quantity: %s',
                    move.product_uom_qty
                )

                _logger.info(
                    'Source Location: %s',
                    move.location_id.display_name
                )

                _logger.info(
                    'Destination Location: %s',
                    move.location_dest_id.display_name
                )

                # ------------------------------------------------
                # PRODUCT CHECK
                # ------------------------------------------------

                if not product:

                    _logger.warning(
                        'Skipping move %s because product '
                        'is missing.',
                        move.id
                    )

                    continue

                # ------------------------------------------------
                # TRACKING CHECK
                # ------------------------------------------------

                if product.tracking != 'serial':

                    _logger.warning(
                        'Skipping product %s because tracking '
                        'is "%s", not "serial".',
                        product.display_name,
                        product.tracking
                    )

                    continue

                # ------------------------------------------------
                # DESTINATION
                # ------------------------------------------------

                destination = (
                    move.location_dest_id
                    or picking.location_dest_id
                )

                if not destination:

                    raise ValidationError(
                        _(
                            'Destination location is missing '
                            'for product "%s".'
                        ) % product.display_name
                    )

                _logger.info(
                    'Destination Location ID: %s',
                    destination.id
                )

                _logger.info(
                    'Destination Location Name: %s',
                    destination.display_name
                )

                # ------------------------------------------------
                # LOCATION PREFIX
                # ------------------------------------------------

                location_prefix = (
                    picking._get_location_prefix(
                        destination
                    )
                )

                _logger.info(
                    'Location Prefix: %s',
                    location_prefix
                )

                # ------------------------------------------------
                # PRODUCT PREFIX
                # ------------------------------------------------

                product_prefix = (
                    picking._get_product_prefix(
                        product
                    )
                )

                _logger.info(
                    'Product Prefix: %s',
                    product_prefix
                )

                # ------------------------------------------------
                # VALIDATE PREFIXES
                # ------------------------------------------------

                picking._validate_prefix(
                    location_prefix,
                    _('Location')
                )

                picking._validate_prefix(
                    product_prefix,
                    _('Product')
                )

                # ------------------------------------------------
                # EXISTING MOVE LINES
                # ------------------------------------------------

                lines = move.move_line_ids.sorted(
                    key=lambda line: line.id
                )

                _logger.info(
                    'Existing Move Lines: %s',
                    lines.ids
                )

                # =================================================
                # CREATE MOVE LINES IF NONE EXIST
                # =================================================

                if not lines:

                    quantity = move.product_uom_qty

                    _logger.info(
                        'No move lines found.'
                    )

                    _logger.info(
                        'Creating lines for quantity: %s',
                        quantity
                    )

                    if quantity <= 0:

                        _logger.warning(
                            'Skipping move %s because quantity '
                            'is zero.',
                            move.id
                        )

                        continue

                    if int(quantity) != quantity:

                        raise ValidationError(
                            _(
                                'Serial-tracked product "%s" '
                                'has a non-integer quantity (%s). '
                                'Serial tracking requires one '
                                'serial per unit.'
                            ) % (
                                product.display_name,
                                quantity
                            )
                        )

                    vals = []

                    for index in range(
                        int(quantity)
                    ):

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
                        'Created Move Lines: %s',
                        lines.ids
                    )

                # =================================================
                # PROCESS EACH MOVE LINE
                # =================================================

                for line in lines:

                    _logger.info(
                        '============================================'
                    )

                    _logger.info(
                        'Processing Move Line ID: %s',
                        line.id
                    )

                    _logger.info(
                        'Qty Done: %s',
                        line.qty_done
                    )

                    _logger.info(
                        'Lot ID: %s',
                        line.lot_id.id if line.lot_id else False
                    )

                    _logger.info(
                        'Lot Name: %s',
                        line.lot_name
                    )

                    # ------------------------------------------------
                    # EXISTING SERIAL
                    # ------------------------------------------------

                    if line.lot_id or line.lot_name:

                        _logger.info(
                            'Skipping line %s because serial '
                            'already exists.',
                            line.id
                        )

                        continue

                    # ------------------------------------------------
                    # QTY DONE
                    # ------------------------------------------------

                    if line.qty_done <= 0:

                        _logger.info(
                            'qty_done is 0 for line %s. '
                            'Setting qty_done to 1 for '
                            'serial generation.',
                            line.id
                        )

                        line.write({
                            'qty_done': 1.0
                        })

                    # ------------------------------------------------
                    # GENERATE SERIAL
                    # ------------------------------------------------

                    _logger.info(
                        'Generating serial for:'
                    )

                    _logger.info(
                        'Location Prefix = %s',
                        location_prefix
                    )

                    _logger.info(
                        'Product Prefix = %s',
                        product_prefix
                    )

                    try:

                        serial = picking._next_serial(
                            destination,
                            product
                        )

                    except ValidationError:

                        _logger.exception(
                            'Prefix validation failed for '
                            'move line %s.',
                            line.id
                        )

                        if raise_on_missing_prefix:
                            raise

                        continue

                    _logger.info(
                        'Generated Serial: %s',
                        serial
                    )

                    # ------------------------------------------------
                    # DUPLICATE CHECK
                    # ------------------------------------------------

                    existing = StockProductionLot.search(
                        [
                            ('name', '=', serial),
                            (
                                'product_id',
                                '=',
                                product.id
                            ),
                        ],
                        limit=1
                    )

                    _logger.info(
                        'Existing Lot Search Result: %s',
                        existing
                    )

                    if existing:

                        raise ValidationError(
                            _(
                                'Generated serial "%s" '
                                'already exists for product "%s".'
                            ) % (
                                serial,
                                product.display_name
                            )
                        )

                    # ------------------------------------------------
                    # CREATE LOT AND ASSIGN SERIAL
                    # ------------------------------------------------

                    _logger.info(
                        'Creating lot and assigning serial %s to move line %s',
                        serial,
                        line.id
                    )

                    try:
                        # Create the lot/serial record
                        lot = StockProductionLot.create({
                            'name': serial,
                            'product_id': product.id,
                            'company_id': picking.company_id.id or self.env.company.id,
                        })

                        # Assign the lot to the move line
                        line.write({
                            'lot_id': lot.id,  # Use lot_id instead of lot_name
                            'qty_done': 1.0,
                        })

                        _logger.info(
                            'SUCCESS: Serial %s assigned to move line %s',
                            serial,
                            line.id
                        )

                        processed = True

                    except Exception as e:
                        _logger.error(
                            'Failed to create/assign serial %s: %s',
                            serial,
                            str(e)
                        )
                        raise ValidationError(
                            _('Failed to assign serial number: %s') % str(e)
                        )

        # --------------------------------------------------------
        # END PICKING LOOP
        # --------------------------------------------------------

        # ============================================================
        # MARK PICKING AS PROCESSED
        # ============================================================

        if processed:

            self.write({
                'serial_prefix_generated': True
            })

        _logger.info(
            '========== SERIAL GENERATION END | '
            'PROCESSED=%s ==========',
            processed
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
        _logger.info("move_lines IDs: %s", self.move_lines.ids)
        _logger.info("move_line_ids IDs: %s", self.move_line_ids.ids)
        _logger.info("===================================")

        return self._generate_serials_for_picking(
            raise_on_missing_prefix=True
        )

    # ============================================================
    # VALIDATE - OVERRIDE TO GENERATE SERIALS
    # ============================================================

    def button_validate(self):
        """
        Override button_validate to generate serials before validation
        """
        for picking in self:
            if picking._is_internal_transfer_for_serials():
                _logger.info('Generating serials for internal transfer %s', picking.name)
                picking._generate_serials_for_picking(raise_on_missing_prefix=True)
        
        # Call the original button_validate
        return super(StockPicking, self).button_validate()