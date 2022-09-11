odoo.define('fx_theme.SystrayMenu', function (require) {
    "use strict";

    var Widget = require('web.Widget');
    var SystrayMenu = require('web.SystrayMenu')
    var UserMenu = require('web.UserMenu')

    SystrayMenu.include({

        /**
         * extend to remove the user menu
         * @override
         */
        willStart: function () {
            var self = this;
            var proms = [];
            SystrayMenu.Items = _.sortBy(SystrayMenu.Items, function (item) {
                return !_.isUndefined(item.prototype.sequence) ? item.prototype.sequence : 50;
            });

            SystrayMenu.Items.forEach(function (WidgetClass) {
                var cur_systray_item = new WidgetClass(self);
                // ignore the user menu
                self.widgets.push(cur_systray_item);
                proms.push(cur_systray_item.appendTo($('<div>')));
            });

            return Widget.prototype.willStart.apply(this, arguments).then(function () {
                return Promise.all(proms);
            });
        }
    });
});

