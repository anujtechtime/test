odoo.define('fx.selection', function (require) {
    "use strict";

    var Fields = require("web.relational_fields")
    var special_fields = require("web.special_fields")

    Fields.FieldSelection.include({
        template: 'fx.selection',

        on_attach_callback: function () {
            if (this.mode === 'edit') {
                if (this.attrs.placeholder) {
                    this.$el.select2({
                        id: false,
                        text: this.attrs.placeholder
                    });
                } else {
                    this.$el.select2();
                }
            }
        }
    });

    special_fields.FieldTimezoneMismatch.include({
        template: 'fx.selection',

        on_attach_callback: function () {
            if (this.mode === 'edit') {
                if (this.attrs.placeholder) {
                    this.$el.first().select2({
                        id: false,
                        text: this.attrs.placeholder
                    });
                } else {
                    this.$el.first().select2();
                }
            }
        }
    })

});