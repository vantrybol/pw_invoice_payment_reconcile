odoo.define('hr_lunch_time.kiosk_mode_real', function(require) {
      "use strict";

      var KioskMode = require('hr_attendance.kiosk_confirm');
      var core = require('web.core');
      var QWeb = core.qweb;
      var _t = core._t;
      var config = require('web.config');
      var Dialog = require('web.Dialog');
      var field_utils = require('web.field_utils');

      KioskMode.include({
          events: _.extend(KioskMode.prototype.events ,{
              "click .o_hr_attendance_sign_in_out_icon": _.debounce(function(e) {
                  this.state = $(e.currentTarget).data('state');
                  var self = this;
                  this._rpc({
                          model: 'hr.employee',
                          method: 'attendance_manual',
                          args: [[this.employee_id], this.next_action],
                          context: {
                              'state': this.state,
                          },
                      })
                      .then(function(result) {
                          if (result.action) {
                              self.do_action(result.action);
                          } else if (result.warning) {
                              self.do_warn(result.warning);
                          }
                      });
              }, 200, true),
              'click .o_hr_attendance_pin_pad_button_ok': _.debounce(function(e) {
                 this.state = $(e.currentTarget).data('state')
                 this.update_attendance();
             }, 200, true),
             'click .o_hr_attendance_pin_pad_button_checkout, .o_hr_attendance_pin_pad_button_lunch-start': _.debounce(function(e) {
                 this.state = $(e.currentTarget).data('state')
                 this.update_attendance();
             }, 200, true),
          }),

          update_attendance: function(){
             var self = this;
             var current_state = this.$('input[name="hidden_state"]').data('state');
             if(!this.state){
                 if(current_state == 'checked_out'){
                     this.state = 'checked_in';
                 } else if(current_state == 'lunch_start'){
                     this.state = 'lunch_end';
                 } else if(current_state == 'lunch_end'){
                     this.state = 'check_out';
                 }
             }
             this.$('.o_hr_attendance_pin_pad_button_ok').attr("disabled", "disabled");
             this._rpc({
                 model: 'hr.employee',
                 method: 'attendance_manual',
                 args: [[this.employee_id], this.next_action, this.$('.o_hr_attendance_PINbox').val()],
                 context: {
                     'state': this.state
                 }
             })
             .then(function(result) {
                 if (result.action) {
                     self.do_action(result.action);
                 } else if (result.warning) {
                     self.do_warn(result.warning);
                     self.$('.o_hr_attendance_PINbox').val('');
                     setTimeout( function() { self.$('.o_hr_attendance_pin_pad_button_ok').removeAttr("disabled"); }, 500);
                 }
             });
          },
      });
  });