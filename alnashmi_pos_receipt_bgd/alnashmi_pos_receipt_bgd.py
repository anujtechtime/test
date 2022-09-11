# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo import SUPERUSER_ID
from odoo.exceptions import UserError
from odoo.tools.float_utils import float_compare, float_is_zero, float_round

from odoo.http import request

class IrQWeb(models.AbstractModel):
    _inherit = 'ir.qweb'

    @api.model
    def render(self, id_or_xml_id, values=None, **options):
        values = values or {}
        context = dict(self.env.context, **options)
        if 'receipt_gold' in values:
            return super(IrQWeb, self).render(id_or_xml_id, values=values, **options)
        uid = self.sudo()._uid
        values['receipt_gold'] = 0
        for pos_session_obj in self.sudo().env['pos.session'].search([('state', '=', 'opened'), ('user_id', '=', uid)], order='id desc', limit=1):
	        if pos_session_obj.config_id.name == "GOLD":
	        	values['receipt_gold'] = 1
        return super(IrQWeb, self).render(id_or_xml_id, values=values, **options)

# class View(models.Model):

#     _inherit = "ir.ui.view"

#     @api.multi
#     def render(self, values=None, engine='ir.qweb'):
#         """ Render the template. If website is enabled on request, then extend rendering context with website values. """
#         qcontext = self._prepare_qcontext()
#         if values:
#             qcontext.update(values)

#         uid = self._uid
#         qcontext['receipt_gold'] = 0
#         pos_session = self.env['pos.session'].search([('state', '=', 'opened'), ('user_id', '=', uid)])
#         if pos_session.config_id.name == "GOLD":
#             qcontext['receipt_gold'] = 1
#         values = qcontext
#         return super(View, self).render(values, engine=engine)

class alnashmi_customer_birthday(models.Model):
    _inherit = "res.partner"

    h_birthday = fields.Date(string='H. Birthday', translate=True)
    w_birthday = fields.Date(string='W. Birthday', translate=True)
    h_day = fields.Integer(string='H Day')
    h_month = fields.Integer(string='H Month')
    h_year = fields.Integer(string='H Year')
    w_day = fields.Integer(string='W. Day')
    w_month = fields.Integer(string='W. Month')
    w_year = fields.Integer(string='W. Year')

    @api.model
    def create(self, values):
        if 'h_birthday' in values:
            if values['h_birthday']:
                h_birthday = values['h_birthday']
                h_birthday_arr = h_birthday.split("-")
                values['h_day'] = h_birthday_arr[2]
                values['h_month'] = h_birthday_arr[1]
                values['h_year'] = h_birthday_arr[0]

        if 'w_birthday' in values:
            if values['w_birthday']:
                w_birthday = values['w_birthday']
                w_birthday_arr = w_birthday.split("-")
                values['w_day'] = w_birthday_arr[2]
                values['w_month'] = w_birthday_arr[1]
                values['w_year'] = w_birthday_arr[0]
        return super(alnashmi_customer_birthday, self).create(values)

    def write(self, values):
        if 'h_birthday' in values:
            if values['h_birthday']:
                h_birthday = values['h_birthday']
                h_birthday_arr = h_birthday.split("-")
                values['h_day'] = h_birthday_arr[2]
                values['h_month'] = h_birthday_arr[1]
                values['h_year'] = h_birthday_arr[0]

        if 'w_birthday' in values:
            if values['w_birthday']:
                w_birthday = values['w_birthday']
                w_birthday_arr = w_birthday.split("-")
                values['w_day'] = w_birthday_arr[2]
                values['w_month'] = w_birthday_arr[1]
                values['w_year'] = w_birthday_arr[0]
        return super(alnashmi_customer_birthday, self).write(values)




class PickingStock(models.Model):
    _inherit = "stock.picking"



    state = fields.Selection([
        ('draft', 'Draft'),
        ('waiting', 'Waiting Another Operation'),
        ('confirmed', 'Waiting'),
        ('assigned', 'Ready'),
        ('allow_transfer', 'Transfer Request'),
        ('done', 'Done'),
        ('cancel', 'Cancelled'),
    ], string='Status', compute='_compute_state',
        copy=False, index=True, readonly=True, store=True, tracking=True,
        help=" * Draft: The transfer is not confirmed yet. Reservation doesn't apply.\n"
             " * Waiting another operation: This transfer is waiting for another operation before being ready.\n"
             " * Waiting: The transfer is waiting for the availability of some products.\n(a) The shipping policy is \"As soon as possible\": no product could be reserved.\n(b) The shipping policy is \"When all products are ready\": not all the products could be reserved.\n"
             " * Ready: The transfer is ready to be processed.\n(a) The shipping policy is \"As soon as possible\": at least one product has been reserved.\n(b) The shipping policy is \"When all products are ready\": all product have been reserved.\n"
             " * Done: The transfer has been processed.\n"
             " * Cancelled: The transfer has been cancelled.")


    def allow_transfer(self):
        self.update({
            'state': 'allow_transfer'
            })    

    def button_validate(self):
        self.ensure_one()
        if not self.move_lines and not self.move_line_ids:
            raise UserError(_('Please add some items to move.'))

        # Clean-up the context key at validation to avoid forcing the creation of immediate
        # transfers.
        ctx = dict(self.env.context)
        ctx.pop('default_immediate_transfer', None)
        self = self.with_context(ctx)

        # add user as a follower
        self.message_subscribe([self.env.user.partner_id.id])

        # If no lots when needed, raise error
        picking_type = self.picking_type_id
        precision_digits = self.env['decimal.precision'].precision_get('Product Unit of Measure')
        no_quantities_done = all(float_is_zero(move_line.qty_done, precision_digits=precision_digits) for move_line in self.move_line_ids.filtered(lambda m: m.state not in ('done', 'cancel')))
        no_reserved_quantities = all(float_is_zero(move_line.product_qty, precision_rounding=move_line.product_uom_id.rounding) for move_line in self.move_line_ids)
        if no_reserved_quantities and no_quantities_done:
            raise UserError(_('You cannot validate a transfer if no quantites are reserved nor done. To force the transfer, switch in edit more and encode the done quantities.'))

        if picking_type.use_create_lots or picking_type.use_existing_lots:
            lines_to_check = self.move_line_ids
            if not no_quantities_done:
                lines_to_check = lines_to_check.filtered(
                    lambda line: float_compare(line.qty_done, 0,
                                               precision_rounding=line.product_uom_id.rounding)
                )

            for line in lines_to_check:
                product = line.product_id
                if product and product.tracking != 'none':
                    if not line.lot_name and not line.lot_id:
                        raise UserError(_('You need to supply a Lot/Serial number for product %s.') % product.display_name)
           

        if self.show_operations:
            for cost in self:
                move = self.env['account.move']
                move_vals = {
                    'journal_id': cost.move_line_ids_without_package.product_id.categ_id.property_stock_journal.id,
                    'date': cost.date,
                    'ref': cost.name,
                    'name': cost.name,
                    'line_ids': [],
                    'type': 'entry',
                }
                valuation_layer_ids = []

                for lines in self.move_line_ids_without_package:
                    cost_to_add = lines.product_id.standard_price * lines.qty_done
                    valuation_layer = self.env['stock.valuation.layer'].create({
                                'value': cost_to_add,
                                'unit_cost': lines.product_id.standard_price,
                                'quantity': lines.qty_done,
                                'remaining_qty': 0,
                                'stock_valuation_layer_id': self.move_lines.stock_valuation_layer_ids.ids,
                                'description': cost.name,
                                'stock_move_id': self.move_lines.id,
                                'product_id': lines.product_id.id,
                                'company_id': cost.company_id.id,
                            })
                    # account_line = self.env['account.move.line'].sudo().create({
                    #     'account_id' : cost.location_id.valuation_out_account_id.id,
                    #     'partner_id' : cost.partner_id.id,
                    #     'quantity' : lines.qty_done,
                    #     'date' : cost.date,
                    #     'move_id' : move.id,
                    #     'name' : cost.name,
                    #     'debit' : cost_to_add
                    #     })
                    # account_line1 = self.env['account.move.line'].sudo().create({
                    #     'account_id' : cost.location_dest_id.valuation_in_account_id.id,
                    #     'partner_id' : cost.partner_id.id,
                    #     'quantity' : lines.qty_done,
                    #     'date' : cost.date,
                    #     'move_id' : move.id,
                    #     'name' : cost.name,
                    #     'debit' : 0,
                    #     'credit' : cost_to_add,
                    #     })
                    valuation_layer_ids.append(valuation_layer.id)
                    move_vals['line_ids'] =  self._create_account_move_line(move, cost.location_dest_id.valuation_in_account_id.id, cost.location_id.valuation_out_account_id.id, lines.qty_done, cost.location_id.valuation_out_account_id.id , lines.product_id.standard_price)
                    move_vals['stock_valuation_layer_ids'] = [(6, 0, valuation_layer_ids)]
                    move = move.create(move_vals)  
                    self.move_lines.write({'state': 'done', 'account_move_ids': [(6, 0, move.id)], 'quantity_done' : lines.product_uom_qty, 'product_uom_qty': lines.product_uom_qty})
                    move.post()


        if not self.show_operations:
            landed_cost = self.env['stock.landed.cost']
            lc_id = landed_cost. create({
                'name': "LC/" + self.name,
                'picking_ids' : [(4, self.id ,0)],
                'account_journal_id' : self.env.company.lc_journal_id.id
                })

            labour_products = self.env['product.product'].search([('landed_cost_ok','=',True),('name','=','labour cost')])
            shipping_products = self.env['product.product'].search([('landed_cost_ok','=',True),('name','=','shipping cost')])
            valuation_in_account_id = self.env['res.config.settings'].search([],limit=1)
            total_cost = self.shipping_cost + self.labour_cost 

            if shipping_products:
                lc_id.cost_lines.create({
                    'name' : shipping_products.name,
                    'cost_id' : lc_id.id,
                    'product_id' : shipping_products.id,
                    'price_unit' : self.shipping_cost,
                    'split_method' : 'equal',
                    'account_id' : valuation_in_account_id.valuation_in_account_id.id
                    })
            if  labour_products:
                 lc_id.cost_lines.create({
                    'name' : shipping_products.name,
                    'cost_id' : lc_id.id,
                    'product_id' : labour_products.id,
                    'price_unit' : self.labour_cost,
                    'split_method' : 'equal',
                    'account_id' : valuation_in_account_id.valuation_in_account_id.id
                    })

            # lc_id.button_validate()  
            self.update({
                'stock_lanaded_cost' : lc_id.id
                })

        # Propose to use the sms mechanism the first time a delivery
        # picking is validated. Whatever the user's decision (use it or not),
        # the method button_validate is called again (except if it's cancel),
        # so the checks are made twice in that case, but the flow is not broken
        sms_confirmation = self._check_sms_confirmation_popup()
        if sms_confirmation:
            return sms_confirmation

        if no_quantities_done:
            view = self.env.ref('stock.view_immediate_transfer')
            wiz = self.env['stock.immediate.transfer'].create({'pick_ids': [(4, self.id)]})
            return {
                'name': _('Immediate Transfer?'),
                'type': 'ir.actions.act_window',
                'view_mode': 'form',
                'res_model': 'stock.immediate.transfer',
                'views': [(view.id, 'form')],
                'view_id': view.id,
                'target': 'new',
                'res_id': wiz.id,
                'context': self.env.context,
            }

        

        if self._get_overprocessed_stock_moves() and not self._context.get('skip_overprocessed_check'):
            view = self.env.ref('stock.view_overprocessed_transfer')
            wiz = self.env['stock.overprocessed.transfer'].create({'picking_id': self.id})
            return {
                'type': 'ir.actions.act_window',
                'view_mode': 'form',
                'res_model': 'stock.overprocessed.transfer',
                'views': [(view.id, 'form')],
                'view_id': view.id,
                'target': 'new',
                'res_id': wiz.id,
                'context': self.env.context,
            }

        # Check backorder should check for other barcodes
        if self._check_backorder():
            return self.action_generate_backorder_wizard()
        self.action_done()
        return

    def _create_account_move_line(self, move, credit_account_id, debit_account_id, qty_out, already_out_account_id, cost):
        """
        Generate the account.move.line values to track the landed cost.
        Afterwards, for the goods that are already out of stock, we should create the out moves
        """
        AccountMoveLine = []

        base_line = {
            'name': self.name,
            'product_id': self.product_id.id,
            'quantity': 0,
        }
        debit_line = dict(base_line, account_id=debit_account_id)
        credit_line = dict(base_line, account_id=credit_account_id)
        diff = cost
        if diff > 0:
            debit_line['debit'] = diff
            credit_line['credit'] = diff
        else:
            # negative cost, reverse the entry
            debit_line['credit'] = -diff
            credit_line['debit'] = -diff
        AccountMoveLine.append([0, 0, debit_line])
        AccountMoveLine.append([0, 0, credit_line])

        # Create account move lines for quants already out of stock
        if qty_out > 0:
            debit_line = dict(base_line,
                              name=(self.name + ": " + str(qty_out) + _(' already out')),
                              quantity=0,
                              account_id=already_out_account_id)
            credit_line = dict(base_line,
                               name=(self.name + ": " + str(qty_out) + _(' already out')),
                               quantity=0,
                               account_id=debit_account_id)
            diff = diff * qty_out
            if diff > 0:
                debit_line['debit'] = diff
                credit_line['credit'] = diff
            else:
                # negative cost, reverse the entry
                debit_line['credit'] = -diff
                credit_line['debit'] = -diff
            AccountMoveLine.append([0, 0, debit_line])
            AccountMoveLine.append([0, 0, credit_line])

            if self.env.company.anglo_saxon_accounting:
                expense_account_id = self.product_id.product_tmpl_id.get_product_accounts()['expense'].id
                debit_line = dict(base_line,
                                  name=(self.name + ": " + str(qty_out) + _(' already out')),
                                  quantity=0,
                                  account_id=expense_account_id)
                credit_line = dict(base_line,
                                   name=(self.name + ": " + str(qty_out) + _(' already out')),
                                   quantity=0,
                                   account_id=already_out_account_id)

                if diff > 0:
                    debit_line['debit'] = diff
                    credit_line['credit'] = diff
                else:
                    # negative cost, reverse the entry
                    debit_line['credit'] = -diff
                    credit_line['debit'] = -diff
                AccountMoveLine.append([0, 0, debit_line])
                AccountMoveLine.append([0, 0, credit_line])

        return AccountMoveLine



class StockQuantIds(models.Model):
    _inherit = 'stock.quant'      

    @api.model
    def action_view_quants_active_ids(self): 
        res = self.env['stock.quant'].search([])
        location_name = self.env['stock.location'].search([])
        domain_loc = self.env['product.product']._get_domain_locations()[0]
        quant_ids = self.env['stock.quant'].search([('location_id.usage','=', 'internal')])
        dct = []
        for location in location_name:
            quant_ids = self.env['stock.quant'].search([('location_id.usage','=', 'internal')]).filtered(lambda x: x.location_id.id == location.id)
            for i in quant_ids.mapped('id'):
                dct.append(i)
        return dct  






#     property_stock_account_input_categ_id = fields.Many2one(
#         'account.account', 'Stock Input Account', company_dependent=True,
#         domain="[('deprecated', '=', False)]", check_company=True,
#         help="""When doing automated inventory valuation, counterpart journal items for all incoming stock moves will be posted in this account,
#                 unless there is a specific valuation account set on the source location. This is the default value for all products in this category.
#                 It can also directly be set on each product.""")
#     property_stock_account_output_categ_id = fields.Many2one(
#         'account.account', 'Stock Output Account', company_dependent=True,
#         domain="[('deprecated', '=', False)]", check_company=True,
#         help="""When doing automated inventory valuation, counterpart journal items for all outgoing stock moves will be posted in this account,
#                 unless there is a specific valuation account set on the destination location. This is the default value for all products in this category.
#                 It can also directly be set on each product.""")
#     property_stock_valuation_account_id = fields.Many2one(
#         'account.account', 'Stock Valuation Account', company_dependent=True,
#         domain="[('company_id', '=', allowed_company_ids[0]), ('deprecated', '=', False)]", check_company=True,
#         help="""When automated inventory valuation is enabled on a product, this account will hold the current value of the products.""",)
