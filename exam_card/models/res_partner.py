# from odoo import models, fields, api

# class ResPartner(models.Model):
#     _inherit = 'res.partner'

#     # Custom fields for student information
#     college_name = fields.Char(string='الكلية', help='College name')
#     department_name = fields.Char(string='القسم', help='Department name')
#     stage_name = fields.Char(string='المرحلة', help='Academic stage/year')
#     university_id = fields.Char(string='الرقم الجامعي', help='University ID number')
#     is_student = fields.Boolean(string='طالب', default=False, help='Check if this partner is a student')
#     student_birth_date = fields.Date(string='تاريخ الميلاد')
#     enrollment_date = fields.Date(string='تاريخ التسجيل')
#     student_photo = fields.Binary(string='الصورة', attachment=True)
    
#     @api.model
#     def name_search(self, name, args=None, operator='ilike', limit=100):
#         args = args or []
#         if name:
#             # Search by name or university_id
#             recs = self.search([
#                 '|',
#                 ('name', operator, name),
#                 ('university_id', operator, name)
#             ] + args, limit=limit)
#         else:
#             recs = self.search(args, limit=limit)
#         return recs.name_get()
    
#     def name_get(self):
#         result = []
#         for partner in self:
#             name = partner.name or ''
#             if partner.university_id:
#                 name = f"{partner.university_id} - {name}"
#             if partner.is_student:
#                 name = f"🎓 {name}"
#             result.append((partner.id, name))
#         return result