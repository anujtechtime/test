
# -*- coding: utf-8 -*-

from odoo import models, fields, api
from .fx_theme_default_data import default_modes, version


class FxThemeModes(models.Model):
    '''
    user theme style setting
    '''
    _name = 'fx_theme.theme_mode'
    _description = 'theme mode'

    def _default_sequence(self):
        return self.env['ir.sequence'].next_by_code('fx_theme.theme_mode')

    name = fields.Char(string="name")
    user_setting = fields.Many2one(string="user setting", comodel_name="fx_theme.user_setting")
    sequence = fields.Integer(string="mode sequence", default=_default_sequence)
    theme_styles = fields.One2many(string="theme styles",
                                   comodel_name="fx_theme.theme_style",
                                   inverse_name="theme_mode")
    cur_style = fields.Many2one(string="current style", comodel_name="fx_theme.theme_style")
    version = fields.Char(string="version")

    _sql_constraints = [('name_unique', 'UNIQUE(name)', "mode name can not duplicate")]

    def get_mode_data(self):
        '''
        get the mode data
        :return:
        '''
        rst = []
        for record in self:
            if not record.cur_style:
                record.cur_style = record.theme_styles[0].id
            tmp_data = record.read()[0]
            tmp_data['theme_styles'] = record.theme_styles.get_styles()
            tmp_data['cur_style'] = record.cur_style.id
            rst.append(tmp_data)

        return rst

    def check_mode_data(self):
        '''
        check the mode data
        :return:
        '''
        self.ensure_one()
        name = self.name
        theme_styles = self.theme_styles
        theme_style_cache = dict()
        for theme_style in theme_styles:
            theme_style_cache.setdefault(theme_style.name, []).append(theme_style)

        theme_style_names = theme_styles.mapped('name')
        default_mode = default_modes[name]
        default_theme_styles = default_mode['theme_styles']
        for default_theme_style in default_theme_styles:
            # if not have the style
            theme_style_name = default_theme_style['name']
            if theme_style_name not in theme_style_names:
                self.create_theme_style_from_default_data(default_theme_style)
            else:
                # check the style data, may be one more style with the same name
                theme_styles = theme_style_cache[theme_style_name] or []
                for theme_style in theme_styles:
                    theme_style.check_style_item_data(default_theme_style)

    def create_theme_style_from_default_data(self, theme_style):
        '''
        create theme style
        :return:
        '''
        self.ensure_one()
        style_items = theme_style['style_items']
        item_data = []
        for style_item in style_items:
            item_data.append((0, 0, style_item))
        return self.env['fx_theme.theme_style'].create({
            "name": theme_style["name"],
            "theme_mode": self.id,
            "deletable": theme_style["deletable"],
            "style_items": item_data
        })

    def add_new_style(self):
        '''
        add new style, get the first style as the default
        :return:
        '''
        theme_styles = self.theme_styles
        theme_style = theme_styles[0]
        theme_style_data = theme_style.copy_data()[0]
        theme_style_data["theme_mode"] = self.id
        theme_style_data["deletable"] = True
        val_array = []
        for style_item in theme_style.style_items:
            val = style_item.copy_data()[0]
            val_array.append((0, 0, val))
        theme_style_data['style_items'] = val_array
        theme_style = self.env["fx_theme.theme_style"].create(theme_style_data)
        style_data = theme_style.get_styles()[0]
        return style_data
