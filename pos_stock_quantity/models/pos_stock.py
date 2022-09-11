# -*- coding: utf-8 -*-

from odoo import api, fields, models
from collections import deque


# class StockQuantity(models.Model):
#     _inherit = 'stock.quant'

    # @api.model
    # def get_qty_available(self, location_id, location_ids=None, product_ids=None):
    #     if location_id:
    #         root_location = self.env['stock.location'].search([('id', '=', location_id)])
    #         all_location = [root_location.id]
    #         queue = deque([])
    #         self.location_traversal(queue, all_location, root_location)
    #         stock_quant = self.search_read([('location_id', 'in', all_location)], ['product_id', 'qty', 'location_id'])
    #         return stock_quant
    #     else:
    #         stock_quant = self.search_read([('location_id', 'in', location_ids), ('product_id', 'in', product_ids)],
    #                                        ['product_id', 'qty', 'location_id'])
    #         return stock_quant

    # def location_traversal(self, queue, res, root):
    #     for child in root.child_ids:
    #         if child.usage == 'internal':
    #             queue.append(child)
    #             res.append(child.id)
    #     while queue:
    #         pick = queue.popleft()
    #         res.append(pick.id)
    #         self.location_traversal(queue, res, pick)

    # @api.model
    # def create(self, vals):
    #     res = super(StockQuantity, self).create(vals)
    #     # if res.location_id.usage == 'internal':
    #     #     self.env['pos.stock.channel'].broadcast(res)
    #     return res

    # def write(self, vals):
    #     # record = self.filtered(lambda x: x.location_id.usage == 'internal')
    #     # self.env['pos.stock.channel'].broadcast(record)
    #     return super(StockQuantity, self).write(vals)



class PosConfig(models.Model):
    _inherit = "pos.config"

    show_qty_available = fields.Boolean(string='Display Stock in POS', related='company_id.show_qty_available', readonly=False)
    location_only = fields.Boolean(string='Only in POS Location', related='company_id.location_only',readonly=False)
    allow_out_of_stock = fields.Boolean(string='Allow Out-of-Stock', related='company_id.allow_out_of_stock', readonly=False)
    limit_qty = fields.Integer(string='Deny Order when Quantity Available lower than', related='company_id.limit_qty', readonly=False)
    hide_product = fields.Boolean(string='Hide Products not in POS Location', related='company_id.hide_product', readonly=False)

class PosConfigCompany(models.Model):
    _inherit = 'res.company'

    show_qty_available = fields.Boolean(string='Display Stock in POS')
    location_only = fields.Boolean(string='Only in POS Location')
    allow_out_of_stock = fields.Boolean(string='Allow Out-of-Stock')
    limit_qty = fields.Integer(string='Deny Order when Quantity Available lower than')
    hide_product = fields.Boolean(string='Hide Products not in POS Location')    


class PosStockChannel(models.Model):
    _inherit = 'pos.payment.method'

    currency_id = fields.Many2one('res.currency', string="Currency")

class PosOrderReportInherit(models.Model):
    _inherit = "report.pos.order"

    cost_price = fields.Float(string='Cost Price', readonly=True)
    profit_total = fields.Float(string="Profit", readonly=True)

    def _select(self):
        return """
            SELECT
                MIN(l.id) AS id,
                COUNT(*) AS nbr_lines,
                s.date_order AS date,
                SUM(l.qty) AS product_qty,
                SUM(l.qty * l.price_unit / CASE COALESCE(s.currency_rate, 0) WHEN 0 THEN 1.0 ELSE s.currency_rate END) AS price_sub_total,
                SUM((l.qty * l.price_unit) * (100 - l.discount) / 100 / CASE COALESCE(s.currency_rate, 0) WHEN 0 THEN 1.0 ELSE s.currency_rate END) AS price_total,

                SUM(l.qty * h.value_float) AS cost_price,
                SUM((l.qty * l.price_unit) - (l.qty * h.value_float)) AS profit_total,

                SUM((l.qty * l.price_unit) * (l.discount / 100) / CASE COALESCE(s.currency_rate, 0) WHEN 0 THEN 1.0 ELSE s.currency_rate END) AS total_discount,
                (SUM(l.qty*l.price_unit / CASE COALESCE(s.currency_rate, 0) WHEN 0 THEN 1.0 ELSE s.currency_rate END)/SUM(l.qty * u.factor))::decimal AS average_price,
                SUM(cast(to_char(date_trunc('day',s.date_order) - date_trunc('day',s.create_date),'DD') AS INT)) AS delay_validation,
                s.id as order_id,
                s.partner_id AS partner_id,
                s.state AS state,
                s.user_id AS user_id,
                s.location_id AS location_id,
                s.company_id AS company_id,
                s.sale_journal AS journal_id,
                l.product_id AS product_id,
                pt.categ_id AS product_categ_id,
                p.product_tmpl_id,
                ps.config_id,
                pt.pos_categ_id,
                s.pricelist_id,
                s.session_id,
                s.account_move IS NOT NULL AS invoiced
        """

    def _from(self):
        return """
            FROM pos_order_line AS l
                INNER JOIN pos_order s ON (s.id=l.order_id)
                LEFT JOIN product_product p ON (l.product_id=p.id)
                LEFT JOIN product_template pt ON (p.product_tmpl_id=pt.id)
                LEFT JOIN ir_property h ON (h.res_id=CONCAT('product.product,', CAST(p.id AS varchar)))
                LEFT JOIN uom_uom u ON (u.id=pt.uom_id)
                LEFT JOIN pos_session ps ON (s.session_id=ps.id)
        """

