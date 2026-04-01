
from odoo import models, fields, api

class ResPartner(models.Model):
    _inherit = 'res.partner'

    has_missing_info = fields.Boolean(
        string="Missing Info",
        compute="_compute_missing_info",
        store=True
    )

    @api.depends(
        'year','college','department','student_type','shift','level',
        'stage_id','number_of_years','college_number','batch','register_date',
        'passport_number','gender','nationalty','year_born','phone','mobile','email',
        'State_of_birth','ID_number','ID_issue_Date','place_of_issuance','Marital_status',
        'academic_branch','year_of_graduation','final_result','year_of_acceptance',
        'Round_of_Passing','name_of_school_graduated_from_1',
        'State_of_school_graduated_from_1','institute'
    )
    def _compute_missing_info(self):
        for rec in self:

            fields_to_check = [
                rec.year, rec.college, rec.department, rec.student_type,
                rec.shift, rec.level, rec.stage_id, rec.number_of_years,
                rec.college_number, rec.batch, rec.register_date,
                rec.passport_number, rec.gender, rec.nationalty,
                rec.year_born, rec.phone, rec.mobile, rec.email,
                rec.State_of_birth, rec.ID_number, rec.ID_issue_Date,
                rec.place_of_issuance, rec.Marital_status,
                rec.academic_branch, rec.year_of_graduation,
                rec.final_result, rec.year_of_acceptance,
                rec.Round_of_Passing,
                rec.name_of_school_graduated_from_1,
                rec.State_of_school_graduated_from_1,
                rec.institute
            ]

            rec.has_missing_info = any(not field for field in fields_to_check)
