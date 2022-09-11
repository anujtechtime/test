odoo.define('fx_theme.page_footer', function (require) {
    "use strict";

    var core = require('web.core');
    var Widget = require('web.Widget');

    var fxThemePageFooter = Widget.extend({
        template: 'fx_theme.footer',

        events: _.extend({}, Widget.prototype.events, {}),

        start: function () {
            this._super.apply(this, arguments)
            
            core.bus.on('fx_update_switcher', this, this.udpate_switcher);
            core.bus.on('fx_clear_switcher', this, this.clear_switcher);
            core.bus.on('fx_update_pager', this, this.update_pager);
            core.bus.on('fx_clear_pager', this, this.clear_pager);
        },

        udpate_switcher: function (data) {
            this.$('.switcher').append(data)
        },

        set_corp_info: function (info) {
            this.$('.fx_corp_info').text(info)
        },

        clear_switcher: function () {
            this.$('.switcher').contents().detach();
        },

        clear_pager: function() {
            this.$('.pager').contents().detach();
        },

        update_pager: function(data) {
            this.$('.pager').append(data)
        }
    });

    return fxThemePageFooter;
});
