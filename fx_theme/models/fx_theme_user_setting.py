# -*- coding: utf-8 -*-

from odoo import models, fields, api
from .fx_theme_default_data import default_modes, default_settings, version
import json


class FxThemeUserSetting(models.Model):
    '''
    user theme style setting
    '''
    _name = 'fx_theme.user_setting'
    _description = 'user setting'

    uid = fields.Many2one(string='user id')
    settings = fields.One2many(string="settings",
                               comodel_name="fx_theme.user_setting_item",
                               inverse_name="user_setting")
    theme_modes = fields.One2many(string="theme mode",
                                  comodel_name="fx_theme.theme_mode",
                                  inverse_name="user_setting")
    cur_mode = fields.Many2one(string="current style", comodel_name="fx_theme.theme_mode")
    version = fields.Char(string="version",  default='1.0.0.1')
    remark = fields.Text(string='remark')

    @api.model
    def get_style_create_data(self, style):
        '''
        get style create data
        :return:
        '''
        tmp_style_items = []
        style_items = style["style_items"]
        for style_item in style_items:
            tmp_style_items.append((0, 0, style_item))
        return (0, 0, {
            "name": style["name"],
            "style_items": tmp_style_items
        })

    @api.model
    def get_setting_data(self):
        '''
        get setting data
        :return:
        '''
        data = []
        for key in default_settings.keys():
            data.append((0, 0, {
                "name": key,
                "val": default_settings[key]
            }))
        return data

    @api.model
    def save_setting(self, data):
        print("data@@@@@@@@@@@@@@@@@@@@@@@@@@@@",data)
        '''
        save setting
        :return:
        '''
        # user_setting = self.search([('uid', '=', self.env.uid)])
        # user_setting.ensure_one()
        # mode_id = data['mode_id']
        # user_setting.cur_mode = int(mode_id)
        # style_items = data['style_items']
        # mode = user_setting.theme_modes
        # mode.ensure_one()
        # style_id = data["style_id"]
        # mode.cur_style = style_id
        # # update the style item color
        # theme_style = mode.theme_styles.filtered(lambda tmp_style: tmp_style.id == style_id)
        # style_item_cache = {style_item.id: style_item for style_item in theme_style.style_items}
        # for style_item in style_items:
        #     item_id = style_item["id"]
        #     color = style_item["color"]
        #     temp_style_item = style_item_cache.get(item_id, None)
        #     if temp_style_item:
        #         temp_style_item.val = color
        # new_style = theme_style

        # # update the user setting
        # setting_data = data["setting_data"]
        # setting_cache = {setting.name: setting for setting in user_setting.settings}
        # for name in setting_data:
        #     if name in setting_cache:
        #         setting_cache[name].val = setting_data[name]
        #     else:
        #         # create a new setting item
        #         self.env['fx_theme.user_setting_item'].create([{
        #             "user_setting": user_setting.id,
        #             "name": name,
        #             "val": setting_data[name]
        #         }])
        # style_data = new_style.get_styles()[0]
        # return style_data

    @api.model
    def check_data(self):
        '''
         check if the data is not full
        :return:
        '''
        records = self.search([('uid', '=', self.env.uid)])
        if not records:
            records = self.create([{
                "uid": self.env.uid,
                "settings": self.get_setting_data(),
            }])
        records.ensure_one()
        records.check_setting_data()
        records.check_default_mode_data()

    def create_mode(self, model_data):
        '''
        create mode
        :param model_data:
        :param user_setting:
        :return:
        '''
        theme_styles = model_data['theme_styles']
        theme_style_array = []
        for theme_style in theme_styles:
            style_items = theme_style["style_items"]
            item_val_array = []
            for style_item in style_items:
                item_val_array.append((0, 0, {
                    "name": style_item["name"],
                    "css_info": json.dumps(style_item["css_info"]),
                    "val": style_item["val"],
                    "group": style_item.get("group", False),
                    "identity": style_item.get("identity", False)
                }))
            theme_style_array.append((0, 0, {
                "name": theme_style["name"],
                "deletable": theme_style["deletable"],
                "style_items": item_val_array
            }))
        self.env["fx_theme.theme_mode"].create([{
            "user_setting": self.id,
            "theme_styles": theme_style_array,
            "version": version
        }])

    def check_setting_data(self):
        '''
        check the setting data
        :return:
        '''
        self.ensure_one()
        setting = self.settings
        names = setting.mapped('name')
        val_array = []
        for name in default_settings:
            if name not in names:
                val_array.append((0, 0, {
                    "name": name,
                    "val": default_settings[name],
                }))
        self.settings = val_array

    def check_default_mode_data(self):
        '''
        check default mode data
        :return:
        '''
        self.ensure_one()
        mode_names = self.theme_modes.mapped('name')
        for model_name in default_modes:
            if model_name not in mode_names:
                default_mode = default_modes[model_name]
                self.create_mode(default_mode)
        for theme_mode in self.theme_modes:
            if theme_mode.version == version:
                continue
            theme_mode.check_mode_data()
            theme_mode.version = version

    @api.model
    def get_user_setting(self, get_mode_data=True):
        '''
        get user setting
        :return:
        '''
        self.check_data()

        uid = self.env.user.id
        record = self.sudo().search([('uid', '=', uid)])
        if not record.cur_mode:
            record.cur_mode = record.theme_modes[0].id

        rst = record.read()[0]
        if get_mode_data:
            rst['theme_modes'] = record.theme_modes.get_mode_data()
        rst['settings'] = record.settings.read()
        rst['default_modes'] = default_modes
        rst['cur_mode'] = record.cur_mode.id

        return rst

    @api.model
    def update_cur_style(self, style_id):
        '''
        update user cur mode
        :return:
        '''
        uid = self.env.uid
        record = self.sudo().search([('uid', '=', uid)])
        if record:
            record.cur_style = style_id


class FxUserSettingItem(models.Model):
    '''
    user theme style setting
    '''
    _name = 'fx_theme.user_setting_item'

    user_setting = fields.Many2one(string="user setting", comodel_name="fx_theme.user_setting")
    name = fields.Char(string="name")
    val = fields.Text(string="val")
    remark = fields.Text(string='remark')
