odoo.define('fx.groupByPannel', function (require) {
    "use strict";

    var config = require('web.config');
    var controlPanelViewParameters = require('web.controlPanelViewParameters');
    var core = require('web.core');

    var PannelBase = require("fx.PannelBase")

    var DEFAULT_INTERVAL = controlPanelViewParameters.DEFAULT_INTERVAL;
    var GROUPABLE_TYPES = controlPanelViewParameters.GROUPABLE_TYPES;
    var INTERVAL_OPTIONS = controlPanelViewParameters.INTERVAL_OPTIONS;

    var groupByPannel = PannelBase.extend({
        template: 'fx.group_by_content',

        events: _.extend({}, PannelBase.prototype.events, {
            'click button.o_apply_group': '_onButtonApplyClick',
            'click .o_group_selector': '_onGroupSelectorClick',
        }),

        init: function (parent, groupBys, fields, options) {
            var self = this;
            options = options || {};
            this._super(parent, groupBys);
            this.fields = fields;

            // determines list of options used by groupBys of type 'date'
            this.groupableFields = [];
            _.each(fields, function (field, name) {
                if (field.sortable && name !== "id" && _.contains(GROUPABLE_TYPES, field.type)) {
                    self.groupableFields.push(_.extend({}, field, {
                        name: name,
                    }));
                }
            });
            this.groupableFields = _.sortBy(this.groupableFields, 'string');
            // determines the list of field names that can be added to the menu
            // via the 'Add Custom Groupby' menu
            this.presentedFields = this._setPresentedFields(groupBys);

            // determines where the filter menu is displayed and partly its style
            this.isMobile = config.device.isMobile;

            INTERVAL_OPTIONS = INTERVAL_OPTIONS.map(function (option) {
                return _.extend(option, { description: option.description.toString() });
            });
        },

        start: function () {
            var superProm = this._super.apply(this, arguments);
            this._renderContent();
            return superProm;
        },

        update: function (groupBys) {
            this._super.apply(this, arguments)
            this.presentedFields = this._setPresentedFields(groupBys);
        },

        _addGroupby: function (fieldName) {
            var field = this.presentedFields.find(function (field) {
                return field.name === fieldName;
            });
            var groupBy = {
                type: 'groupBy',
                description: field.string,
                fieldName: fieldName,
                fieldType: field.type,
            };
            if (_.contains(['date', 'datetime'], field.type)) {
                groupBy.hasOptions = true;
                groupBy.options = INTERVAL_OPTIONS;
                groupBy.defaultOptionId = DEFAULT_INTERVAL;
                groupBy.currentOptionIds = new Set([]);
            }
            this.trigger_up('new_groupBy', groupBy);
        },

        _renderMenuItems: function () {
            if (this.$el) {
                var group_items_container = this.$('.group-items-container')
                group_items_container.empty()
                var grouItems = $(core.qweb.render('DropdownMenu.MenuItems', { widget: this }))
                grouItems.appendTo(group_items_container)
            }
        },

        _renderContent: function () {
            this.$addCustomGroup = this.$('.o_add_custom_group');
            this.$groupSelector = this.$('.o_group_selector');
        },

        _setPresentedFields: function (groupBys) {
            return this.groupableFields.filter(function (field) {
                var groupByFields = _.pluck(groupBys, 'fieldName');
                return !_.contains(groupByFields, field.name);
            });
        },

        _toggleCustomGroupMenu: function () {
            this.generatorMenuIsOpen = !this.generatorMenuIsOpen;
            this._renderContent();
            if (this.generatorMenuIsOpen) {
                this.$groupSelector.focus();
            }
        },

        _onButtonApplyClick: function (ev) {
            ev.stopPropagation();
            var fieldName = this.$groupSelector.val();
            this.generatorMenuIsOpen = false;
            this._addGroupby(fieldName);
        },

        _onGroupSelectorClick: function (ev) {
            ev.stopPropagation();
        }
    });

    return groupByPannel;
});
