# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError, UserError

class ResPartner(models.Model):
    _inherit = 'res.partner'

    # Student Type Fields
    # student_type = fields.Many2one(
    #     'level.level', 
    #     string='Student Type',
    #     help='Select the student type from the available levels'
    # )
    
    # Attachment Fields for Official Letter
    student_type_attachment = fields.Binary(
        string='Official Letter (كتاب رسمي)',
        attachment=True,
        help='Upload the official letter for student type change'
    )
    
    student_type_attachment_filename = fields.Char(
        string='Attachment Filename',
        help='Name of the uploaded file'
    )
    
    # Tracking Fields
    previous_student_type = fields.Many2one(
        'level.level', 
        string='Previous Student Type',
        help='Stores the previous student type for tracking changes'
    )
    
    student_type_change_pending = fields.Boolean(
        string='Student Type Change Pending',
        default=False,
        help='Flag indicating if a student type change requires attachment'
    )
    
    student_type_change_date = fields.Datetime(
        string='Student Type Change Date',
        help='Date when the student type was last changed'
    )
    
    student_type_changed_by = fields.Many2one(
        'res.users',
        string='Changed By',
        help='User who last changed the student type'
    )

    @api.onchange('student_type')
    def _onchange_student_type(self):
        """Handle student type change and validate attachment requirement"""
        if self.student_type:
            # Get the general channel values
            general_types = self._get_general_channel_types()
            
            # Check if new type is non-general
            if self.student_type.Student not in general_types:
                # Check if this is a change from previous value
                if self.previous_student_type and self.previous_student_type != self.student_type:
                    # Set pending flag
                    self.student_type_change_pending = True
                    
                    # Validate if attachment exists
                    if not self.student_type_attachment:
                        return {
                            'warning': {
                                'title': _('Attachment Required'),
                                'message': _(
                                    'يجب رفع كتاب رسمي لتغيير نوع الطالب إلى: %s\n'
                                    'Please upload an official letter to change student type to: %s'
                                ) % (self.student_type.Student, self.student_type.Student)
                            }
                        }
                elif not self.previous_student_type:
                    # New record with non-general type
                    self.student_type_change_pending = True
                    if not self.student_type_attachment:
                        return {
                            'warning': {
                                'title': _('Attachment Required'),
                                'message': _(
                                    'يجب رفع كتاب رسمي لتحديد نوع الطالب: %s\n'
                                    'Please upload an official letter for student type: %s'
                                ) % (self.student_type.Student, self.student_type.Student)
                            }
                        }
            else:
                # If changing to general channel, clear pending flag
                self.student_type_change_pending = False

    @api.onchange('student_type_attachment')
    def _onchange_attachment(self):
        """Clear pending flag when attachment is added"""
        if self.student_type_attachment and self.student_type_change_pending:
            self.student_type_change_pending = False
            return {
                'warning': {
                    'title': _('Attachment Added'),
                    'message': _('Official letter uploaded successfully. You can now save the record.')
                }
            }

    @api.constrains('student_type', 'student_type_attachment')
    def _check_student_type_attachment(self):
        """Validate that attachment is required for non-general types"""
        for record in self:
            if record.student_type:
                general_types = record._get_general_channel_types()
                
                # Check if student type is non-general
                if record.student_type.Student not in general_types:
                    # Check if this is a change from the original record
                    if record._origin and record._origin.student_type != record.student_type:
                        if not record.student_type_attachment:
                            raise ValidationError(_(
                                'يجب رفع كتاب رسمي لتغيير نوع الطالب إلى: %s\n'
                                'An official letter is required to change student type to: %s'
                            ) % (record.student_type.Student, record.student_type.Student))
                    
                    # Check if this is a new record with non-general type
                    elif not record._origin and not record.student_type_attachment:
                        raise ValidationError(_(
                            'يجب رفع كتاب رسمي لتحديد نوع الطالب: %s\n'
                            'An official letter is required for student type: %s'
                        ) % (record.student_type.Student, record.student_type.Student))

    def _get_general_channel_types(self):
        """Get the list of general channel type names"""
        return ['عامة', 'قناة عامة', 'General', 'General Channel']

    @api.model
    def create(self, vals):
        """Override create to handle initial student_type setup"""
        if 'student_type' in vals and vals.get('student_type'):
            student_type = self.env['level.level'].browse(vals['student_type'])
            general_types = self._get_general_channel_types()
            
            if student_type and student_type.Student not in general_types:
                if not vals.get('student_type_attachment'):
                    raise ValidationError(_(
                        'يجب رفع كتاب رسمي عند تحديد نوع طالب غير القناة العامة: %s\n'
                        'An official letter is required for non-general student type: %s'
                    ) % (student_type.Student, student_type.Student))
        
        # Set change tracking fields
        if 'student_type' in vals:
            vals.update({
                'student_type_change_date': fields.Datetime.now(),
                'student_type_changed_by': self.env.user.id,
            })
        
        return super(ResPartner, self).create(vals)

    def write(self, vals):
        """Override write to handle student_type changes with attachment validation"""
        # Handle student type change
        if 'student_type' in vals:
            for record in self:
                old_type = record.student_type
                new_type_id = vals.get('student_type')
                
                # Store previous type before change
                if old_type:
                    vals['previous_student_type'] = old_type.id
                
                # Validate change if new type is provided
                if new_type_id:
                    new_type = self.env['level.level'].browse(new_type_id)
                    general_types = self._get_general_channel_types()
                    
                    # Check if changing to non-general type
                    if new_type and new_type.Student not in general_types:
                        # Check if this is a real change
                        if old_type and old_type != new_type:
                            # Validate attachment exists
                            if not record.student_type_attachment and not vals.get('student_type_attachment'):
                                raise ValidationError(_(
                                    'يجب رفع كتاب رسمي لتغيير نوع الطالب من "%s" إلى "%s"\n'
                                    'An official letter is required to change student type from "%s" to "%s"'
                                ) % (old_type.Student, new_type.Student, old_type.Student, new_type.Student))
                            
                            # Set pending flag
                            vals['student_type_change_pending'] = True
                        elif not old_type:
                            # New record with non-general type
                            if not record.student_type_attachment and not vals.get('student_type_attachment'):
                                raise ValidationError(_(
                                    'يجب رفع كتاب رسمي لتحديد نوع الطالب: %s\n'
                                    'An official letter is required for student type: %s'
                                ) % (new_type.Student, new_type.Student))
                    else:
                        # Changing to general type, clear pending flag
                        vals['student_type_change_pending'] = False
                
                # Update tracking fields
                vals.update({
                    'student_type_change_date': fields.Datetime.now(),
                    'student_type_changed_by': self.env.user.id,
                })
        
        return super(ResPartner, self).write(vals)

    def action_clear_pending_change(self):
        """Action to manually clear pending change flag (for admin use)"""
        for record in self:
            if record.student_type_change_pending:
                if record.student_type_attachment:
                    record.student_type_change_pending = False
                else:
                    raise UserError(_(
                        'لا يمكن مسح حالة التغيير المعلق دون رفع كتاب رسمي\n'
                        'Cannot clear pending change status without uploading an official letter'
                    ))

    def action_request_attachment(self):
        """Action to request attachment from user"""
        for record in self:
            if record.student_type and record.student_type_change_pending:
                return {
                    'type': 'ir.actions.act_window',
                    'name': _('Upload Official Letter'),
                    'res_model': 'res.partner',
                    'res_id': record.id,
                    'view_mode': 'form',
                    'view_id': self.env.ref('student_type_management.view_partner_form_inherit').id,
                    'target': 'current',
                    'context': {
                        'default_student_type_attachment': record.student_type_attachment,
                        'default_student_type_change_pending': True,
                    }
                }