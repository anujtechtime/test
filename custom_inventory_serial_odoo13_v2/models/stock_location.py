# -*- coding: utf-8 -*-
from odoo import models, fields, api

class StockLocation(models.Model):
    _inherit = 'stock.location'

    building_code = fields.Char(string='Building Code', copy=False)
    floor_code = fields.Char(string='Floor Code', copy=False)
    hall_code = fields.Char(string='Hall Code', copy=False)
    location_prefix = fields.Char(
        string='Location Prefix',
        compute='_compute_location_prefix',
        store=True,
        copy=False,
    )

    @api.depends('building_code', 'floor_code', 'hall_code', 'location_id')
    def _compute_location_prefix(self):
        for rec in self:
            parts = [
                (rec.building_code or '').strip(),
                (rec.floor_code or '').strip(),
                (rec.hall_code or '').strip(),
            ]
            # If explicit building/floor/hall codes are supplied on this location,
            # concatenate them in the requested order.
            prefix = ''.join(parts)
            rec.location_prefix = prefix or False
