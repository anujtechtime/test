# -*- coding: utf-8 -*-

from odoo import models, fields, api
import json


class FxThemeStyle(models.Model):
    '''
    user theme style setting
    '''
    _name = 'fx_theme.theme_style'
    _description = 'theme style'

    def _default_sequence(self):
        return self.env['ir.sequence'].next_by_code('fx_theme.theme_style')

    name = fields.Char(string="style name", required=True)
    theme_mode = fields.Many2one(comodel_name="fx_theme.theme_mode", string="theme mode")
    sequence = fields.Integer(string="mode sequence", default=_default_sequence)
    deletable = fields.Boolean(string="deletable", default=True)
    style_items = fields.One2many(
        string="style items",
        comodel_name="fx_theme.style_item",
        inverse_name="theme_style")

    def get_styles(self):
        '''
        get mode datas
        :return:
        '''
        results = []
        for record in self:
            result = record.read()[0]
            result["style_items"] = record.style_items.read()
            for style_item in record.style_items:
                if 'identity' in style_item and style_item['identity'] != '':
                    result[style_item['identity']] = style_item['val']
            style_item_group = dict()
            for style_item in result["style_items"]:
                style_item_group.setdefault(style_item['group'], []).append(style_item)
            result['groups'] = style_item_group
            results.append(result)
        return results

    @api.model
    def delete_style(self, style_id):
        '''
        delete styel of user
        :return:
        '''
        record = self.search([('id', '=', style_id)])
        record.unlink()

    def check_style_item_data(self, theme_style_data):
        '''
        check style item data
        :return:
        '''
        self.ensure_one()
        default_style_items = theme_style_data['style_items']
        style_item_cache = {style_item.name: style_item for style_item in self.style_items}

        default_style_item_cache = dict()
        for default_style_item in default_style_items:
            # may be the user change the color, so we can not update it
            style_item_name = default_style_item["name"]
            default_style_item_cache[style_item_name] = default_style_item
            if style_item_name not in style_item_cache:
                default_style_item["theme_style"] = self.id
                default_style_item["css_info"] = json.dumps(default_style_item["css_info"])
                self.env['fx_theme.style_item'].create(default_style_item)
            else:
                # update the style item
                tmp_style_item = style_item_cache[style_item_name]
                tmp_style_item.write({
                    "group": default_style_item.get("group", False),
                    "identity": default_style_item.get("identity", False),
                    "css_info": json.dumps(default_style_item["css_info"]),
                })
        # delete the style item
        for style_item_name in style_item_cache:
            if style_item_name not in default_style_item_cache:
                style_item_cache[style_item_name].unlink()


class StyleItem(models.Model):
    '''
    user theme style setting
    '''
    _name = 'fx_theme.style_item'

    theme_style = fields.Many2one(string="theme style", comodel_name="fx_theme.theme_style")
    name = fields.Char(string="name", required=True)
    val = fields.Char(string="val", required=True)
    identity = fields.Char(string="identity")
    group = fields.Char(string="group", default="")
    css_info = fields.Text(string="css info", default="[]")
