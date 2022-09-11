# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo import SUPERUSER_ID
from odoo.exceptions import UserError


class pos_session(models.Model):
    _inherit = 'pos.session'

    def get_on_hand_location(self, prodid):
        """ Display opened Session for logged user with Cash Register balance

        :param session_id: POS Open Session id .

        :return: Array of POS Session records.
        """
        print("prodid@@@@@@@@@@@@@@@@@",prodid)
        lists = {}
        guest = []
        location = self.env['stock.location'].search([('usage','=','internal')])
        for locs in location:
            print("locs55555555555555555555555555",locs)
            location_n = self.env['stock.quant'].search([('location_id','=',locs.id),('product_id','=',int(prodid))])
            print("location_n@@@@@@@@@@@@@@@@@",location_n)
            lists['oh_hand'] = location_n.id
            print("lists@@@@@@@@@@@@@@@",lists)
            print("guest@@@@@@@@@@@@@@@@",guest)
            guest.append(lists['oh_hand'])


        print("lists@@@@@@@@@@@@@@@@@@",lists)
        return guest


    def get_on_hand_location_onchange(self, location_name, productid):
        """ Display opened Session for logged user with Cash Register balance

        :param session_id: POS Open Session id .

        :return: Array of POS Session records.
        """
        print("location_name, productid@@@@@@@@@@@@@@@@@@@@@",location_name, productid)
        location_n = self.env['stock.quant'].search([('product_id','=',int(productid))])
        for loc in  location_n:
            print("loc.location_id.name@@@@@@@@@@@22222222222",loc.location_id.name, loc.location_id.id, loc.quantity)
            if loc.location_id.name == location_name:
                return loc.quantity


class PosOrder(models.Model):
    _inherit = "pos.order"

    @api.model
    def _process_order(self, order, draft, existing_order):
        """Create or update an pos.order from a given dictionary.

        :param pos_order: dictionary representing the order.
        :type pos_order: dict.
        :param draft: Indicate that the pos_order is not validated yet.
        :type draft: bool.
        :param existing_order: order to be updated or False.
        :type existing_order: pos.order.
        :returns number pos_order id
        """
        order = order['data']
        pos_session = self.env['pos.session'].browse(order['pos_session_id'])
        if pos_session.state == 'closing_control' or pos_session.state == 'closed':
            order['pos_session_id'] = self._get_valid_session(order).id

        pos_order = False
        print("order@@@@@@@@@@@@@@@@",order)
        order['name'] = self.env['ir.sequence'].next_by_code('self.service')
        if not existing_order:
            pos_order = self.create(self._order_fields(order))
        else:
            pos_order = existing_order
            pos_order.lines.unlink()
            order['user_id'] = pos_order.user_id.id
            pos_order.write(self._order_fields(order))

        self._process_payment_lines(order, pos_order, pos_session, draft)

        if not draft:
            try:
                pos_order.action_pos_order_paid()
            except psycopg2.DatabaseError:
                # do not hide transactional errors, the order(s) won't be saved!
                raise
            except Exception as e:
                _logger.error('Could not fully process the POS Order: %s', tools.ustr(e))

        if pos_order.to_invoice and pos_order.state == 'paid':
            pos_order.action_pos_order_invoice()

            
    # def set_location_for_inventory(self, location_name, configid):
    #     print("location_name@@@@@@@@@@@@@11111111111111111111111111111111@",location_name, configid)
    #     confd = self.env['pos.config'].search([('id','=',int(configid))], limit=1)
    #     print("conf@@@@@@@@@@@@@@@@@@@@@@@",confd)
    #     location = self.env['stock.location'].search([('usage','=','internal')])
    #     for  loc in location:
    #         if loc.name == location_name:
    #             print("self.config_id.picking_type_id@@@@@@@@@@@@@@@@@",self)
    #             print("loc@@@@@@@@@@@@@@###############",loc)
    #             confd.picking_type_id.update({
    #                 'default_location_src_id' : loc.id
    #                 })
    #             return loc.name