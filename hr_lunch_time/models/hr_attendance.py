from odoo import fields, models, api, exceptions, _


class HrAttendance(models.Model):
    _inherit = 'hr.attendance'

    lunch_start = fields.Datetime('Lunch Start Time')
    lunch_end = fields.Datetime('Lunch End Time')

    @api.depends('check_in', 'check_out', 'lunch_start', 'lunch_end')
    def _compute_worked_hours(self):
        for attendance in self:
            if attendance.check_out and attendance.check_in:
                delta = attendance.check_out - attendance.check_in
                if attendance.lunch_end and attendance.lunch_start:
                    lunch_delta = attendance.lunch_end - attendance.lunch_start
                    attendance.worked_hours = ((delta.total_seconds() - lunch_delta.total_seconds()) / 3600.0)
                else:
                    attendance.worked_hours = delta.total_seconds() / 3600.0
            else:
                attendance.worked_hours = False


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    attendance_state = fields.Selection(selection_add=[('lunch_start', 'Lunch Start'),
                                                       ('lunch_end', 'Lunch End')])

    @api.depends('last_attendance_id.check_in', 'last_attendance_id.check_out', 'last_attendance_id')
    def _compute_attendance_state(self):
        for employee in self:
            att = employee.last_attendance_id.sudo()
            if att.check_in and not att.check_out and not att.lunch_start and not att.lunch_end:
                employee.attendance_state = 'checked_in'
            elif att.check_in and not att.check_out and att.lunch_start and not att.lunch_end:
                employee.attendance_state = 'lunch_start'
            elif att.check_in and not att.check_out and att.lunch_start and att.lunch_end:
                employee.attendance_state = 'lunch_end'
            else:
                employee.attendance_state = 'checked_out'

    def _attendance_action_change(self):
        """ Check In/Check Out action
            Check In: create a new attendance record
            Check Out: modify check_out field of appropriate attendance record
        """
        self.ensure_one()
        action_date = fields.Datetime.now()
        if self.attendance_state == 'checked_out':
            vals = {
                'employee_id': self.id,
                'check_in': action_date,
            }
            return self.env['hr.attendance'].create(vals)

        attendance = self.env['hr.attendance'].search([('employee_id', '=', self.id), ('check_out', '=', False)], limit=1)
        state = self._context.get('state')
        if attendance and state:
            if state == 'lunch_start':
                attendance.lunch_start = action_date
            elif state == 'lunch_end':
                attendance.lunch_end = action_date
            elif state == 'check_out':
                attendance.check_out = action_date
        elif attendance and not state:
            attendance.check_out = action_date
        else:
            raise exceptions.UserError(_('Cannot perform check out on %(empl_name)s, could not find corresponding check in. '
                'Your attendances have probably been modified manually by human resources.') % {'empl_name': self.sudo().name, })
        return attendance
