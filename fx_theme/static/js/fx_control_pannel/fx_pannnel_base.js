odoo.define('fx.PannelBase', function (require) {
    "use strict";

    var core = require('web.core');
    var Widget = require('web.Widget');

    var PannelBase = Widget.extend({
        events: {
            'click .o_menu_item': '_onItemClick',
            'click .o_item_option': '_onOptionClick',
            'click span.o_trash_button': '_onTrashButtonClick',
            'click .dropdown-item-text': '_onDropDownItemTextClick',
        },

        init: function (parent, items) {
            this._super(parent);

            this.items = items;
            this.openItems = {};
        },

        start: function () {
            var self = this
            return this._super.apply(this, arguments).then(function(){
                self._renderMenuItems()
            });
        },

        update: function (items) {
            this.items = items;
            this._renderMenuItems()
        },

        _renderMenuItems: function () {
            console.log('the render menu item function is not imply!')
        },

        _onDropDownItemTextClick: function (ev) {
            ev.stopPropagation();
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
                this.trigger_up('menu_item_clicked', { id: id });
            }
        },

        _onOptionClick: function (event) {
            event.preventDefault();
            event.stopPropagation();
            var optionId = $(event.currentTarget).data('option_id');
            var id = $(event.currentTarget).data('item_id');
            this.trigger_up('item_option_clicked', { id: id, optionId: optionId });
        },

        _onTrashButtonClick: function (event) {

        }
    });

    return PannelBase;
});