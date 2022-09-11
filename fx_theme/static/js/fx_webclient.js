
odoo.define('fx_theme.web_client', function (require) {
    "use strict";

    var WebClient = require('web.WebClient');
    var core = require('web.core');
    var session = require('web.session');
    var FxThemeHeader = require('fx_theme.header')
    var dom = require('web.dom');
    var fxMenu = require('fx_theme.menu')
    var DebugManager = require('web.DebugManager');

    // remove the include by debug manager
    require('web.DebugManager.Backend')

    var fx_web_client = WebClient.include({
        user_setting: {},

        start: function () {
            var self = this;
            var super_func = this._super
            return this._rpc({
                "model": "fx_theme.user_setting",
                "method": "get_user_setting",
                "args": [false]
            }).then(function (user_setting) {
                self.user_setting = user_setting;

                // init the menu type
                self._update_menu_type();

                // get the user setting
                core.bus.on('fx_get_user_setting', self, function (event) {
                    event.call_back(self.user_setting);
                });

                return super_func.apply(self, arguments).then(function () {
                    // hide side menu when navigation-toggle-one is set
                    var $body = $('body')
                    $(document).on("click", "*", function (event) {
                        var width = $(window).width()
                        if (!$(event.target).is($(".navigation, .navigation *, .navigation-toggler *"))
                            && ($body.hasClass("navigation-toggle-one") || width < 1200)) {
                            $body.removeClass("navigation-show")
                        }
                    });
                })
            })
        },

        current_action_updated: function (action, controller) {
            // this._super.apply(this, arguments);
            var debugManager = _.find(this.header.systray_menu.widgets, function (item) {
                return item instanceof DebugManager;
            });
            if (debugManager) {
                debugManager.update('action', action, controller && controller.widget);
            }
        },

        createOverlay: function () {
            var $body = $('body')
            if ($(".fx_theme_overlay").length < 1) {
                $body.addClass("no-scroll").append('<div class="fx_theme_overlay"></div>')
            }
            $(".fx_theme_overlay").addClass("show")
        },

        removeOverlay: function () {
            var $body = $('body')
            $body.removeClass("no-scroll");
            $(".fx_theme_overlay").remove()
        },

        _update_menu_type: function () {
            var menu_type = this.user_setting.menu_type;
            if (menu_type == 'horizon') {
                $('body').addClass('hz_menu')
                // remove the vertical classes
                $('body').removeClass('navigation-toggle-one')
                $('body').removeClass('navigation-toggle-two')
                $('body').removeClass('navigation-toggle-none')
            } else {
                $('body').removeClass('hz_menu')
            }
        },

        show_application: function () {

            var self = this;
            this.set_title();
            return this.menu_dp.add(this.instanciate_menu_widgets()).then(function () {

                // header need the menu data, so we put the init code here here
                self.instanciate_header_widget();

                // bind has change method
                $(window).bind('hashchange', self.on_hashchange);

                // If the url's state is empty, we execute the user's home action if there is one (we
                // show the first app if not)
                var state = $.bbq.getState(true);
                if (_.keys(state).length === 1 && _.keys(state)[0] === "cids") {
                    return self.menu_dp.add(self._rpc({
                        model: 'res.users',
                        method: 'read',
                        args: [session.uid, ["action_id"]],
                    }))
                        .then(function (result) {
                            var data = result[0];
                            if (data.action_id) {
                                return self.do_action(data.action_id[0]).then(function () {
                                    self.menu.change_menu_section(
                                        self.menu.action_id_to_primary_menu_id(data.action_id[0]));
                                });
                            } else {
                                self.menu.openFirstApp();
                            }
                        });
                } else {
                    return self.on_hashchange();
                }
            });
        },

        /**
         * ignore if horizon mode
         */
        instanciate_header_widget: function () {
            var self = this
            this.header = new FxThemeHeader(this, this.menu_data)
            var fragment = document.createDocumentFragment();
            return this.header.appendTo(fragment).then(function () {
                // here will call the on_attach_call_back
                dom.append(self.$el, fragment, {
                    in_DOM: true,
                    callbacks: [{ widget: self.header }],
                });
            });
        },

        instanciate_menu_widgets: function () {
            var self = this;
            return this.load_menus().then(function (menuData) {
                if (self.menu) {
                    self.menu.destroy();
                }
                self.menu = new fxMenu(self, menuData, self.user_setting);
                self.menu_data = menuData;
                var fragment = document.createDocumentFragment();
                return self.menu.appendTo(fragment).then(function () {
                    self.favorite_apps = self.menu.get_favorite_apps();
                    dom.append(self.$el, fragment, {
                        in_DOM: true,
                        callbacks: [{ widget: self.menu }],
                    });
                });
            });
        },

        /**
         * send the user setting to the client 
         * @param {*} event 
         */
        _on_get_user_setting: function (event) {
            var callback = event.data.callback
            callback(this.user_setting)
        },

        do_push_state: function (state) {
            if (!state.menu_id && this.menu) { // this.menu doesn't exist in the POS
                state.menu_id = this.menu.current_menu_id;
            }
            if ('title' in state) {
                this.set_title(state.title);
                delete state.title;
            }
            var url = '#' + $.param(state);
            this._current_state = $.deparam($.param(state), false); // stringify all values
            $.bbq.pushState(url);
            this.trigger('state_pushed', state);
        },

        on_hashchange: function (event) {

            if (this._ignore_hashchange) {
                this._ignore_hashchange = false;
                return Promise.resolve();
            }

            var self = this;
            return this.clear_uncommitted_changes().then(function () {
                var stringstate = $.bbq.getState(false);
                if (!_.isEqual(self._current_state, stringstate)) {
                    var state = $.bbq.getState(true);
                    if (state.action || (state.model && (state.view_type || state.id))) {
                        // load the action here
                        return self.menu_dp.add(self.action_manager.loadState(state, !!self._current_state)).then(function () {
                            if (state.menu_id) {
                                if (state.menu_id != self.menu.current_menu_id) {
                                    core.bus.trigger('change_menu_item', state.menu_id);
                                }
                            } else {
                                var action = self.action_manager.getCurrentAction();
                                if (action) {
                                    var menu_id = self.menu.action_id_to_primary_menu_id(action.id);
                                    if (state.menu_id != self.menu.current_menu_id) {
                                        core.bus.trigger('change_menu_item', menu_id);
                                    }
                                }
                            }
                        });
                    } else if (state.menu_id) {
                        var action_id = self.menu.menu_id_to_action_id(state.menu_id);
                        return self.menu_dp.add(self.do_action(action_id, { clear_breadcrumbs: true })).then(
                            function () {
                                core.bus.trigger('change_menu_section', state.menu_id);
                            });
                    } else {
                        self.menu.openFirstApp();
                    }
                }
                self._current_state = stringstate;
            }, function () {
                if (event) {
                    self._ignore_hashchange = true;
                    window.location = event.originalEvent.oldURL;
                }
            });
        },
    });

    return fx_web_client;
});
