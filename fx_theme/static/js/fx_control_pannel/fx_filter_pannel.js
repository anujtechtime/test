odoo.define('fx.FilterPannel', function (require) {
    "use strict";

    var config = require('web.config');
    var core = require('web.core');
    var Domain = require('web.Domain');
    var search_filters = require('web.search_filters');
    var PannelBase = require("fx.PannelBase")

    var FilterPannel = PannelBase.extend({
        template: "FilterPannel",

        custom_events: {
            confirm_proposition: '_onConfirmProposition',
            remove_proposition: '_onRemoveProposition',
        },

        events: _.extend({}, PannelBase.prototype.events, {
            'click .o_add_condition': '_onAddCondition',
            'click .o_apply_filter': '_onApplyClick',
            'click .dropdown-item-text': '_onDropDownItemTextClick',
        }),

        init: function (parent, filters, fields) {
            this._super(parent, filters);

            // determines where the filter menu is displayed and its style
            this.isMobile = config.device.isMobile;
            this.propositions = [];
            this.fields = _.pick(fields, function (field, name) {
                return field.selectable !== false && name !== 'id';
            });

            this.fields.id = { string: 'ID', type: 'id', searchable: true };
        },

        start: function () {
            var superProm = this._super.apply(this, arguments);

            // add one by default
            if (!this.propositions.length)
                this._appendProposition();

            this._renderMenuItems()
            return superProm;
        },

        _renderMenuItems: function () {
            if (this.$el) {
                var filter_container = this.$('.filter_container')
                filter_container.empty()
                var filterItems = $(core.qweb.render('DropdownMenu.MenuItems', {widget: this}))
                filterItems.appendTo(filter_container)
            }
        },

        _appendProposition: function () {
            // make modern sear_filters code!!! It works but...
            var prop = new search_filters.ExtendedSearchProposition(this, this.fields);
            this.propositions.push(prop);
            this.$('.o_apply_filter').prop('disabled', false);
            return prop.appendTo(this.$('.propation_container'))
        },

        _commitSearch: function () {
            var filters = _.invoke(this.propositions, 'get_filter').map(function (preFilter) {
                return {
                    type: 'filter',
                    description: preFilter.attrs.string,
                    domain: Domain.prototype.arrayToString(preFilter.attrs.domain),
                };
            });
            this.trigger_up('new_filters', { filters: filters });
            _.invoke(this.propositions, 'destroy');
            this.propositions = [];
        },

        _onAddCondition: function (ev) {
            ev.stopPropagation();
            this._appendProposition();
        },

        _onApplyClick: function (ev) {
            ev.stopPropagation();
            this._commitSearch();
        },

        _onConfirmProposition: function (ev) {
            ev.stopPropagation();
            this._commitSearch();
        },

        _onRemoveProposition: function (ev) {
            ev.stopPropagation();
            this.propositions = _.without(this.propositions, ev.target);
            if (!this.propositions.length) {
                this.$('.o_apply_filter').prop('disabled', true);
            }
            ev.target.destroy();
        },

        update: function (filters) {
            this._super.apply(this, arguments);
            // save the old select items
            this._renderMenuItems();
        }
    });

    return FilterPannel;
});
