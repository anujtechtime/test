# -*- coding: utf-8 -*-

from odoo import models, fields, api, _

class CertiPartner(models.Model):
	_inherit = "res.partner"

	grade = fields.Float("Grade")
	graduation_sequence = fields.Integer("Graduation Sequence")


class AlmaaqalCertificate(models.Model):
    _name = 'almaaqal.certificate'
    _description = 'Certificate'

    number = fields.Char("Number")
    date = fields.Date("Date")
    Status = fields.Selection([('draft','Draft'),('posted','Posted')], string="Status")

    type_d = fields.Selection([('arabic_no_grades','Arabic No Grades'),('english_no_grades','English No Grades'),('arabic_with_grades','Arabic with Grades'),('english_no_grades','English No Grades'),], string="Type") 

    # Student (Connected to student module: Partner)
    name_in_arabic =  fields.Many2one("res.partner", string="Name in Arabic")
    name_in_english = fields.Char("Name in English" , related="name_in_arabic.name_english")
    college = fields.Many2one("faculty.faculty", related="name_in_arabic.college")
    department = fields.Many2one("department.department", related="name_in_arabic.department")
    grade = fields.Float("Grade", related="name_in_arabic.grade")
    graduation_sequence = fields.Integer("Graduation Sequence", related="name_in_arabic.graduation_sequence")
    year_name_graduation_year = fields.Char("Year Name Graduation year" , related="name_in_arabic.year_of_collage_graduation")  
    notes = fields.Text("Notes", related="name_in_arabic.notes")

    grade_year = fields.Many2many("almaaqal.grade", string="Grade")



