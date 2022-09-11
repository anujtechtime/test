odoo.define('fx.many2one', function (require) {
    "use strict";

    var relational_fields = require('web.relational_fields');
    var core = require('web.core');
    var dialogs = require('web.view_dialogs');

    var _t = core._t;

    /**
     * extend to add the dropdown arrow
     */
    relational_fields.FieldMany2One.include({

        init: function () {
            this._super.apply(this, arguments);
            if (this.attrs.options && this.attrs.options.limit) {
                this.limit = this.attrs.options.limit
            }
        },

        /**
         * rotate the arrow when search
         */
        _onInputClick: function () {
            if (this.attrs.options && this.attrs.options.direct_search) {
                this.direct_search()
            } else {
                if (this.$input.autocomplete("widget").is(":visible")) {
                    this.$input.autocomplete("close");
                    this.$(".o_dropdown_arrow").addClass("fx-reverse")
                } else if (this.floating) {
                    this.$(".o_dropdown_arrow").removeClass("fx-reverse")
                    this.$input.autocomplete("search"); // search with the input's content
                } else {
                    this.$(".o_dropdown_arrow").removeClass("fx-reverse")
                    this.$input.autocomplete("search", ''); // search with the empty string
                }
            }
        },

        _searchCreatePopup: function (view, ids, context) {
            var self = this;
            return new dialogs.SelectCreateDialog(this, _.extend({}, this.nodeOptions, {
                res_model: this.field.relation,
                domain: this.record.getDomain({fieldName: this.name}),
                context: _.extend({}, this.record.getContext(this.recordParams), context || {}),
                title: (view === 'search' ? _t("Search: ") : _t("Create: ")) + this.string,
                initial_ids: ids ? _.map(ids, function (x) { return x[0]; }) : undefined,
                initial_view: view,
                js_class: this.attrs.options.js_class || undefined,
                disable_multiple_selection: true,
                no_create: !self.can_create,
                on_selected: function (records) {
                    self.reinitialize(records[0]);
                    self.activate();
                }
            })).open();
        },

        direct_search: function () {
            var self = this;
            var def = $.Deferred();
            this.orderer.add(def);

            var context = this.record.getContext(this.recordParams);
            var domain = this.record.getDomain(this.recordParams);

            // Add the additionalContext
            _.extend(context, this.additionalContext);

            var blacklisted_ids = this._getSearchBlacklist();
            if (blacklisted_ids.length > 0) {
                domain.push(['id', 'not in', blacklisted_ids]);
            }

            // Clear the value in case the user clicks on discard
            self.$('input').val('');
            return self._searchCreatePopup("search");
        },


        reinitialize: function (value) {
            this._super(value);
            this.$(".o_dropdown_arrow").addClass("fx-reverse")
        },
        
        /**
         * rewrite to support custom js_class
         * @param {*} view 
         * @param {*} ids 
         * @param {*} context 
         */
        _searchCreatePopup: function (view, ids, context) {
            var self = this;
            return new dialogs.SelectCreateDialog(this, _.extend({}, this.nodeOptions, {
                res_model: this.field.relation,
                domain: this.record.getDomain({ fieldName: this.name }),
                context: _.extend({}, this.record.getContext(this.recordParams), context || {}),
                title: (view === 'search' ? _t("Search: ") : _t("Create: ")) + this.string,
                initial_ids: ids ? _.map(ids, function (x) { return x[0]; }) : undefined,
                initial_view: view,
                js_class: this.attrs.options.pop_list_js_class || undefined,
                disable_multiple_selection: true,
                no_create: !self.can_create,
                on_selected: function (records) {
                    self.reinitialize(records[0]);
                    self.activate();
                }
            })).open();
        },

            /**
         * @private
         */
        _bindAutoComplete: function () {
            var self = this;

            // avoid ignoring autocomplete="off" by obfuscating placeholder, see #30439
            if (this.$input.attr('placeholder')) {
                this.$input.attr('placeholder', function (index, val) {
                    return val.split('').join('\ufeff');
                });
            }

            this.$input.autocomplete({
                source: function (req, resp) {
                    _.each(self._autocompleteSources, function (source) {
                        // Resets the results for this source
                        source.results = [];

                        // Check if this source should be used for the searched term
                        if (!source.validation || source.validation.call(self, req.term)) {
                            source.loading = true;

                            // Wrap the returned value of the source.method with $.when.
                            // So event if the returned value is not async, it will work
                            $.when(source.method.call(self, req.term)).then(function (results) {
                                source.results = results;
                                source.loading = false;
                                resp(self._concatenateAutocompleteResults());
                            });
                        }
                    });
                },

                select: function (event, ui) {
                    // we do not want the select event to trigger any additional
                    // effect, such as navigating to another field.
                    event.stopImmediatePropagation();
                    event.preventDefault();

                    var item = ui.item;
                    self.floating = false;
                    if (item.id) {
                        self.reinitialize({ id: item.id, display_name: item.name });
                    } else if (item.action) {
                        item.action();
                    }
                    return false;
                },

                focus: function (event) {
                    event.preventDefault(); // don't automatically select values on focus
                },

                close: function (event) {
                    self.$(".o_dropdown_arrow").addClass("fx-reverse")
                    // it is necessary to prevent ESC key from propagating to field
                    // root, to prevent unwanted discard operations.
                    if (event.which === $.ui.keyCode.ESCAPE) {
                        event.stopPropagation();
                    }
                },
                autoFocus: true,
                html: true,
                minLength: 0,
                delay: this.AUTOCOMPLETE_DELAY,
            });

            this.$input.autocomplete("option", "position", { my: "left top-110", at: "left bottom+110" });
            this.autocomplete_bound = true;
        }
    });
});