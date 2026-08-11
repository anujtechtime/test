# -*- coding: utf-8 -*-
from odoo import models, fields, api


class StockLocation(models.Model):
    _inherit = 'stock.location'

    prefix_code = fields.Char(
        string='Prefix Code',
        copy=False,
        index=True,
        help='Prefix for this location. The full location prefix is built from the '
             'configured prefixes in the parent location path.',
    )

    @api.multi
    def get_serial_prefix(self):
        """Return the concatenated prefix for the complete location path.

        Example:
            Warehouse/N/F/5 with prefixes N/F/5 -> NF5
        Empty prefixes are ignored. The current location is included.
        """
        self.ensure_one()
        parts = []
        current = self
        while current:
            if current.prefix_code:
                parts.append(current.prefix_code.strip())
            current = current.location_id
        parts.reverse()
        return ''.join(parts)
