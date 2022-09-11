odoo.define('fx.ControlPanelRenderer', function (require) {
    "use strict";

    var TimeRangeMenu = require('web.TimeRangeMenu');
    var ControlPanelRenderer = require('web.ControlPanelRenderer')

    var mvc = require('web.mvc');
    var Renderer = mvc.Renderer;

    var FilterPannel = require('fx.FilterPannel')
    var GroupByPannel = require('fx.groupByPannel')
    var FavoritePannel = require('fx.FavoritePannel')

    var core = require('web.core')
    var tab_id = 8526

    var fxControlPanelRenderer = ControlPanelRenderer.include({
        template: 'fx_control_pannel',

        custom_events: {
            close_search_option_pannel: '_close_search_option_pannel'
        },

        start: function () {

            // exposed jQuery nodesets
            this.nodes = {
                $buttons: this.$('.o_cp_buttons'),
                $pager: this.$('.o_cp_pager'),
                $sidebar: this.$('.o_cp_sidebar'),
                $switch_buttons: this.$('.o_cp_switch_buttons'),
            };

            // if we don't use the default search bar and buttons, we expose the
            // corresponding areas for custom content
            if (!this.withSearchBar) {
                this.nodes.$searchview = this.$('.o_cp_searchview');
            }

            if (this.searchMenuTypes.length === 0) {
                this.nodes.$searchview_buttons = this.$('.o_search_options');
            }

            if (this.withBreadcrumbs) {
                this._renderBreadcrumbs();
            }

            var superDef = Renderer.prototype.start.apply(this, arguments);
            var searchDef = this._renderSearch();

            // global click
            var self = this;
            core.bus.on('click', this, function (event) {
                var target = $(event.target)
                if (!target.is('.o_searchview_more') && target.parents('.fx_search_options').length == 0) {
                    self.displaySearchMenu = false
                    self._setSearchMenusVisibility()
                }
            })

            // breadcrumb clicked
            core.bus.on('fx_theme.breadcrumb_clicked', this, function (data) {
                var controllerID = data
                self.trigger_up('breadcrumb_clicked', {controllerID: controllerID});
            })

            return Promise.all([superDef, searchDef]).then(function() {
                self.displaySearchMenu = false
                self._setSearchMenusVisibility()
            })
        },

        _renderBreadcrumbs: function () {
            var breadcrumbsDescriptors = this._breadcrumbs.concat({ title: this._title });
            core.bus.trigger('update_bread_crumbs', breadcrumbsDescriptors);
        },

        _setSearchMenusVisibility: function () {
            this.$('.o_searchview_more')
                .toggleClass('fa-search-plus', !this.displaySearchMenu)
                .toggleClass('fa-search-minus', this.displaySearchMenu);
            this.$('.fx_search_options')
                .toggleClass('o_hidden', !this.displaySearchMenu);
        },

        updateContents: function (status, options) {
            var new_cp_content = status.cp_content || {};
            var clear = 'clear' in (options || {}) ? options.clear : true;

            if (this.withBreadcrumbs) {
                this._breadcrumbs = status.breadcrumbs || this._breadcrumbs;
                this._title = status.title || this._title;
                this._renderBreadcrumbs();
            }

            if (clear) {
                this._detachContent(this.nodes);
            } else {
                this._detachContent(_.pick(this.nodes, _.keys(new_cp_content)));
            }
            this._attachContent(new_cp_content);
        },

        _attachContent: function (content) {
            for (var $element in content) {
                if ($element == '$switch_buttons') {
                    core.bus.trigger('fx_update_switcher', content[$element]);
                } else if ($element == '$pager') {
                    core.bus.trigger('fx_update_pager', content[$element]);
                } else {
                    var $nodeset = content[$element];
                    if ($nodeset && this.nodes[$element]) {
                        this.nodes[$element].append($nodeset);
                    }
                }
            }
        },

        _detachContent: function (content) {
            for (var $element in content) {
                if ($element == '$switch_buttons') {
                    core.bus.trigger('fx_clear_switcher', content[$element]);
                } else if ($element == '$pager') {
                    core.bus.trigger('fx_clear_pager', content[$element]);
                } else {
                    content[$element].contents().detach();
                }
            }
        },

        _setupMenu: function (menuType) {
            var bodyContainer = undefined
            var tab_length = this.$('.fx-tab-header .nav_item').length
            if (_.contains(['filter', 'groupBy', 'timeRange', 'favorite'], menuType)) {
                bodyContainer = this._addTab(menuType, tab_length)
            }

            var widget = undefined;
            switch (menuType) {
                case 'filter':
                    widget = new FilterPannel(this, this._getMenuItems(menuType), this.state.fields)
                    break

                case 'groupBy':
                    widget = new GroupByPannel(this, this._getMenuItems(menuType), this.state.fields)
                    break

                case 'timeRange':
                    widget = new TimeRangeMenu(this, this._getMenuItems(menuType), this.state.fields)
                    break

                case 'favorite':
                    widget = new FavoritePannel(this, this._getMenuItems(menuType), this.action);
                    break
            }

            if (bodyContainer && widget) {
                widget.appendTo(bodyContainer);
            }

            this.subMenus[menuType] = widget;
        },

        _updateMenus: function () {
            var self = this;
            this.searchMenuTypes.forEach(function (menuType) {
                self.subMenus[menuType].update(self._getMenuItems(menuType));
            });
        },

        _addTab: function (tab_name) {
            var length = this.$('.fx-tab-body .tab-pane').length
            var tmp_id = tab_id++
            var $tab_header = $(core.qweb.render('fx.search_option_tab_header',
                { tab_id: tmp_id, tab_name: tab_name }))
            if (length == 0) {
                $tab_header.find('a').addClass('active')
            }
            $tab_header.appendTo(this.$('.fx-tab-header'))
            var $tab_body = $(core.qweb.render('fx.search_option_tab_content',
                { tab_id: tmp_id, tab_name: tab_name }))
            if (length == 0) {
                $tab_body.addClass('active')
                $tab_body.addClass('show')
            }
            $tab_body.appendTo(this.$('.fx-tab-body'))
            return $tab_body
        },

        _close_search_option_pannel: function() {
            self.displaySearchMenu = false
            this._setSearchMenusVisibility()
        }
    });

    return fxControlPanelRenderer;
});
