odoo.define('fx_theme.abstract_controller', function (require) {
    "use strict";

    var core = require('web.core');
    var dom = require('web.dom');

    var SystrayMenu = require('web.SystrayMenu');
    var Widget = require('web.Widget');

    var QWeb = core.qweb;

    var FxThemeHeader = Widget.extend({
        template: 'fx_theme_header',

        events: {},

        init: function (parent, menu_data) {
            this._super.apply(this, arguments);
        },

        start: function () {
            var self = this;
            this.systray_menu = new SystrayMenu(this);
            var systrayMenuProm = this.systray_menu.attachTo(
                this.$('.o_menu_systray')).then(function () {
                    dom.initAutoMoreMenu(self.$section_placeholder, {
                        maxWidth: function () {
                            return self.$el.width();
                        },
                        sizeClass: 'SM',
                    });
                });

            return Promise.all([this._super.apply(this, arguments), systrayMenuProm]);
        }
    });

    return FxThemeHeader;
});
