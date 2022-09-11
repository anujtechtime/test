/**
 * fx form controller
 */
odoo.define('fx.FormController', function (require) {
    "use strict";

    var core = require('web.core');
    var FormController = require('web.FormController')

    var _t = core._t;
    var qweb = core.qweb;

    FormController.include({
        template: "fx.form_controller",

        // hook hte update control pannel
        updateControlPanel: function (status, options) {
            if (this._controlPanel) {
                status = status || {};
                status.title = status.title || this.getTitle();
                if (options.cp_content) {
                    if (options.cp_content.$buttons) {
                        var $buttons = options.cp_content.$buttons
                        this.$('.footer').append($buttons);
                        delete options.cp_content['$buttons']
                    }
                    this._controlPanel.updateContents(status, options || {});
                }
                this._controlPanel.updateContents(status, options || {});
            }
        },
    })
})