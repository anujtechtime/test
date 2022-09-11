odoo.define('fx_theme.full_screen', function (require) {
    "use strict";

    var Widget = require('web.Widget');

    var fxFullScreen = Widget.extend({
        events: _.extend({}, Widget.prototype.events, {
            "click [data-toggle='fullscreen']": "_on_full_screen"
        }),

        template: 'fx_full_screen',

        init: function (parent, menu_data) {
            this._super.apply(this, arguments);
        },

        _on_full_screen: function() {
            this.$el.toggleClass("active-fullscreen");
            if (document.fullscreenEnabled) {
                if (this.$el.hasClass("active-fullscreen")) {
                    document.documentElement.requestFullscreen()
                } else {
                    document.exitFullscreen()
                }
            } else {
                alert("your browser does not support fullscreen.")
            }
        }
    });

    return fxFullScreen;
});
