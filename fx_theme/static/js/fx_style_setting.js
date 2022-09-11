odoo.define('fx.StyleSetting', function (require) {
    "use strict";

    var SystrayMenu = require('web.SystrayMenu');
    var Widget = require('web.Widget');
    var core = require('web.core')
    var pyUtils = require('web.py_utils');

    var StyleSetting = Widget.extend({
        template: 'fx.style_setting_extend',
        sequence: 0,
        items: [],

        events: _.extend({}, Widget.prototype.events, {
            "click .customizer-toggler": "_on_customizer_toggler_click",
            "click .customizer-close": "_on_customizer_close_click",
            "click .operation-toolbar .delete_btn": "_on_delete_theme_style",
            "click .save-btn": "_on_save_btn_click",
            "click .cancel-btn": "_on_cancel_btn_click",
            "click .reset-btn": "_on_reset_btn_click",
            "click .preview-btn": "_on_preview_btn_click",
            "click .add_new_style": "_on_add_new_style",
            "click .delete_style": "_on_delete_style",
            "change .theme-mode-radio": "_onchange_theme_mode_radio"
        }),

        start: function () {
            var self = this;
            this._super.apply(this, arguments)
            $(document).on("click", "*", function (event) {
                if (!$(event.target).is($(".customizer, .customizer *"))
                    && !self._is_color_pikcer_click(event)) {
                    self.$('.customizer').removeClass('open');
                }
            });
            this._init_color_picker(this.$el);
            this._init_tab();
            this._reset_setting();
            // apply the current style
            setTimeout(function () {
                self._inner_preview();
            }, 0);
        },

        _is_color_pikcer_click: function (event) {
            if (this.$('.customizer').is(':visible')
                && $(event.target).is($(".colorpicker-bs-popover, .colorpicker-bs-popover *"))) {
                return true
            } else {
                return false
            }
        },

        _init_tab: function () {
            var self = this
            var mode_id = this.user_setting.cur_mode
            this.$(".theme-mode-radio [data-mode-id=" + mode_id + "]").attr("checked", "checked");
            this.$(".theme-mode-container[data-mode-id=" + mode_id + "]").removeClass("d-none")

            _.each(this.user_setting.theme_modes, function (theme_mode) {
                self._active_theme_style(theme_mode.id, theme_mode.cur_style);
            })
        },

        /**
         * get the user setting
         */
        willStart: function () {
            var self = this;
            var def = $.Deferred();

            core.bus.trigger('fx_get_user_setting',  {
                call_back: function(user_setting) {
                    self.user_setting = user_setting
                    def.resolve()
                }
            });

            return def;
        },

        _on_customizer_toggler_click: function (event) {
            event.preventDefault();
            event.stopPropagation();
            this.$('.customizer').addClass('open')
        },

        _on_customizer_close_click: function () {
            event.preventDefault();
            event.stopPropagation();
            this.$('.customizer').removeClass('open')
        },

        _on_preview_btn_click: function () {
            event.preventDefault();
            event.stopPropagation();
            this._inner_preview();
        },

        _inner_preview: function () {
            this._update_mode();
            this._update_style();
            this._update_menu_type();
            this._update_show_menu_txt();
        },

        _on_delete_theme_style: function (event) {
            event.stopPropagation()

            var $target = $(event.target)
            var styleId = parseInt($target.data('style-id'));
            // remove the nave item and tab pane
            this.$(".theme-style-nav-item[" + styleId + "]").remove()
            this.$(".theme-style-tab_pane[" + styleId + "]").remove()
            // chose the first
            this.$(".theme-style-nav-item nav-link").first().tab('show')
        },

        _reset_setting: function () {
            var tmp_settings = this.user_setting.settings
            var user_setting = {}
            _.each(tmp_settings, function (setting) {
                user_setting[setting.name] = setting.val
            })

            var font_type = user_setting.font_type || "sans-serif"
            this.$("input[name='font_type'][data-font-type=" + font_type + "]").attr("checked", "checked");
            var menu_type = user_setting.menu_type || "vertical"
            this.$("input[name='menu_type'][data-menu-type=" + menu_type + "]").attr("checked", "checked");
            var show_app_name = user_setting.show_app_name || false
            if (!show_app_name) {
                this.$("input[name='show_app_name']").removeAttr('checked')
            } else {
                this.$("input[name='show_app_name']").attr('checked', 'checked')
            }
        },

        _reset_cur_mode: function () {
            var mode_id = this.$("input[name='theme_mode_radio']:checked").data('mode-id');
            var style_id = this.$('.theme_style_tab.active:visible').data('style-id')
            var mode_data = _.find(this.user_setting.theme_modes, function (mode_data) {
                return mode_data.id == mode_id
            })
            var theme_styles = mode_data.theme_styles
            var theme_style = _.find(theme_styles, function (tmp_style) {
                return tmp_style.id == style_id
            })

            if (theme_style.style_items){
            var style_items = theme_style.style_items;
            var $style_item_container = this.$(
                '.style_item_container[data-style-id=' + style_id + ']')
            var $style_items = $style_item_container.find('.style_item')
            _.each($style_items, function (style_item) {
                var $tmp_style_item = $(style_item)
                var style_item_id = parseInt($tmp_style_item.data('style-item-id'))
                var $color_value = $tmp_style_item.find('.color_value')
                var tmp_style_item = _.find(style_items, function (tmp_item) {
                    return tmp_item.id == style_item_id
                })
                $color_value.val(tmp_style_item.val);
            })
        }


        },

        _update_mode: function () {
            var mode = this.$("input[name='theme_mode_radio']:checked").data('mode-name');
            switch (mode) {
                case 'dark':
                    $('body').removeClass('normal')
                    $('body').addClass('dark')
                    break;
                case 'normal':
                    $('body').removeClass('dark')
                    break;
            }
        },

        _update_show_menu_txt: function () {
            // comming soon
        },

        _update_menu_type: function () {
            var menu_type = this.$("input[name='menu_type']:checked").data('menu-type');
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

        _add_new_tab: function (theme_style) {
            this._add_new_style_nav_item(theme_style);
            this._add_new_style_tab_pane(theme_style);
            this.$(".theme_style_tab[data-style-id=" + theme_style.id + "]").tab('show')
        },

        _add_new_style_nav_item: function (theme_style) {
            var mode_id = this.$("input[name='theme_mode_radio']:checked").data('mode-id');
            var $theme_mode_container = this.$('.theme-mode-container[data-mode-id=' + mode_id + ']')
            var $add_new = $theme_mode_container.find('.add_new_style')
            var $nav_item = $(core.qweb.render('fx_theme.theme_style_tab', { theme_style: theme_style }))
            $nav_item.insertBefore($add_new)
        },

        // init color picker
        _add_new_style_tab_pane: function (theme_style) {
            var mode_id = this.$("input[name='theme_mode_radio']:checked").data('mode-id');
            var $theme_mode_container = this.$('.theme-mode-container[data-mode-id=' + mode_id + ']');
            var $tab_pane = $(core.qweb.render('fx_theme.theme_style_tab_pane', { theme_style: theme_style }));
            var $tab_container = $theme_mode_container.find('.tab-content');
            $tab_pane.appendTo($tab_container);
            this._init_color_picker($tab_pane);
        },

        _remove_new_tab: function (style_id) {
            this.$(".theme_style_tab[data-style-id=" + style_id + "]").parent().remove()
            this.$(".theme-style-tab-pane[data-style-id=" + style_id + "]").remove()
        },

        _active_theme_style: function (mode_id, style_id) {
            // show the style tab
            this.$(".theme_style_tab[data-style-id=" + style_id + "]").addClass('active')
            this.$(".theme-style-tab-pane[data-style-id=" + style_id + "]").addClass('show').addClass('active')
        },

        _get_style_txt: function () {
            var result = []
            var mode_id = this.$("input[name='theme_mode_radio']:checked").data('mode-id');
            var style_id = this.$('.theme_style_tab.active:visible').data('style-id')
            var mode_data = _.find(this.user_setting.theme_modes, function (mode_data) {
                return mode_data.id == mode_id
            })

            var theme_styles = mode_data.theme_styles
            var theme_style = _.find(theme_styles, function (tmp_style) {
                return tmp_style.id == style_id
            })

            if (theme_style && theme_style.style_items){
            var style_items = theme_style.style_items;
            var $style_item_container = this.$(
                '.style_item_container[data-style-id=' + style_id + ']')
            var $style_items = $style_item_container.find('.style_item')
            _.each($style_items, function (style_item) {
                var $tmp_style_item = $(style_item)
                var style_item_id = parseInt($tmp_style_item.data('style-item-id'))
                var $color_value = $tmp_style_item.find('input')
                var color = $color_value.val()
                var tmp_style_item = _.find(style_items, function (tmp_item) {
                    return tmp_item.id == style_item_id
                })
                var css_infos = pyUtils.py_eval(tmp_style_item.css_info || "[]")
                _.each(css_infos, function (css_info) {
                    var selector = css_info.selector
                    var key = css_info.key
                    var tmp_txt = selector + " {" + key + ":" + color + "!important;}"
                    result.push(tmp_txt)
                })
            })
        }


            // update the font type
            var font_type = this.$("input[name='font_type']:checked").data('font-type');
            var font_type_css = "*:not(.fa) {font-family: " + font_type + ", sans-serif !important;}"

            result.push(font_type_css);
            return result.join('\n')
        },

        _get_cur_style_data: function () {
            var result = []
            var style_id = this.$('.theme_style_tab.active:visible').data('style-id')
            var $style_item_container = this.$(
                '.style_item_container[data-style-id=' + style_id + ']')
            var $style_items = $style_item_container.find('.style_item')
            _.each($style_items, function (style_item) {
                var $tmp_style_item = $(style_item)
                var style_item_id = parseInt($tmp_style_item.data('style-item-id'))
                var $color_value = $tmp_style_item.find('input')
                var color = $color_value.val()
                color = _.str.trim(color)
                result.push({
                    "id": style_item_id,
                    "color": color
                })
            })
            return result;
        },

        _update_style: function () {
            var style_id = 'fx_theme_style_id';
            var $body = $('body')
            var styleText = this._get_style_txt();
            var style = document.getElementById(style_id);
            if (style.styleSheet) {
                style.setAttribute('type', 'text/css');
                style.styleSheet.cssText = styleText;
            } else {
                style.innerHTML = styleText;
            }
            style && $body[0].removeChild(style);
            $body[0].appendChild(style);
        },

        _init_color_picker: function (item) {
            var self = this;
            item.find('.style_color_item')
                .colorpicker({
                    format: 'rgba',
                    extensions: [
                        {
                            name: 'swatches',
                            options: {
                                colors: {
                                    'black': '#000000',
                                    'gray': '#888888',
                                    'white': '#ffffff',
                                    'red': 'red',
                                    'default': '#777777',
                                    'primary': '#337ab7',
                                    'success': '#5cb85c',
                                    'info': '#5bc0de',
                                    'warning': '#f0ad4e',
                                    'danger': '#d9534f'
                                },
                                namesAsValues: false
                            }
                        }
                    ]
                }).on('colorpickerChange', function (e) {
                    self._color_chagned(e)
                });
        },

        _color_chagned: function (e) {
            var style_id = $(e.currentTarget).parents('.style_item_container').first().data('style-id')
            var $color_item = $(e.currentTarget)
            var identity = $color_item.data('identity')
            if (identity) {
                var color = $color_item.find('input').val()
                var $theme_style = self.$('.theme-style-nav-item[data-style-id=' + style_id + ']');
                switch (identity) {
                    case 'border':
                        $theme_style.find('.style-preview-box').css("border-color", color);
                        $theme_style.find('.sidebar-box').css("border-right-color", color);
                        $theme_style.find('.preview-header-box').css("border-bottom-color", color);
                        $theme_style.find('.preview-footer-box').css("border-top-color", color);
                        break
                    case 'side_bar_color':
                        $theme_style.find('.sidebar-box').css("background-color", color);
                        break
                    case 'header_color':
                        $theme_style.find('.preview-header-box').css("background-color", color);
                        break
                    case 'body_color':
                        $theme_style.find('.preview-body-box').css("background-color", color);
                        break
                    case 'footer_color':
                        $theme_style.find('.preview-footer-box').css("background-color", color);
                        break
                }
            }
        },

        _get_cur_setting: function () {
            var menu_type = this.$("input[name='menu_type']:checked").data('menu-type');
            var font_type = this.$("input[name='font_type']:checked").data('font-type');
            var show_app_name = this.$("input[name='show_app_name']").val() || false;
            return {
                "menu_type": menu_type,
                "font_type": font_type,
                "show_app_name": show_app_name
            }
        },

        _reset_cur_style: function () {
            var cur_mode_id = this.user_setting.cur_mode
            var cur_mode = _.find(this.user_setting.theme_modes, function (mode) {
                return mode.id = cur_mode_id
            })
            var cur_style_id = cur_mode.cur_style
            var cur_style = _.find(cur_mode.theme_styles, function (temp_style) {
                return tmp_style.id == cur_style_id
            })
            return cur_style.style_items;
        },

        _save_settings: function () {
            var self = this
            var mode_id = this.$("input[name='theme_mode_radio']:checked").data('mode-id');
            var style_id = this.$('.theme_style_tab.active:visible').data('style-id')
            this._rpc({
                "model": "fx_theme.user_setting",
                "method": "save_setting",
                "args": [{
                    "mode_id": mode_id,
                    "style_id": style_id,
                    "setting_data": this._get_cur_setting(),
                    "style_items": this._get_cur_style_data()
                }]
            }).then(function (updated_style) {
                // add the new style header and tab
                var theme_style = self._get_setting_style_data(mode_id, style_id)
                // update the style item
                Object.assign(theme_style, updated_style)
            })
        },

        _refresh_style_preview: function (theme_style) {
            var $theme_style = this.$('.theme-style-nav-item[data-style-id=' + theme_style.id + ']');
            var $nav_item = $(core.qweb.render('fx_theme.theme_style_tab', { theme_style: theme_style }))
            $nav_item.replaceWith($theme_style)
        },

        _on_add_new_style: function (event) {
            event.preventDefault();
            var self = this;
            var mode_id = this.$("input[name='theme_mode_radio']:checked").data('mode-id');
            this._rpc({
                "model": "fx_theme.theme_mode",
                "method": "add_new_style",
                "args": [mode_id]
            }).then(function (new_style) {
                var mode = _.find(self.user_setting.theme_modes, function (tmp_mode) {
                    return tmp_mode.id == mode_id;
                })
                mode.theme_styles.push(new_style);
                self._add_new_tab(new_style);
            })
        },

        _on_delete_style: function (event) {
            event.preventDefault();
            var self = this;
            var style_id = this.$('.theme_style_tab.active:visible').data('style-id');
            this._rpc({
                "model": "fx_theme.theme_style",
                "method": "delete_style",
                "args": [style_id]
            }).then(function () {
                self._remove_new_tab(style_id);
            })
        },

        _get_setting_style_data: function (mode_id, style_id) {
            var mode = _.find(this.user_setting.theme_modes, function (tmp_mode) {
                return tmp_mode.id == mode_id
            })
            var theme_styles = mode.theme_styles
            var theme_style = _.find(theme_styles, function (tmp_style) {
                return tmp_style.id == style_id;
            })
            return theme_style
        },

        _on_cancel_btn_click: function (event) {
            event.preventDefault();
            event.stopPropagation();
            this.$('.customizer').removeClass('open')
        },

        _on_reset_btn_click: function (event) {
            event.stopPropagation();
        },

        _on_save_btn_click: function (event) {
            event.preventDefault();
            // save the style data
            this._save_settings();
        },

        _get_mode_data: function (mode_id) {
            return _.find(this.user_setting.theme_modes, function (mode) {
                return mode.id == mode_id
            })
        },

        _onchange_theme_mode_radio: function (event) {
            event.stopPropagation();
            var mode_id = $(event.target).data('mode-id')
            this.$(".theme-mode-container").addClass("d-none")
            this.$(".theme-mode-container[data-mode-id=" + mode_id + "]").removeClass("d-none")
        }
    });

    // add to the style setting
    StyleSetting.items = []
    SystrayMenu.Items.push(StyleSetting);

    return StyleSetting;
});
