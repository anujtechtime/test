###################################################################################
#
#    Copyright (c) 2017-2019 MuK IT GmbH.
#
#    This file is part of MuK Documents Thumbnails 
#    (see https://mukit.at).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Lesser General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Lesser General Public License for more details.
#
#    You should have received a copy of the GNU Lesser General Public License
#    along with this program. If not, see <http://www.gnu.org/licenses/>.
#
###################################################################################

from odoo import api, fields, models, _

class ResConfigSettings(models.TransientModel):
    
    _inherit = 'res.config.settings'
    
    #----------------------------------------------------------
    # Functions
    #----------------------------------------------------------
    
    
    def documents_open_thumbnail_cron(self):
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'ir.cron',
            'view_type': 'form',
            'view_mode': 'tree,form',
            'name': _("Automatic Thumbnail Creation"),
            'res_id': self.env.ref('muk_dms_thumbnails.cron_dms_file_thumbnails').id,
            'views': [(False, "form")],
            'context': self.env.context,
        }  
