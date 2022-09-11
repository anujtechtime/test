odoo.define('fx_theme.form_render', function (require) {
    "use strict";

    var formRender = require("web.FormRenderer")

    formRender.include({
        // overwrite to add card class to sheet
        _renderTagSheet: function (node) {
            this.has_sheet = true;
            var $sheet = $('<div>', {class: 'clearfix card position-relative o_form_sheet'});
            $sheet.append(node.children.map(this._renderNode.bind(this)));
            return $sheet;
        },
    })
});
