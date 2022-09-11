/* Copyright 2018 Tecnativa - Jairo Llopis
 * License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl). */



odoo.define('web_responsive', function (require) {
    'use strict';

    // @oleksiipavlenko
    // function setCookie(key, value, expiry) {
    //     var expires = new Date();
    //     expires.setTime(expires.getTime() + (expiry * 24 * 60 * 60 * 1000));
    //     document.cookie = key + '=' + value + ';expires=' + expires.toUTCString();
    // }
    // @oleksiipavlenko
    // function getCookie(key) {
    //     var keyValue = document.cookie.match('(^|;) ?' + key + '=([^;]*)(;|$)');

    //     // document.cookie = "isMenuOpen=false";
    //     return keyValue ? keyValue[2] : null;
    // }
    // @oleksiipavlenko
    var AppsMenu = require("web.AppsMenu");
    var Menu = require("web.Menu");
    var ActionManager = require('web.ActionManager');
    var AbstractWebClient = require("web.AbstractWebClient");
    var BasicController = require('web.BasicController');
    var config = require("web.config");
    var core = require("web.core");
    var FormRenderer = require('web.FormRenderer');
    var RelationalFields = require('web.relational_fields');
    var Session = require('web.session');
    var utils = require('web.utils');
    // var Chatter = require('mail.Chatter');
    // var DocumentViewer = require('mail.DocumentViewer');
    // @oleksiipavlenko
    var first = true;
    // @oleksiipavlenko
    $(function() {
        (function($) {
            $(document).on('click', '.o_menu_apps .dropdown-menu', function (e) {
            e.stopPropagation();
        });
    }) (jQuery);
    });

    /* Hide AppDrawer in desktop and mobile modes.
     * To avoid delays in pages with a lot of DOM nodes we make
     * sub-groups' with 'querySelector' to improve the performance.
     */
    function closeAppDrawer () {
        _.defer(function () {
            // Need close AppDrawer?
            var menu_apps_dropdown = document.querySelector(
                '.o_menu_apps .dropdown');
            $(menu_apps_dropdown).has('.dropdown-menu.show')
                .find('> a').dropdown('toggle');
            // Need close Sections Menu?
            // TODO: Change to 'hide' in modern Bootstrap >4.1
            var menu_sections = document.querySelector(
                '.o_menu_sections li.show .dropdown-toggle');
            $(menu_sections).dropdown('toggle');
            $('.o_menu_sections').addClass('show');
            // Need close Mobile?
            var menu_sections_mobile = document.querySelector(
                '.o_menu_sections.show');
            $(menu_sections_mobile).collapse('hide');
        });
    }

    /**
     * Reduce menu data to a searchable format understandable by fuzzy.js
     *
     * `AppsMenu.init()` gets `menuData` in a format similar to this (only
     * relevant data is shown):
     *
     * ```js
     * {
     *  [...],
     *  children: [
     *    // This is a menu entry:
     *    {
     *      action: "ir.actions.client,94", // Or `false`
     *      children: [... similar to above "children" key],
     *      name: "Actions",
     *      parent_id: [146, "Settings/Technical/Actions"], // Or `false`
     *    },
     *    ...
     *  ]
     * }
     * ```
     *
     * This format is very hard to process to search matches, and it would
     * slow down the search algorithm, so we reduce it with this method to be
     * able to later implement a simpler search.
     *
     * @param {Object} memo
     * Reference to current result object, passed on recursive calls.
     *
     * @param {Object} menu
     * A menu entry, as described above.
     *
     * @returns {Object}
     * Reduced object, without entries that have no action, and with a
     * format like this:
     *
     * ```js
     * {
     *  "Discuss": {Menu entry Object},
     *  "Settings": {Menu entry Object},
     *  "Settings/Technical/Actions/Actions": {Menu entry Object},
     *  ...
     * }
     * ```
     */
    function findNames (memo, menu) {
        if (menu.action) {
            var key = menu.parent_id ? menu.parent_id[1] + "/" : "";
            memo[key + menu.name] = menu;
        }
        if (menu.children.length) {
            _.reduce(menu.children, findNames, memo);
        }
        return memo;
    }

    Menu.include({
        events: _.extend({
            // Clicking a hamburger menu item should close the hamburger
            "click .o_menu_sections [role=menuitem]": "_onClickMenuItem",
            // "click .o_main_navbar": "_onClickrightmenu",
            // "click .o_user_menu": "_onClickadmin",
            // "click .o_notification_second": "_onClickchat",
            // "click .o_notification_click": "_onClicknotif",
            // Opening any dropdown in the navbar should hide the hamburger
            "show.bs.dropdown .o_menu_systray, .o_menu_apps":
                "_hideMobileSubmenus",
            "hide.bs.dropdown .o_menu_systray, .o_menu_apps":
                "_hideMobileSubmenus",
        }, Menu.prototype.events),

        //  _onClickadmin : function(){
        //     console.log("_onClickadmin**00***");
        //     if($('.o_menu_apps .dropdown').hasClass( "show" )){
        //         if($('.o_user_menu .dropdown-menu').hasClass('show')){
        //             console.log("_onClickadmin**11***");
        //             $('.o_user_menu .dropdown-menu').removeClass('show');
        //                 // e.stopPropagation();
        //                 return false;
        //         }
        //         else{
        //             console.log("_onClickadmin**22***");
        //             $('.o_user_menu .dropdown-menu').addClass('show');
        //                 // e.stopPropagation();
        //                 return false;
        //         }
        //         }
        // },

        // _onClickchat : function(){
        //     console.log("_onClickchat**00***");
        //     if($('.o_menu_apps .dropdown').hasClass( "show" )){
        //         if($('.o_notification_second .dropdown-menu').hasClass('show')){
        //             $('.o_notification_second .dropdown-menu').removeClass('show');
        //                 // e.stopPropagation();
        //                 return false;
        //         }
        //         else{
        //             $('.o_notification_second .dropdown-menu').addClass('show');
        //                 // e.stopPropagation();
        //                 return false;
        //         }
        //     }
        // },

        // _onClicknotif : function(){
        //     console.log("_onClicknotif**00***");
        //     if($('.o_menu_apps .dropdown').hasClass( "show" )){
        //         if($('.o_notification_click .dropdown-menu').hasClass('show')){
        //             $('.o_notification_click .dropdown-menu').removeClass('show');
        //                 return false;
        //         }
        //         else{
        //             $('.o_notification_click .dropdown-menu').addClass('show');
        //                 return false;
        //         }
        //         }
        // },



        start: function () {
            var session = this.getSession();
            console.log("session@@@@@@@@@",session);

            var avatar_src_logo = session.url('/web/image', {
                model:'res.company',
                field: 'logo',
                id: session.user_context.allowed_company_ids[0],
            });
            var $avatar_logo = $('.o_sub_menu_logo');
            $avatar_logo.attr('src', avatar_src_logo);

            this._rpc({
                    model: 'res.company',
                    method: 'get_theme_colo',
                    args: [session.company_id]
                }).then(function(company_color){
                    console.log("company_color@@@@@@@@@@@@@@@@",$('.o_menu_apps .dropdown-menu'));
                    var $o_main_navbar = $('.o_main_navbar')[0].style.backgroundColor = company_color;
                    var $dropdown = $('.o_menu_apps .dropdown-menu')[0].style.background = company_color;

                    // .dropdown-item:hover, .dropdown-item:focus

                });

                    // function checkForUpdate()
                    // {
                    //     if (window.applicationCache != undefined && window.applicationCache != null)
                    //     {
                    //         window.applicationCache.addEventListener('updateready', updateApplication);
                    //     }
                    // }
                    // function updateApplication(event)
                    // {
                    //     if (window.applicationCache.status != 4) return;
                    //     window.applicationCache.removeEventListener('updateready', updateApplication);
                    //     window.applicationCache.swapCache();
                    //     window.location.reload();
                    // }


                // self = this;
                // var expir_date = $.ajax({
                //     type: 'GET',
                //     url: '/get/expire_date/',
                //     headers: {
                //             'Content-Type': 'application/x-www-form-urlencoded'
                //         },
                   
                //     async: false,
                //     dataType: 'json',
                //     data: {},
                //     done: function(results) {
                //         return results;
                //     },
                // }).responseJSON;

                // var expire_values = $.ajax({
                //     type: 'GET',
                //     url: '/get/expire_values/',
                //     headers: {
                //             'Content-Type': 'application/x-www-form-urlencoded'
                //         },
                   
                //     async: false,
                //     dataType: 'json',
                //     data: {},
                //     done: function(results) {
                //         return results;
                //     },
                // }).responseJSON;

                // this._rpc({
                //     model: 'upgrade.database',
                //     method: 'get_param_values',
                //     args: [1]
                // }).then(function(subscription_id){
                //     if((subscription_id === 'trial' && expire_values && expire_values != true && 'diffdays' in expire_values)){
                //         // $('.renew_form').removeClass('display');
                //         // $('.oe_register').removeClass('display');
                //         // $('.trialdb').removeClass('display');
                //         // $('.diffdays').text(expire_values.diffdays);
                //     }else if((subscription_id !== 'trial' && expire_values && expire_values != true && 'diffdays' in expire_values && 'period' in expire_values && expire_values.period === 'monthly' && expire_values.diffdays <= 15)){
                //         // $('.renew_form').removeClass('display');
                //         // $('.livedb').removeClass('display');
                //         // $('.diffdays').text(expire_values.diffdays);
                //         // $('.oe_renew').removeClass('display');
                //     }else if((subscription_id !== 'trial' && expire_values && expire_values != true && 'diffdays' in expire_values && 'period' in expire_values && expire_values.period === 'annually' && expire_values.diffdays <= 30)){
                //         // $('.renew_form').removeClass('display');
                //         // $('.livedb').removeClass('display');
                //         // $('.diffdays').text(expire_values.diffdays);
                //         // $('.oe_renew').removeClass('display');
                //     }else if(subscription_id === 'trial' && expire_values){
                //         var navc = $('.o_menu_apps')[0].childNodes[0].children;
                //         navc[0].click();
                //         // $('.o_main_navbar').addClass('displ');
                //         // $('.o_main_content').addClass('displcontent');
                //         // $('.o_user_menu').addClass('displuser');
                //         // $('.o_menu_apps').addClass('displuser');
                //         // $('.renew_form').removeClass('display');
                //         // $('.trialdbexpired').removeClass('display');
                //         // $('.oe_register').removeClass('display');
                //     }else if(expire_values && expire_values === true){
                //         var navc = $('.o_menu_apps')[0].childNodes[0].children;
                //         navc[0].click();
                //         // $('.o_main_navbar').addClass('displ');
                //         // $('.o_main_content').addClass('displcontent');
                //         // $('.o_user_menu').addClass('displuser');
                //         // $('.o_menu_apps').addClass('displuser');
                //         // $('.renew_form').removeClass('display');
                //         // $('.dbexpired').removeClass('display');
                //         // $('.oe_renew').removeClass('display');
                //     }

                //     if ((subscription_id !== 'trial' && expire_values && expire_values != true && 'ext_apps' in expire_values && 'ext_users' in expire_values)){
                //         if (expire_values.ext_apps === 'yes' && expire_values.ext_users === 'yes'){
                //             $('.extappuser').removeClass('display');
                //         }else if (expire_values.ext_apps === 'yes' && expire_values.ext_users === 'no'){
                //             $('.extapp').removeClass('display');
                //         }else if (expire_values.ext_apps === 'no' && expire_values.ext_users === 'yes'){
                //             $('.extuser').removeClass('display');
                //         }
                //     }
                                      
                // });

            this.$menu_toggle = this.$(".o-menu-toggle");
            // var apply = this._super.apply(this, arguments);
            var isMenuOpen = Session.get_cookie('isMenuOpen');

            if(isMenuOpen) {
              var clas = $('.o_menu_apps .dropdown').addClass('show');
              $('.o-menu-toggle').addClass('disp');
              $('.o_menu_apps .dropdown-menu').addClass('show');
            }

            setInterval(function() {
                if($('.o_menu_apps .dropdown').hasClass("show" )) {
                    Session.set_cookie('isMenuOpen', true);
                    //sessionStorage['manucheck'] = true;
                    $('.o_menu_systray .o_no_notification').removeClass('o_mail_systray_item');
                    $('.o_menu_sections').removeClass('visible');
                    $('.o_menu_brand').removeClass('visible');
                } else {
                    Session.set_cookie('isMenuOpen', false);
                    //sessionStorage['manucheck'] = false;
                    $('.o_menu_sections').addClass('visible');
                    $('.o_menu_systray .o_no_notification').addClass('o_mail_systray_item');
                    $('.o_menu_brand').addClass('visible');
                }
            }, 500)

            setInterval(function() {
                if($('.o_menu_apps .dropdown').hasClass( "show" )) {
                    $('.o_menu_sections').removeClass('visible');
                    $('.o-menu-toggle').addClass('disp')
                    $('.o_menu_systray .o_no_notification').removeClass('o_mail_systray_item');
                    $('.o_menu_brand').removeClass('visible');
                } else {
                 $('.o_menu_sections').addClass('visible');
                 $('.o-menu-toggle').removeClass('disp');
                 $('.o_menu_systray .o_no_notification').addClass('o_mail_systray_item');
                 $('.o_menu_brand').addClass('visible');
                }
            }, 0)

            return this._super.apply(this, arguments);
        },

        /**
         * Hide menus for current app if you're in mobile
         */
        _hideMobileSubmenus: function (ev) {

            if (
                config.device.isMobile &&
                this.$menu_toggle.is(":visible") &&
                this.$section_placeholder.is(":visible")
            ) {
                this.$section_placeholder.collapse("hide");
            }
            if($('.o_menu_apps .dropdown').hasClass( "show" )) {
                utils.set_cookie('home', false);
            }else{
                utils.set_cookie('home', true);
            }
            var isMenuOpen = Session.get_cookie('isMenuOpen');
            if (!config.device.isMobile) {

                if(isMenuOpen) {
                    $('.o_menu_apps .dropdown').addClass('show');
                    $('.o_menu_apps .dropdown-menu').addClass('show');
                     ev.stopPropagation();
                }
            }
            else{
                if(isMenuOpen) {
                    $('.o_menu_apps .dropdown').addClass('show');
                    $('.o_menu_apps .dropdown-menu').addClass('show');
                    ev.stopPropagation();
                }
            }
        },

        /**
         * Prevent hide the menu (should be closed when action is loaded)
         *
         * @param {ClickEvent} ev
         */
        _onClickMenuItem: function (ev) {
            ev.stopPropagation();
        },

        // _onClickrightmenu: function(ev) {
        //     console.log("_onClickrightmenu**00***");
        //     // if($('.o_menu_apps .dropdown').hasClass( "show" )){
        //     //     ev.stopPropagation(); 
        //     // }
        //     var isMenuOpen = Session.get_cookie('isMenuOpen');
        //     if (!config.device.isMobile) {
        //         console.log("isMenuOpen**00***",isMenuOpen);
        //         if (isMenuOpen){
        //              ev.stopPropagation(); 
        //         }
        //     }
        // },

        /**
         * No menu brand in mobiles
         *
         * @override
         */
        _updateMenuBrand: function () {
            if (!config.device.isMobile) {
                var isMenuOpen = Session.get_cookie('isMenuOpen');
                var home = utils.get_cookie('home');
                if(isMenuOpen || isMenuOpen == null) {
                  var clas = $('.o_menu_apps .dropdown').addClass('show');
                  $('.o-menu-toggle').addClass('disp');
                  $('.o_menu_apps .dropdown-menu').addClass('show');
                }
                else if(home == 'true' || home != 'false') {
                  var clas = $('.o_menu_apps .dropdown').addClass('show');
                  $('.o-menu-toggle').addClass('disp');
                  $('.o_menu_apps .dropdown-menu').addClass('show');
                }
                return this._super.apply(this, arguments);
            }

            
            if(config.device.isMobile){
                $('.o_menu_apps .dropdown').addClass('show');
              $('.o-menu-toggle').addClass('disp');
              $('.o_menu_apps .dropdown-menu').addClass('show');
            }
        },
    });

    AppsMenu.include({
        events: _.extend({
            "keydown .search-input input": "_searchResultsNavigate",
            "input .search-input input": "_searchMenusSchedule",
            "click .o-menu-search-result": "_searchResultChosen",
            "shown.bs.dropdown": "_searchFocus",
            "hidden.bs.dropdown": "_searchReset",
            "hide.bs.dropdown": "_hideAppsMenu",
        }, AppsMenu.prototype.events),

        /**
         * Rescue some menu data stripped out in original method.
         *
         * @override
         */
        init: function (parent, menuData) {
            this._super.apply(this, arguments);
            // Keep base64 icon for main menus
            for (var n in this._apps) {
                this._apps[n].web_icon_data =
                    menuData.children[n].web_icon_data;
            }
            // Store menu data in a format searchable by fuzzy.js
            this._searchableMenus = _.reduce(
                menuData.children,
                findNames,
                {}
            );
            // Search only after timeout, for fast typers
            this._search_def = $.Deferred();
        },

        /**
         * @override
         */
        start: function () {
            this.$search_container = this.$(".search-container");
            this.$search_input = this.$(".search-input input");
            this.$search_results = this.$(".search-results");
            return this._super.apply(this, arguments);
        },

        /**
         * Prevent the menu from being opened twice
         *
         * @override
         */
        _onAppsMenuItemClicked: function (ev) {
            this._super.apply(this, arguments);
            ev.preventDefault();
            ev.stopPropagation();
        },

        /**
         * Get all info for a given menu.
         *
         * @param {String} key
         * Full path to requested menu.
         *
         * @returns {Object}
         * Menu definition, plus extra needed keys.
         */
        _menuInfo: function (key) {
            var original = this._searchableMenus[key];
            return _.extend({
                action_id: parseInt(original.action.split(',')[1], 10),
            }, original);
        },

        /**
         * Autofocus on search field on big screens.
         */
        _searchFocus: function () {
            if (!config.device.isMobile) {
                this.$search_input.focus();
            }
        },

        /**
         * Reset search input and results
         */
        _searchReset: function () {
            this.$search_container.removeClass("has-results");
            this.$search_results.empty();
            this.$search_input.val("");
        },

        /**
         * Schedule a search on current menu items.
         */
        _searchMenusSchedule: function () {
            this._search_def.reject();
            this._search_def = $.Deferred();
            setTimeout(this._search_def.resolve.bind(this._search_def), 50);
            this._search_def.done(this._searchMenus.bind(this));
        },

        /**
         * Search among available menu items, and render that search.
         */
        _searchMenus: function () {
            var query = this.$search_input.val();
            if (query === "") {
                this.$search_container.removeClass("has-results");
                this.$search_results.empty();
                return;
            }
            var results = fuzzy.filter(
                query,
                _.keys(this._searchableMenus),
                {
                    pre: "<b>",
                    post: "</b>",
                }
            );
            this.$search_container.toggleClass(
                "has-results",
                Boolean(results.length)
            );
            this.$search_results.html(
                core.qweb.render(
                    "web_responsive.MenuSearchResults",
                    {
                        results: results,
                        widget: this,
                    }
                )
            );
        },

        /**
         * Use chooses a search result, so we navigate to that menu
         *
         * @param {jQuery.Event} event
         */
        _searchResultChosen: function (event) {
            event.preventDefault();
            event.stopPropagation();
            var $result = $(event.currentTarget),
                text = $result.text().trim(),
                data = $result.data(),
                suffix = ~text.indexOf("/") ? "/" : "";
            // Load the menu view
            this.trigger_up("menu_clicked", {
                action_id: data.actionId,
                id: data.menuId,
                previous_menu_id: data.parentId,
            });
            // Find app that owns the chosen menu
            var app = _.find(this._apps, function (_app) {
                return text.indexOf(_app.name + suffix) === 0;
            });
            // Update navbar menus
            core.bus.trigger("change_menu_section", app.menuID);
        },

        /**
         * Navigate among search results
         *
         * @param {jQuery.Event} event
         */
        _searchResultsNavigate: function (event) {
            // Find current results and active element (1st by default)
            var all = this.$search_results.find(".o-menu-search-result"),
                pre_focused = all.filter(".active") || $(all[0]),
                offset = all.index(pre_focused),
                key = event.key;
            // Keyboard navigation only supports search results
            if (!all.length) {
                return;
            }
            // Transform tab presses in arrow presses
            if (key === "Tab") {
                event.preventDefault();
                key = event.shiftKey ? "ArrowUp" : "ArrowDown";
            }
            switch (key) {
            // Pressing enter is the same as clicking on the active element
            case "Enter":
                pre_focused.click();
                break;
            // Navigate up or down
            case "ArrowUp":
                offset--;
                break;
            case "ArrowDown":
                offset++;
                break;
            default:
                // Other keys are useless in this event
                return;
            }
            // Allow looping on results
            if (offset < 0) {
                offset = all.length + offset;
            } else if (offset >= all.length) {
                offset -= all.length;
            }
            // Switch active element
            var new_focused = $(all[offset]);
            pre_focused.removeClass("active");
            new_focused.addClass("active");
            this.$search_results.scrollTo(new_focused, {
                offset: {
                    top: this.$search_results.height() * -0.5,
                },
            });
        },

        /*
        * Control if AppDrawer can be closed
        */
        _hideAppsMenu: function () {
            return !this.$('input').is(':focus');
        },
    });

    BasicController.include({

        /**
         * Close the AppDrawer if the data set is dirty and a discard dialog
         * is opened
         *
         * @override
         */
        canBeDiscarded: function (recordID) {
            if (this.model.isDirty(recordID || this.handle)) {
                closeAppDrawer();
            }
            return this._super.apply(this, arguments);
        },
    });

    RelationalFields.FieldStatus.include({

        /**
         * Fold all on mobiles.
         *
         * @override
         */
        _setState: function () {
            this._super.apply(this, arguments);
            if (config.device.isMobile) {
                _.map(this.status_information, function (value) {
                    value.fold = true;
                });
            }
        },
    });

    // Responsive view "action" buttons
    FormRenderer.include({

        /**
         * In mobiles, put all statusbar buttons in a dropdown.
         *
         * @override
         */
        _renderHeaderButtons: function () {
            var $buttons = this._super.apply(this, arguments);
            if (
                !config.device.isMobile ||
                !$buttons.is(":has(>:not(.o_invisible_modifier))")
            ) {
                return $buttons;
            }

            // $buttons must be appended by JS because all events are bound
            $buttons.addClass("dropdown-menu");
            var $dropdown = $(core.qweb.render(
                'web_responsive.MenuStatusbarButtons'
            ));
            $buttons.addClass("dropdown-menu").appendTo($dropdown);
            return $dropdown;
        },
    });

    // Chatter Hide Composer
    // Chatter.include({
    //     _openComposer: function (options) {
    //         if (this._composer &&
    //                 options.isLog === this._composer.options.isLog &&
    //                 this._composer.$el.is(':visible')) {
    //             this._closeComposer(false);
    //         } else {
    //             this._super.apply(this, arguments);
    //         }
    //     },
    // });

    // Hide AppDrawer or Menu when the action has been completed
    ActionManager.include({

        /**
        * @override
        */
        _appendController: function () {
            this._super.apply(this, arguments);
             // @oleksiipavlenko
            if(!first) {
                closeAppDrawer();
            } else {
                first = false;
            }
        },
    });

    /**
     * Use ALT+SHIFT instead of ALT as hotkey triggerer.
     *
     * HACK https://github.com/odoo/odoo/issues/30068 - See it to know why.
     *
     * Cannot patch in `KeyboardNavigationMixin` directly because it's a mixin,
     * not a `Class`, and altering a mixin's `prototype` doesn't alter it where
     * it has already been used.
     *
     * Instead, we provide an additional mixin to be used wherever you need to
     * enable this behavior.
     */
    var KeyboardNavigationShiftAltMixin = {

        /**
         * Alter the key event to require pressing Shift.
         *
         * This will produce a mocked event object where it will seem that
         * `Alt` is not pressed if `Shift` is not pressed.
         *
         * The reason for this is that original upstream code, found in
         * `KeyboardNavigationMixin` is very hardcoded against the `Alt` key,
         * so it is more maintainable to mock its input than to rewrite it
         * completely.
         *
         * @param {keyEvent} keyEvent
         * Original event object
         *
         * @returns {keyEvent}
         * Altered event object
         */
        _shiftPressed: function (keyEvent) {
            var alt = keyEvent.altKey || keyEvent.key === "Alt",
                newEvent = _.extend({}, keyEvent),
                shift = keyEvent.shiftKey || keyEvent.key === "Shift";
            // Mock event to make it seem like Alt is not pressed
            if (alt && !shift) {
                newEvent.altKey = false;
                if (newEvent.key === "Alt") {
                    newEvent.key = "Shift";
                }
            }
            return newEvent;
        },

        _onKeyDown: function (keyDownEvent) {
            return this._super(this._shiftPressed(keyDownEvent));
        },

        _onKeyUp: function (keyUpEvent) {
            return this._super(this._shiftPressed(keyUpEvent));
        },
    };

    // Include the SHIFT+ALT mixin wherever
    // `KeyboardNavigationMixin` is used upstream
    AbstractWebClient.include(KeyboardNavigationShiftAltMixin);

    // DocumentViewer: Add support to maximize/minimize
    // DocumentViewer.include({
    //     // Widget 'keydown' and 'keyup' events are only dispatched when
    //     // this.$el is active, but now the modal have buttons that can obtain
    //     // the focus. For this reason we now listen core events, that are
    //     // dispatched every time.
    //     events: _.extend(_.omit(DocumentViewer.prototype.events, [
    //         'keydown',
    //         'keyup',
    //     ]), {
    //         'click .o_maximize_btn': '_onClickMaximize',
    //         'click .o_minimize_btn': '_onClickMinimize',
    //         'shown.bs.modal': '_onShownModal',
    //     }),

    //     start: function () {
    //         core.bus.on('keydown', this, this._onKeydown);
    //         core.bus.on('keyup', this, this._onKeyUp);
    //         return this._super.apply(this, arguments);
    //     },

    //     destroy: function () {
    //         core.bus.off('keydown', this, this._onKeydown);
    //         core.bus.off('keyup', this, this._onKeyUp);
    //         this._super.apply(this, arguments);
    //     },

    //     _onShownModal: function () {
    //         // Disable auto-focus to allow to use controls in edit mode.
    //         // This only affects the active modal.
    //         // More info: https://stackoverflow.com/a/14795256
    //         $(document).off('focusin.modal');
    //     },
    //     _onClickMaximize: function () {
    //         this.$el.removeClass('o_responsive_document_viewer');
    //     },
    //     _onClickMinimize: function () {
    //         this.$el.addClass('o_responsive_document_viewer');
    //     },
    // });
});
