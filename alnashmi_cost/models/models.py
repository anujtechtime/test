# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


# class alnashmi_cost(models.Model):
#     _name = 'alnashmi_cost.alnashmi_cost'
#     _description = 'alnashmi_cost.alnashmi_cost'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100

class Picking(models.Model):
    _inherit = "stock.picking"

    stock_landed_cost = fields.Many2one('stock.landed.cost', string="Landed Cost")
    labour_cost = fields.Float("Labour Cost")
    shipping_cost = fields.Float("Shipping Cost")



    def button_validate(self):
        line = super(Picking, self).button_validate()
        if not self.show_operations:
            for cost in self:
                move = self.env['account.move'].search([])
                move_vals = {
                    'journal_id': cost.move_line_ids_without_package.product_id.categ_id.property_stock_journal.id,
                    'date': cost.date,
                    'ref': cost.name,
                    'name': cost.name,
                    'line_ids': [],
                    'type': 'entry',
                }
                valuation_layer_ids = []

                valuation_in_account_id = self.env['res.config.settings'].search([],limit=1)
                total_cost = self.shipping_cost + self.labour_cost
                move_vals_total =  self._create_account_move_line(move, valuation_in_account_id.valuation_in_account_id.id, valuation_in_account_id.valuation_out_account_id.id, 0, valuation_in_account_id.valuation_out_account_id.id , total_cost)
                valuation_layer = self.env['stock.valuation.layer'].create({
                            'value': total_cost,
                            'unit_cost': total_cost,
                            'quantity': 1,
                            'remaining_qty': 0,
                            'stock_valuation_layer_id': self.move_lines.stock_valuation_layer_ids.ids,
                            'description': cost.name,
                            'stock_move_id': self.move_lines.id,
                            'product_id': self.move_line_ids_without_package.product_id.id,
                            'company_id': cost.company_id.id,
                        })
                valuation_layer_ids.append(valuation_layer.id)
                move_vals['line_ids'] =  self._create_account_move_line(move, valuation_in_account_id.valuation_in_account_id.id, valuation_in_account_id.valuation_out_account_id.id, 0, valuation_in_account_id.valuation_out_account_id.id , total_cost)
                move_vals['stock_valuation_layer_ids'] = [(6, 0, valuation_layer_ids)]
                print("move_vals@@@@@@@@@@@@@@@@@@@@",move_vals)
                move = move.create(move_vals)  
                self.move_lines.write({'state': 'done', 'account_move_ids': [(6, 0, move.id)], 'quantity_done' : 1, 'product_uom_qty': 1})
                move.post()
        return line


class PickingCost(models.Model):
    _inherit = "purchase.order.line"

    labour_cost = fields.Float("Labour Cost")
    shipping_cost = fields.Float("Shipping Cost")


class PickingCostLine(models.Model):
    _inherit = "purchase.order"

    @api.depends('order_line.price_total')
    def _amount_all(self):
        for order in self:
            amount_untaxed = amount_tax = 0.0
            for line in order.order_line:
                line.price_subtotal = line.labour_cost + line.shipping_cost + line.price_unit
                amount_untaxed += line.price_subtotal
                amount_tax += line.price_tax
            order.update({
                'amount_untaxed': order.currency_id.round(amount_untaxed),
                'amount_tax': order.currency_id.round(amount_tax),
                'amount_total': amount_untaxed + amount_tax,
            })    


    def button_confirm(self):
        labourcost = 0
        shipping_cost = 0
        for order in self:
            if order.state not in ['draft', 'sent']:
                continue
            order._add_supplier_to_product()
            # Deal with double validation process
            if order.company_id.po_double_validation == 'one_step'\
                    or (order.company_id.po_double_validation == 'two_step'\
                        and order.amount_total < self.env.company.currency_id._convert(
                            order.company_id.po_double_validation_amount, order.currency_id, order.company_id, order.date_order or fields.Date.today()))\
                    or order.user_has_groups('purchase.group_purchase_manager'):
                order.button_approve()
            else:
                order.write({'state': 'to approve'})
            for vals in order.order_line:
                labourcost += vals.labour_cost  
                shipping_cost += vals.shipping_cost 
            order.picking_ids.update({
                'labour_cost' : labourcost,
                'shipping_cost' : shipping_cost
            })    
        print("order@@@@@@@@@@@@@2###########3",self.picking_ids)          
        return True


class ResConfigSettingsValuation(models.TransientModel):
    _inherit = 'res.config.settings'


    valuation_in_account_id = fields.Many2one(
        'account.account', 'Stock Valuation Account (Incoming)',readonly=False,
        domain=[('internal_type', '=', 'other'), ('deprecated', '=', False)], related="company_id.valuation_in_account_id")
    valuation_out_account_id = fields.Many2one(
        'account.account', 'Stock Valuation Account (Outgoing)', readonly=False,
        domain=[('internal_type', '=', 'other'), ('deprecated', '=', False)], related="company_id.valuation_out_account_id")


class ResConfigCompany(models.Model):
    _inherit = 'res.company'


    valuation_in_account_id = fields.Many2one(
        'account.account', 'Stock Valuation Account (Incoming)',
        domain=[('internal_type', '=', 'other'), ('deprecated', '=', False)])
    valuation_out_account_id = fields.Many2one(
        'account.account', 'Stock Valuation Account (Outgoing)',
        domain=[('internal_type', '=', 'other'), ('deprecated', '=', False)])

