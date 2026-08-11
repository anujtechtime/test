# -*- coding: utf-8 -*-
from odoo import models, api

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
        for picking in self:
            if picking.state != 'done':
                continue
            for move_line in picking.move_line_ids:
                product = move_line.product_id
                if product.tracking != 'serial':
                    continue
                if move_line.lot_id:
                    continue
                location = move_line.location_dest_id
                prefix = self._get_serial_prefix(location, product)
                if not prefix:
                    continue
                serial_name = self._next_serial_name(prefix)
                lot = Lot.create({
                    'name': serial_name,
                    'product_id': product.id,
                    'company_id': picking.company_id.id,
                })
                move_line.lot_id = lot.id
        return True

    def button_validate(self):
        result = super(StockPicking, self).button_validate()
        # Only completed pickings are processed.
        self.filtered(lambda p: p.state == 'done').action_generate_serials_from_destination()
        return result
