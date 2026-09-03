from odoo import models, fields, api
from odoo.exceptions import ValidationError

class ExamCardWizard(models.TransientModel):
    _name = 'exam.card.wizard'
    _description = 'Exam Card Print Wizard'

    # Partner selection
    partner_id = fields.Many2one(
        'res.partner', 
        string='الطالب',
        required=True,
        help='Select the student for the exam card'
    )
    
    exam_type = fields.Selection([
        ('الامتحانات النهائية', 'الامتحانات النهائية'),
        ('الفصل الأول', 'الفصل الأول'),
        ('الفصل الثاني', 'الفصل الثاني'),
        ('الامتحان التكميلي', 'الامتحان التكميلي')
    ], string='نوع الامتحان', default='الامتحانات النهائية', required=True)
    
    academic_year = fields.Many2one(
        'year.year',
        string='السنة الدراسية',
        default=lambda self: self.env['year.year'].search([], limit=1),
        required=True
    )
    
    # Auto-filled fields from partner
    student_name = fields.Char(
        string='الاسم',
        compute='_compute_partner_fields',
        store=False,
        readonly=True
    )
    college_name = fields.Char(
        string='الكلية',
        compute='_compute_partner_fields',
        store=False,
        readonly=True
    )
    department_name = fields.Char(
        string='القسم',
        compute='_compute_partner_fields',
        store=False,
        readonly=True
    )
    stage_name = fields.Char(
        string='المرحلة',
        compute='_compute_partner_fields',
        store=False,
        readonly=True
    )
    university_id = fields.Char(
        string='الرقم الجامعي',
        compute='_compute_partner_fields',
        store=False,
        readonly=True
    )

    # Manual override option
    allow_manual_edit = fields.Boolean(
        string='تعديل يدوي',
        default=False,
        help='Enable manual editing of student information'
    )
    
    manual_student_name = fields.Char(string='الاسم (يدوي)')
    manual_college_name = fields.Char(string='الكلية (يدوي)')
    manual_department_name = fields.Char(string='القسم (يدوي)')
    manual_stage_name = fields.Char(string='المرحلة (يدوي)')
    manual_university_id = fields.Char(string='الرقم الجامعي (يدوي)')

    @api.depends('partner_id')
    def _compute_partner_fields(self):
        """Auto-fill fields from partner data"""
        for record in self:
            if record.partner_id:
                record.student_name = record.partner_id.name or ''
                record.college_name = record.partner_id.college.college or ''
                record.department_name = record.partner_id.department.department or ''
                lev = record.partner_id.level
                if lev == 'leve1':
                    depp = 'المرحلة الاولى'
                if lev == 'level2':
                    depp = 'المرحلة الثانية'
                if lev == 'level3':
                    depp = 'المرحلة الثالثة'
                if lev == 'level4':
                    depp = 'المرحلة الرابعة'
                if lev == 'level5':
                    depp = 'المرحلة الخامسة'

                record.stage_name = depp or ''
                record.university_id = record.partner_id.college_number or ''
            else:
                record.student_name = ''
                record.college_name = ''
                record.department_name = ''
                record.stage_name = ''
                record.university_id = ''

    @api.onchange('allow_manual_edit')
    def _onchange_allow_manual_edit(self):
        """Reset manual fields when toggling manual edit"""
        if not self.allow_manual_edit:
            self.manual_student_name = False
            self.manual_college_name = False
            self.manual_department_name = False
            self.manual_stage_name = False
            self.manual_university_id = False

    def get_display_data(self):
        """Get the final display data (manual override or partner data)"""
        self.ensure_one()
        if self.allow_manual_edit:
            return {
                'student_name': self.student_name or '________________',
                'college_name': self.manual_college_name or self.college_name or '________________',
                'department_name': self.manual_department_name or self.department_name or '________________',
                'stage_name': self.manual_stage_name or self.stage_name or '________________',
                'university_id': self.manual_university_id or self.university_id or '________________',
            }
        else:
            return {
                'student_name': self.student_name or '________________',
                'college_name': self.college_name or '________________',
                'department_name': self.department_name or '________________',
                'stage_name': self.stage_name or '________________',
                'university_id': self.university_id or '________________',
            }

    def action_print_exam_card(self):
        """Generate and print the exam card"""
        self.ensure_one()
        
        # Validate required fields
        if not self.partner_id:
            raise ValidationError('الرجاء اختيار الطالب')
        
        # Get display data
        display_data = self.get_display_data()
        
        data = {
            'exam_type': self.exam_type,
            'academic_year': self.academic_year.year if self.academic_year else '',
            'partner_id': self.partner_id.id,
            'partner_name': self.partner_id.name,
            'student_name': display_data['student_name'],
            'college_name': display_data['college_name'],
            'department_name': display_data['department_name'],
            'stage_name': display_data['stage_name'],
            'university_id': display_data['university_id'],
        }
        data.update(display_data)
        
        return self.env.ref('exam_card.action_report_account_exam_card_wizard').report_action(self, data=data)


class ExamCardPrint(models.AbstractModel):
    _name = 'report.exam_card.report_exam_card'
    _description = 'Exam Card Report'

    @api.model
    def _get_report_values(self, docids, data=None):
        docs = []
        if data:
            doc = {
                'exam_type': data.get('exam_type', 'الامتحانات النهائية'),
                'academic_year': data.get('academic_year', ''),
                'student_name': data.get('student_name', '________________'),
                'college_name': data.get('college_name', '________________'),
                'department_name': data.get('department_name', '________________'),
                'stage_name': data.get('stage_name', '________________'),
                'university_id': data.get('university_id', '________________'),
                'partner_id': data.get('partner_id'),
                'partner_name': data.get('partner_name'),
            }
            docs.append(doc)
        
        return {
            'doc_ids': docids,
            'doc_model': 'exam.card.wizard',
            'docs': docs,
        }