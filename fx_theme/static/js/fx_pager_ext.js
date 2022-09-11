odoo.define('web.fx_pager_ext', function (require) {
    "use strict";

    // replace the template
    var Pager = require('web.Pager');
    Pager.include({
        template: "fx.Pager"
    });
});
