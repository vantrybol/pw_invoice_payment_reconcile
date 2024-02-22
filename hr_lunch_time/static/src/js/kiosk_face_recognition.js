odoo.define('hr_lunch_time.kiosk_mode', function(require) {
    "use strict";

    var Attendances = require('hr_attendance.my_attendances');
    var core = require('web.core');
    var QWeb = core.qweb;
    var _t = core._t;
    var config = require('web.config');
    var field_utils = require('web.field_utils');


    Attendances.include({
        events: _.extend(Attendances.prototype.events ,{
            "click .o_hr_attendance_sign_in_out_icon": _.debounce(function(e) {
                this.state = $(e.currentTarget).data('state');
                this.update_attendance();
            }, 200, true),
        }),
        update_attendance: function () {
            var self = this;
            this._rpc({
                model: 'hr.employee',
                method: 'attendance_manual',
                args: [[self.employee.id], 'hr_attendance.hr_attendance_action_my_attendances'],
                context: {
                    'state': self.state,
                },
            }).then(function(result) {
                if (result.action) {
                    self.do_action(result.action);
                } else if (result.warning) {
                    self.do_warn(result.warning);
                }
            });
        },
    });
});