odoo.define('fx_theme.menu', function (require) {
    "use strict";

    var core = require('web.core');
    var Widget = require('web.Widget');
    var UserProfile = require('fx_theme.UserProfile');
    var session = require('web.session');
    var FxMenuBoard = require('fx_theme.menu_board')
    var dom = require('web.dom');

    var $body = $("body");
    var $window = $(window);

    var Menu = Widget.extend({

        template: 'fx_theme.menu',
        current_menu_id: undefined,
        current_primary_menu: undefined,
        menu_board: undefined,

        events: {
            'click .navigation-menu-group ul li>a': '_onMenuItemClick',
            'click [data-nav-target]': '_onAppNameClicked',
            'click .navigation-logo': '_onLogoClick',
            'click #fx_theme_menu_entry_lvl_1': '_onMenuItemClick'
        },

        custom_events: _.extend({}, Widget.prototype.custom_events, {
            'fx_favorite_app_dropped': '_onAppDropped',
            'fx_update_favorite': '_updaeFavorites'
        }),

        getApps: function () {
            return this._apps;
        },

        _onAppDropped: function (event) {
            var $dropedEl = $(event.data.el)

            var menuID = $dropedEl.data('menu-id')
            var app = _.find(this._apps, function (tmpApp) {
                return tmpApp.menuID == menuID
            })
            if (app) {
                var $app = this.$('.navigation-menu-tab-body [data-menu-id="' + menuID + '"]').not($dropedEl)
                if ($app) {
                    $app.remove()
                }
            }
            this._updaeFavorites()
        },

        init: function (parent, menu_data, user_setting) {
            this._super.apply(this, arguments);

            this.$menu_sections = {};
            this.menu_data = menu_data;
            this.user_setting = user_setting || {}

            this._apps = _.map(this.menu_data.children, function (appMenuData) {
                return {
                    actionID: parseInt(appMenuData.action.split(',')[1]),
                    menuID: appMenuData.id,
                    name: appMenuData.name,
                    xmlID: appMenuData.xmlid,
                    web_icon_data: appMenuData.web_icon_data
                };
            });

            // hide the side bar 
            core.bus.on('click', this, function (event) {
                if (!$(event.target).is($(".navigation, .navigation *, .navigation-toggler *"))
                    && $body.hasClass("navigation-toggle-one")) {
                    $body.removeClass("navigation-show")
                }
            });
            
            core.bus.on('change_menu_item', this, this.change_menu_item);
            core.bus.on('change_action_item', this, this.change_action_item);
            core.bus.on('open_first_leaf_app', this, this._open_first_leaf_app);
        },

        start: function () {
            var self = this
            return this._super.apply(this, arguments).then(function () {
                // place the user profile
                self.userProfile = new UserProfile(self)
                self.userProfile.appendTo(self.$(".navigation-menu-tab-header"))
                
                // add the sub item arrow
                self.$(".navigation-menu-body ul li a").each(function () {
                    var item = $(this);
                    if (item.next("ul").length) {
                        item.append('<i class="sub-menu-arrow fa fa-angle-down"></i>')
                    }
                });

                self.$(".navigation-menu-body ul li.open > a > .sub-menu-arrow")
                    .removeClass("fa fa-angle-down")
                    .addClass("fa fa-angle-up").addClass("rotate-in")

                // just show when above 992
                if (992 <= $window.width()) {
                    self.$(".navigation-menu-body").niceScroll()
                }

                self.$('[data-toggle="tooltip"]').tooltip({
                    container: "body"
                })

                self._initMenuBoard();
            });
        },

        _open_first_leaf_app: function(menu_id) {
            var app = _.find(this.menu_data.children, function (tmp_data) {
                return tmp_data.id == menu_id
            })
            this.openFirsetLeafApp(app);
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

        update_logo: function (reload) {
            var company = session.company_id;
            var img = session.url('/web/binary/company_logo' + '?db=' + session.db + (company ? '&company=' + company : ''));
            this.$('.navigation-logo a img').attr('src', '').attr('src', img + (reload ? "&t=" + Date.now() : ''));
            this.$('.oe_logo_edit').toggleClass('oe_logo_edit_admin', session.is_superuser);
        },

        // data-nav-target
        _onAppNameClicked: function (event) {
            event.preventDefault();
            var item = $(event.currentTarget)
            this._openApp(item)
        },

        _onMenuItemClick: function (event) {
            console.log("event@@@@@@@@@@@@@@@@@@@@@",event)
            var click_link = $(event.currentTarget)
            console.log("click_link@@@@@@@@@@@@@@@@@",click_link.next("div"))

            // if(click_link.next("div").hasClass('close')) {
            //     click_link.next("div").removeClass('close')
            //     click_link.next("div").addClass('open')
            //  }

            

            
             
            // div.nextSibling
            if (click_link.next("ul").length) {
                event.stopPropagation()
                event.preventDefault()
            } else {
                // just trigger on leaf
                core.bus.trigger('fx_menu_item_clicked')
                if(click_link.next("div").css("display") == "none") {
                click_link.next("div").css("display", "block")
                // click_link.next("div").addClass('open')
             }
             
                else{

                click_link.next("div").css("display", "none")
            }
            }
            this._onLinkClicked(click_link)
        },

        _onLinkClicked: function (click_link) {
            if (click_link.next("ul").length) {
                var arrow = click_link.find(".sub-menu-arrow");
                if (arrow.hasClass("fa-angle-down")) {
                    setTimeout(function () {
                        arrow.removeClass("fa-angle-down").addClass("fa fa-angle-up")
                    }, 200)
                } else {
                    arrow.removeClass("fa-angle-up").addClass("fa fa-angle-down");
                }
                arrow.toggleClass("rotate-in")
                click_link.next("ul").toggle(200)

                click_link.parent("li").siblings().find("ul").not(click_link.parent("li").find("ul")).slideUp(200)
                click_link.next("ul").find("li ul").slideUp(200);

                // update sub arrows
                var arrows = click_link.next("ul").find("li>a").find(".sub-menu-arrow")
                arrows.removeClass("fa-angle-up").addClass("fa-angle-down").removeClass("rotate-in")

                // update next block arrows
                arrows = click_link.parent("li").siblings().not(click_link.parent("li").find("ul")).find(">a").find(".sub-menu-arrow")
                arrows.removeClass("fa-angle-up").addClass("fa-angle-down").removeClass("rotate-in")

                var $body = $("body");
                var $window = $(window);
                if (!$body.hasClass("horizontal-side-menu") && 1200 <= $window.width()) {
                    setTimeout(function () {
                        self.$(".navigation-menu-body").getNiceScroll().resize()
                    }, 300)
                }
            } else {
                var menu_id = click_link.data("menu")
                console.log("click_link@@@@@@@@222222222222444444444444444",click_link.next("div"))
                this.current_menu_id = menu_id
                this.$('.navigation-menu-group a').removeClass('active')
                
                click_link.addClass('active')
            }
        },

        /**
         * Helpers used by web_client in order to restore the state from
         * an url (by restore, read re-synchronize menu and action manager)
         */
        action_id_to_primary_menu_id: function (action_id) {
            var primary_menu_id, found;
            for (var i = 0; i < this.menu_data.children.length && !primary_menu_id; i++) {
                found = this._action_id_in_subtree(this.menu_data.children[i], action_id);
                if (found) {
                    primary_menu_id = this.menu_data.children[i].id;
                }
            }
            return primary_menu_id;
        },

        // check whether the action id is in the subtree
        _action_id_in_subtree: function (root, action_id) {
            // action_id can be a string or an integer
            if (root.action && root.action.split(',')[1] === String(action_id)) {
                return true;
            }
            var found;
            for (var i = 0; i < root.children.length && !found; i++) {
                found = this._action_id_in_subtree(root.children[i], action_id);
            }
            return found;
        },

        _get_app_data: function (menu_id) {
            var app = undefined
            for (var i = 0; i < this.menu_data.children.length; i++) {
                if (this.menu_data.children[i].id == menu_id) {
                    app = this.menu_data.children[i]
                    break;
                }
            }
            return app
        },

        openFirstApp: function () {
            if (!this.menu_data.children
                || this.menu_data.children.length == 0) {
                return
            }
            var firstApp = this.menu_data.children[0]
            if (!firstApp.children || firstApp.children.length == 0) {
                $('body').addClass('no-sub-menu')
                this._open_menu_section(firstApp.id);
                var action_id = firstApp.action.split(',')[1];
                this._trigger_menu_clicked(firstApp.id, action_id);
                this.current_menu_id = firstApp.id;
            } else {
                $('body').removeClass('no-sub-menu')
                var firstLeafApp = this.getFirstLeafApp(firstApp)
                if (firstLeafApp) {
                    this.change_menu_item(firstLeafApp.id)
                    var action_id = firstLeafApp.action.split(',')[1];
                    this._trigger_menu_clicked(firstLeafApp.id, action_id);
                    this.current_menu_id = firstLeafApp.id;
                }
            }
        },

        openFirsetLeafApp: function (secApp) {
            var targetApp = secApp;
            if (!targetApp.children || targetApp.children.length == 0) {
                $('body').addClass('no-sub-menu')
                this._open_menu_section(targetApp.id);
            } else {
                $('body').removeClass('no-sub-menu')
                targetApp = this.getFirstLeafApp(targetApp)
                this.change_menu_item(targetApp.id)
            }

            var action_id = targetApp.action.split(',')[1];
            this._trigger_menu_clicked(targetApp.id, action_id);
            this.current_menu_id = targetApp.id;
        },

        _trigger_menu_clicked: function (menu_id, action_id) {
            this.trigger_up('menu_clicked', {
                id: menu_id,
                action_id: action_id,
                previous_menu_id: this.current_menu_id
            });
        },

        getFirstLeafApp: function (app) {
            // if has no sub app
            var subApps = app.children || false
            if (!subApps) {
                return app
            }
            for (var i = 0; i < subApps.length; i++) {
                var tmp_app = subApps[i]
                if (!tmp_app.children || tmp_app.children.length == 0) {
                    return tmp_app
                } else {
                    return this.getFirstLeafApp(tmp_app)
                }
            }
        },

        action_id_to_primary_menu_id: function (action_id) {
            var primary_menu_id = undefined;
            var found = false;
            for (var i = 0; i < this.menu_data.children.length; i++) {
                found = this._action_id_in_subtree(this.menu_data.children[i], action_id);
                if (found) {
                    primary_menu_id = this.menu_data.children[i].id;
                    break
                }
            }
            return primary_menu_id;
        },

        menu_id_to_action_id: function (menu_id, root) {

            if (!root) {
                root = $.extend(true, {}, this.menu_data);
            }

            if (root.id === menu_id) {
                return root.action.split(',')[1];
            }
            for (var i = 0; i < root.children.length; i++) {
                var action_id = this.menu_id_to_action_id(menu_id, root.children[i]);
                if (action_id !== undefined) {
                    return action_id;
                }
            }
            return undefined;
        },

        _get_menu_data: function (menu_id) {
            return _.find(this.menu_data.children, function (data) {
                return data.id == menu_id
            });
        },

        _openApp: function (item) {
            var menu_id = parseInt(item.data("menu-id"))
            var app = _.find(this.menu_data.children, function (tmp_data) {
                return tmp_data.id == menu_id
            })
            this.openFirsetLeafApp(app);
        },

        // just change the ui
        _open_menu_section: function (menu_id) {
            if (menu_id == this.primary_menu_id) {
                return
            }
            var app = this._get_app_data(menu_id)
            var item = this.$('[data-nav-target="#' + menu_id + '"]')
            var nav_target = item.data("nav-target");

            var $body = $("body");
            if (app.children && app.children.length > 0) {
                $body.removeClass('no-sub-menu')
                // open the tab
                if ($body.hasClass("navigation-toggle-one")) {
                    $body.addClass("navigation-show")
                }
                // close the active item
                $(".navigation .navigation-menu-body .navigation-menu-group > div").removeClass("open")
                // open the active item
                var menuBody = $(".navigation .navigation-menu-body .navigation-menu-group " + nav_target).addClass("open")
            } else {
                $body.addClass('no-sub-menu')
            }

            // set the status
            $("[data-nav-target]").removeClass("active")

            // addd the active status
            item.addClass("active")

            // add the tooltip
            item.tooltip("hide")

            // set the primary menuid to avoid renter
            this.current_primary_menu = menu_id;

            return menuBody
        },

        change_menu_item: function (menu_id) {
            var action_id = this.menu_id_to_action_id(menu_id)
            if (action_id) {
                this.change_action_item(parseInt(action_id))
            }
        },

        change_action_item: function (action_id) {
            var app_id = this.action_id_to_primary_menu_id(action_id)
            if (app_id) {
                // change the menu section
                var menuBody = this._open_menu_section(app_id)
                if (!menuBody) {
                    return
                }
                var link = menuBody.find('[data-action-id="' + action_id + '"]')
                // expand parent
                var parents = link.parents('ul')
                _.each(parents, function (ul) {
                    ul = $(ul).show()
                    var prev_link = ul.prev('a')
                    if (prev_link.length) {
                        var arrow = prev_link.find(".sub-menu-arrow")
                        arrow.removeClass("fa-angle-down").addClass("fa-angle-up")
                    }
                })
                this._onLinkClicked(link)
            }
        },

        _initMenuBoard: function () {
            this.menu_board = new FxMenuBoard(this, this.menu_data)
            this.menu_board.appendTo(this.$('.fx-nav-footer'))
        },

        _isMenuExsits: function (menuID) {
            return _.find(this._apps, function (tmpApp) {
                return tmpApp.menuID == menuID
            })
        },

        _updaeFavorites: function () {
            var favorites = this.$('.fx_nav_bar_app_item')
            var datas = []
            for (var index = 0; index < favorites.length; index++) {
                var favorite = $(favorites[index]);
                datas.push({
                    'sequence': parseInt(favorite.index()),
                    'menu_id': parseInt(favorite.attr('data-menu-id'))
                })
            }
            if (datas.length > 0) {
                this._rpc({
                    "model": "fx.favorite_menu",
                    "method": "update_favorite_menu",
                    "args": [datas]
                })
            }
        }
    });

    return Menu;
});
