odoo.define('fx.basic_fields', function (require) {
    "use strict";

    var basic_fields = require('web.basic_fields');

    /**
     * add form control class
     */
    basic_fields.InputField.include({
        _renderEdit: function () {
            this._super.apply(this, arguments)
            this.$el.addClass('form-control')
        }
    })
})
