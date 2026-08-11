# -*- coding: utf-8 -*-
from odoo import models, api
import logging

_logger = logging.getLogger(__name__)

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    def _get_serial_prefix(self, location, product):
        location_prefix = (location.location_prefix or '').strip()
        product_code = (product.product_tmpl_id.product_test_code or '').strip()
        return '%s%s' % (location_prefix, product_code)

    def _next_serial_name(self, prefix):
        self.env.cr.execute(
            '''
            SELECT name
              FROM stock_production_lot
             WHERE name LIKE %s
             ORDER BY id DESC
             LIMIT 1
            ''',
            (prefix + '%',)
        )
        row = self.env.cr.fetchone()
        last_number = 0
        if row:
            name = row[0] or ''
            suffix = name[len(prefix):]
            if suffix.isdigit():
                last_number = int(suffix)
        return '%s%04d' % (prefix, last_number + 1)

    def action_generate_serials_from_destination(self):
            Lot = self.env['stock.production.lot']
            _logger.info("LOT11111111111111111111111 %s" % Lot)
            for picking in self:
                _logger.info("Processing picking: %s" % picking)
                if picking.state != 'done':
                    _logger.info("Picking is not done: %s" % picking)
                    continue
                for move_line in picking.move_line_ids:
                    _logger.info("Processing move line: %s" % move_line)
                    product = move_line.product_id
                    if product.tracking != 'serial':
                        _logger.info("Product is not tracked by serial: %s" % product.tracking)
                        continue
                    if move_line.lot_id:
                        _logger.info("Move line already has a lot: %s" % move_line.lot_id)
                        continue
                    location = move_line.location_dest_id
                    prefix = self._get_serial_prefix(location, product)
                    _logger.info("Generated prefix: %s" % prefix)
                    if not prefix:
                        continue
                    serial_name = self._next_serial_name(prefix)
                    _logger.info("Generated serial name: %s" % serial_name)
                    lot = Lot.create({
                        'name': serial_name,
                        'product_id': product.id,
                        'company_id': picking.company_id.id,
                    })
                    _logger.info("Generated lotwwwwwwwwwwww: %s" % lot)
                    move_line.lot_id = lot.id
            return True
    

    def button_validate(self):
        result = super(StockPicking, self).button_validate()
        # Only completed pickings are processed.
        self.filtered(lambda p: p.state == 'done').action_generate_serials_from_destination()
        return result
