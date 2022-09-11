odoo.define('fx.search_filters', function (require) {
    "use strict";

    var search_filters = require('web.search_filters');
    var ExtendedSearchProposition = search_filters.ExtendedSearchProposition

    // rewrite to replace the template
    ExtendedSearchProposition.include({
        template: 'fx.extended_search.proposition',

        select_field: function (field) {
            this._super.apply(this, arguments)
        },
    });
});
