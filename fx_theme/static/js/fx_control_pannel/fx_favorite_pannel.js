odoo.define('fx.FavoritePannel', function (require) {
    "use strict";

    var config = require('web.config');
    var core = require('web.core');
    var Dialog = require('web.Dialog');
    var favorites_submenus_registry = require('web.favorites_submenus_registry');
    var Widget = require('web.Widget')

    var _t = core._t;

    var FavoritePannel = Widget.extend({
        template: "fx.favorite_pannel",

        events: _.extend({}, Widget.prototype.events, {
            'click .o_menu_item': '_onItemClick',
            'click .o_item_option': '_onOptionClick',
            'click span.o_trash_button': '_onTrashButtonClick'
        }),

        custom_events: _.extend({}, Widget.prototype.custom_events, {
            favorite_submenu_toggled: '_onSubMenuToggled',
        }),

        init: function (parent, favorites, action) {
            this.items = favorites
            this.action = action;
            this.isMobile = config.device.isMobile;
            this._super(parent, favorites);
        },

        start: function () {
            var self = this;
            var params = {
                favorites: this.items,
                action: this.action,
            };
            var superProm = this._super.apply(this, arguments);
            this._renderFavorites()
            this.subMenus = [];
            favorites_submenus_registry.values().forEach(function (SubMenu) {
                var subMenu = new SubMenu(self, params);
                subMenu.appendTo(self.$('.widget_container'));
                self.subMenus.push(subMenu);
            });
            return superProm;
        },

        _closeSubMenus: function () {
            _.invoke(this.subMenus, 'closeMenu');
        },

        _onSubMenuToggled: function (ev) {
            ev.stopPropagation();
        },

        _renderFavorites: function() {
            if (this.$el) {
                var favoritor_container = this.$('.favorite-container')
                favoritor_container.empty()
                var filterItems = $(core.qweb.render('DropdownMenu.MenuItems', {widget: this}))
                filterItems.appendTo(favoritor_container)
            }
        },

        _onTrashButtonClick: function (event) {
            
            event.preventDefault();
            event.stopPropagation();

            var self = this;
            var id = $(event.currentTarget).data('id');
            var favorite = this.items.find(function (favorite) {
                return favorite.id === id;
            });
            var globalWarning = _t("This filter is global and will be removed for everybody if you continue.");
            var warning = _t("Are you sure that you want to remove this filter?");
            var message = favorite.userId ? warning : globalWarning;

            Dialog.confirm(self, message, {
                title: _t("Warning"),
                confirm_callback: function () {
                    self.trigger_up('item_trashed', { id: id });
                },
            });
        },

        _onOptionClick: function (event) {
            event.preventDefault();
            event.stopPropagation();
            var optionId = $(event.currentTarget).data('option_id');
            var id = $(event.currentTarget).data('item_id');
            this.trigger_up('item_option_clicked', { id: id, optionId: optionId });
        },


        update: function (favorites) {
            this.items = favorites;
            this._renderFavorites();
            _.invoke(this.subMenus, 'update', { favorites: this.items });
        },

        _onItemClick: function (event) {
            event.preventDefault();
            event.stopPropagation();
    
            var id = $(event.currentTarget).data('id');
            var item = this.items.find(function (item) {
                return item.id === id;
            });
            if (item.hasOptions) {
                this.openItems[id] = !this.openItems[id];
                this._renderMenuItems();
            } else {
                this.trigger_up('menu_item_clicked', {id: id});
            }
        },
    });

    return FavoritePannel;
});