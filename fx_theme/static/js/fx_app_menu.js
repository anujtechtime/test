odoo.define('fx_theme.app_menu', function (require) {
    "use strict";

    var core = require('web.core');
    var Widget = require('web.Widget');
    var UserProfile = require('fx_theme.UserProfile');
    var qweb = core.qweb

    var AppMenu = Widget.extend({
        template: 'fx_theme.app_menu',

        events: _.extend({}, Widget.prototype.event, {
            'click [data-nav-target]': '_onAppNameClicked',
            'click .navigation-logo img': '_onLogoClick'
        }),

        custom_events: _.extend({}, Widget.prototype.custom_events, {}),

        getApps: function () {
            return this._apps;
        },

        init: function (parent, menu_data) {
            this._super.apply(this, arguments);

            this.menu_data = menu_data
            this._apps = _.map(this.menu_data.children, function (appMenuData) {
                return {
                    actionID: parseInt(appMenuData.action.split(',')[1]),
                    menuID: appMenuData.id,
                    name: appMenuData.name,
                    xmlID: appMenuData.xmlid,
                    web_icon_data: appMenuData.web_icon_data
                };
            });
        },

        start: function () {
            var self = this
            return this._super.apply(this, arguments).then(function () {
                // place the user profile
                self.userProfile = new UserProfile(self)
                self.userProfile.appendTo(self.$(".navigation-menu-tab-header"))
                setTimeout(() => {
                    self._initResize() 
                }, 0);
            });
        },

        _initResize: function () {
            var self = this;
            var res = undefined;
            $(window).on('resize', function () {
                if (res) { clearTimeout(res) }
                res = setTimeout(_.bind(self._check_size, self), 100);
            });
            setTimeout(_.bind(self._check_size, self), 300)
        },

        on_attach_callback: function () {
            this._initResize()
        },

        _check_size: function () {

            // the hz app menu is hide
            if ($(window).width() < 1200) {
                return
            }

            var view_more_width = this.$('.view_more_app').outerWidth(true);
            var max_width = this.$el.width();
            var total_width = view_more_width

            this.$('.view_more_app + .dropdown-menu > div').empty()
            this.$('.app_item').each(function () {
                total_width += $(this).outerWidth(true);
            });

            if (total_width > max_width) {
                var self = this;
                this.$('.view_more_app > div > a').remove();
                var cur_width = view_more_width;
                var show_more_app = false;
                this.$('.app_item').show().each(function () {
                    if (cur_width + $(this).outerWidth(true) < max_width - 10) {
                        cur_width += $(this).outerWidth(true);
                    } else {
                        self.$('.view_more_app + .dropdown-menu > div').append($(this).clone());
                        // hide the item
                        $(this).hide();
                        show_more_app = true
                    }
                });
                if (show_more_app) {
                    this.$('.view_more_app').addClass('show');
                }
            } else {
                this.$('.app_item').show();
                this.$('.view_more_app').removeClass('show');
            }
        },

        // data-nav-target
        _onAppNameClicked: function (event) {
            event.preventDefault();
            var $item = $(event.currentTarget);
            this.$('.app_item').removeClass('active');
            var menu_id = $item.data('menu-id')
            core.bus.trigger('open_first_leaf_app', menu_id);
            $item.addClass('active');
        },

        _onLogoClick: function (ev) {
            var self = this;
            ev.preventDefault();
            this._rpc({
                model: 'res.users',
                method: 'read',
                args: [[session.uid], ['company_id']],
            })
                .then(function (data) {
                    self._rpc({
                        route: '/web/action/load',
                        params: { action_id: 'base.action_res_company_form' },
                    })
                        .then(function (result) {
                            result.res_id = data[0].company_id[0];
                            result.target = "new";
                            result.views = [[false, 'form']];
                            result.flags = {
                                action_buttons: true,
                                headless: true,
                            };
                            self.do_action(result, {
                                on_close: self.update_logo.bind(self, true),
                            });
                        });
                });
            return false;
        },
    });

    return AppMenu;
});
