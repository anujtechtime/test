# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from datetime import date


class burj_module(models.Model):
    _inherit = 'purchase.order.line'

    finished_date = fields.Date("Finish Date")


    @api.onchange('finished_date', 'date_planned')
    def _onchange_finished_date(self):
        if self.finished_date and self.date_planned:
            print("date############################",(self.finished_date - self.date_planned.date()).days)
            self.product_qty = (self.finished_date - self.date_planned.date()).days
