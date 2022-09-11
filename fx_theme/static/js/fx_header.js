odoo.define('fx_theme.header', function (require) {
    "use strict";

    var SystrayMenu = require('web.SystrayMenu');
    var Widget = require('web.Widget');
    var overLay = require('fx.overlay');
    var core = require('web.core')
    var AppMenu = require('fx_theme.app_menu')

    var FxThemeHeader = Widget.extend({
        template: 'fx_theme_header',
        overlay: undefined,
        RESIZE_DELAY: 200,
        app_nemu: undefined,
        menu_data: undefined,

        events: _.extend({}, Widget.prototype.events, {
            "click .navigation-toggler": '_on_toggle_click',
        }),

        custom_events: _.extend({}, Widget.prototype.custom_events, {
            'fx_overlay_clicked': '_on_overlay_clicked'
        }),

        init: function (parent, menu_data) {
            this._super.apply(this, arguments);
            this.menu_data = menu_data;
        },

        _on_toggle_click: function (event) {
            event.preventDefault();
            event.stopPropagation();

            var self = this;
            var $window = $(window);
            var $body = $('body');

            // create overlay when the size is below 1200
            if ($window.width() < 1200) {
                self.createOverlay();
                $body.addClass("navigation-show");
            } else {
                if ($body.hasClass("navigation-toggle-one")) {
                    $body.addClass("navigation-toggle-none");
                    $body.removeClass("navigation-toggle-one");
                    $body.removeClass("navigation-show");
                } else if ($body.hasClass("navigation-toggle-two")) {
                    $body.addClass("navigation-toggle-one");
                    $body.removeClass("navigation-toggle-two");
                    $body.removeClass("navigation-show");
                } else if ($body.hasClass("navigation-toggle-none")) {
                    $body.addClass("navigation-toggle-two");
                    $body.removeClass("navigation-toggle-none");
                    $body.removeClass("navigation-show");
                } else {
                    // if nothing
                    $body.addClass("navigation-toggle-one");
                    $body.removeClass("navigation-toggle-two");
                    $body.removeClass("navigation-show");
                }
            }
        },

        on_attach_callback: function () {
            this.appMenu.on_attach_callback()
        },

        createOverlay: function () {
            if (!this.overlay) {
                this.overlay = new overLay(this)
                var $body = $("body");
                this.overlay.appendTo($body)
            } else {
                this.overlay.show()
            }
        },

        start: function () {
            this.systray_menu = new SystrayMenu(this);
            var systrayMenuProm = this.systray_menu.attachTo(this.$('.fx_theme_systray'));

            this.appMenu = new AppMenu(this, this.menu_data);
            this.appMenu.appendTo(this.$('.app_menu'));

            core.bus.on('resize', this, _.debounce(this._onResize.bind(this), this.RESIZE_DELAY));
            core.bus.on('fx_menu_item_clicked', this, this._onMenuItemClicked.bind(this));

            return Promise.all([this._super.apply(this, arguments), systrayMenuProm]);
        },

        _onResize: function () {
            var window_width = $(window).width();
            if (window_width < 1200 && $('body').hasClass('navigation-show')) {
                this.createOverlay();
            }
        },

        _on_overlay_clicked: function () {
            if (this.overlay) {
                var $body = $("body");
                $body.removeClass('navigation-show')
                this.overlay.hide();
            }
        },

        _onMenuItemClicked: function () {
            if (this.overlay && this.overlay.is_visible()) {
                var $body = $("body");
                $body.removeClass('navigation-show')
                this.overlay.hide();
            }
        }
    });

    return FxThemeHeader;
});
