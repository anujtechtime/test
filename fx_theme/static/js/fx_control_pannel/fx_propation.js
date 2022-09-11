odoo.define('fx_theme.custom_proposition', function (require) {
    "use strict";

    var core = require('web.core');
    var field_utils = require('web.field_utils');
    var Widget = require('web.Widget');
    var searchExtend = require('funenc.search_extend');
    var session = require('web.session');

    var _t = core._t;
    var _lt = core._lt;

    var Field = Widget.extend({
        init: function (parent, field, option) {
            this._super(parent);

            this.field = field;
            this.option = option;
            if (option) {
                this.name = option.name || undefined
            } else {
                this.name = undefined
            }
            this.placeholder = _t((option && option.placeholder) || '请输入' + field.string)
            this.attributes.placeholder = this.placeholder 
        },

        start: function () {
            this.set_default()
        },

        set_default: function () {
            if (this.getParent().search_view) {
                var search_default = this.getParent().search_view._search_defaults;
                this.default_value = search_default[this.name] || undefined
                this.$el.val(this.default_value)
            }
        },

        get_label: function (field, operator) {
            var format;
            switch (operator.value) {
                case '∃':
                case '∄':
                    format = _t('%(field)s %(operator)s');
                    break;
                default:
                    format = _t('%(field)s %(operator)s "%(value)s"');
                    break;
            }
            return this.format_label(format, field, operator);
        },

        format_label: function (format, field, operator) {
            return _.str.sprintf(format, {
                field: field.string,
                // According to spec, HTMLOptionElement#label should return
                // HTMLOptionElement#text when not defined/empty, but it does
                // not in older Webkit (between Safari 5.1.5 and Chrome 17) and
                // Gecko (pre Firefox 7) browsers, so we need a manual fallback
                // for those
                operator: operator.label || operator.text,
                value: this
            });
        },

        get_domain: function (field, operator) {
            switch (operator.value) {
                case '∃':
                    return [[field.name, '!=', false]];
                case '∄':
                    return [[field.name, '=', false]];
                default:
                    return [[field.name, operator.value, this.get_value()]];
            }
        },

        show_inputs: function ($operator) {
            var $value = this.$el.parent();
            switch ($operator.val()) {
                case '∃':
                case '∄':
                    $value.hide();
                    break;
                default:
                    $value.show();
            }
        },
        /**
         * Returns a human-readable version of the value, in case the "logical"
         * and the "semantic" values of a field differ (as for selection fields,
         * for instance).
         *
         * The default implementation simply returns the value itself.
         *
         * @return {String} human-readable version of the value
         */
        toString: function () {
            return this.get_value();
        },

        /**
         * 一些自定义控件由于比较特殊，需要自己清理
         */
        reset: function () {
            this.$('input').val("")
            this.$('select[class="o_input"]').find('option').removeAttr("selected")
            this.$('select[class="o_input"]').find('option').first().attr("selected", "selected")
        },
    });

    var Char = Field.extend({
        tagName: 'input',
        className: 'o_input',
        attributes: {
            type: 'text'
        },
        operators: [
            {value: "like", text: _lt("contains")},
            {value: "not ilike", text: _lt("doesn't contain")},
            {value: "=", text: _lt("is equal to")},
            {value: "!=", text: _lt("is not equal to")},
            {value: "∃", text: _lt("is set")},
            {value: "∄", text: _lt("is not set")}
        ],
        get_value: function () {
            return this.$el.val();
        },

        reset: function () {
            this.$el.val("")
            this.$('input').val("")
            this.$('select[class="o_input"]').find('option').removeAttr("selected")
            this.$('select[class="o_input"]').find('option').first().attr("selected", "selected")
        },
    });

    // 时间字段
    var DateTime = Widget.extend({
        template: 'lay_datetime',

        operators: [
            {value: "between", text: _lt("is between")},
            {value: "ilike", text: _lt("contains")},
            {value: "not ilike", text: _lt("doesn't contain")},
            {value: "=", text: _lt("is equal to")},
            {value: "!=", text: _lt("is not equal to")},
            {value: "∃", text: _lt("is set")},
            {value: "∄", text: _lt("is not set")}
        ],

        init: function (parent, field, option) {
            this._super(parent, field, option);
            this.field = field;
            option.range = option.range !== undefined ? option.range : true;
            this.option = option;
            this.setPlaceholder(field, option);
            this.id = 'lay_datetime_' + parent.getParent().controller_id + field.name;
        },

        start: function () {
            this.set_default()
        },

        set_default: function () {
            if (this.getParent().search_view && this.name) {
                var search_default = this.getParent().search_view._search_defaults;
                this.default_value = search_default[this.name] || undefined;
                this.$el.val(this.default_value)
            }
        },

        on_attach_callback: function () {
            var self = this;
            layui.use('laydate', function () {
                var laydate = layui.laydate;
                laydate.render({
                    elem: '#' + self.id, //指定元素
                    lang: session.user_context.lang === "en_US" ? 'en' : 'cn',
                    type: 'datetime',
                    range: self.option.range === true ? '~' : false,
                });
            });
        },

        setPlaceholder: function (field, option) {
            this.placeholder = _t(option.placeholder || '请选择' + field.string)
        },

        get_value: function () {
            return this.$el.val()
        },

        get_domain: function (field, operator) {
            var self = this;
            var value = self.get_value();
            if (!value || value === '') {
                return
            }
            switch (operator.value) {
                case 'between':
                    return [[field.name, '>=', value.split(' ~ ')[0]], [field.name, '<=', value.split(' ~ ')[1]]];
                default:
                    return [[field.name, operator.value, value]];
            }
        },

        reset: function () {
            this.$el.val('')
        }
    });

    var Date = DateTime.extend({
        on_attach_callback: function () {
            var self = this;
            layui.use('laydate', function () {
                var laydate = layui.laydate;
                laydate.render({
                    elem: '#' + self.id, //指定元素
                    lang: session.user_context.lang === "en_US" ? 'en' : 'cn',
                    type: 'date',
                    range: self.option.range === true ? '~' : false,
                });
            });
        }
    });

    var Integer = Field.extend({
        tagName: 'input',
        className: 'o_input',
        attributes: {
            type: 'number',
            value: '0',
        },
        operators: [
            {value: "=", text: _lt("is equal to")},
            {value: "!=", text: _lt("is not equal to")},
            {value: ">", text: _lt("greater than")},
            {value: "<", text: _lt("less than")},
            {value: ">=", text: _lt("greater than or equal to")},
            {value: "<=", text: _lt("less than or equal to")},
            {value: "∃", text: _lt("is set")},
            {value: "∄", text: _lt("is not set")}
        ],
        toString: function () {
            return this.$el.val();
        },
        get_value: function () {
            try {
                var val = this.$el.val();
                return field_utils.parse.integer(val === "" ? 0 : val);
            } catch (e) {
                return "";
            }
        }
    });

    var Id = Integer.extend({
        operators: [{value: "=", text: _lt("is")}]
    });

    var Float = Field.extend({
        template: 'SearchView.extended_search.proposition.float',
        operators: [
            {value: "=", text: _lt("is equal to")},
            {value: "!=", text: _lt("is not equal to")},
            {value: ">", text: _lt("greater than")},
            {value: "<", text: _lt("less than")},
            {value: ">=", text: _lt("greater than or equal to")},
            {value: "<=", text: _lt("less than or equal to")},
            {value: "∃", text: _lt("is set")},
            {value: "∄", text: _lt("is not set")}
        ],
        init: function (parent, field, option) {
            this._super(parent, field, option);
            this.decimal_point = _t.database.parameters.decimal_point;
        },
        toString: function () {
            return this.$el.val();
        },
        get_value: function () {
            try {
                var val = this.$el.val();
                return field_utils.parse.float(val === "" ? 0.0 : val);
            } catch (e) {
                return "";
            }
        }
    });

    var Selection = Field.extend({
        template: 'SearchView.extended_search.proposition.selection_funenc',

        init: function(parent, field, option){
            this._super(parent, field, option);
            this.filter_id = 'custom_search_' + parent.getParent().controller_id
        },

        operators: [
            {value: "=", text: _lt("is")},
            {value: "!=", text: _lt("is not")},
            {value: "∃", text: _lt("is set")},
            {value: "∄", text: _lt("is not set")}
        ],
        toString: function () {
            var select = this.$el[0];
            var option = select.options[select.selectedIndex];
            return option.label || option.text;
        },

        on_attach_callback: function () {
            var self = this;
            layui.use('form', function () {
                var form = layui.form;
                form.render('select', self.filter_id)
            });
        },

        get_value: function () {
            return this.$el.val();
        },

        get_domain: function (field, operator) {
            if (this.get_value()) {
                return [[field.name, operator.value, this.get_value()]];
            }
        },

        reset: function () {
            this.value = '';
            var self = this;
            this.$el.val('')
            layui.use('form', function () {
                var form = layui.form;
                var field_name_obj = {};
                field_name_obj[self.field.name] = '';
                form.val(self.filter_id, field_name_obj);
            });
        }
    });

    var Many2one = Widget.extend({
        template: 'lay_m2o',

        operators: [
            {value: "=", text: _lt("is equal to")},
            {value: "between", text: _lt("is between")},
            {value: "ilike", text: _lt("contains")},
            {value: "not ilike", text: _lt("doesn't contain")},
            {value: "!=", text: _lt("is not equal to")},
            {value: "∃", text: _lt("is set")},
            {value: "∄", text: _lt("is not set")}
        ],

        init: function (parent, field, option) {
            this._super(parent, field, option);
            this.field = field;
            option.range = option.range !== undefined ? option.range : true;
            this.option = option;
            this.setPlaceholder(field, option);
            this.filter_id = 'custom_search_' + parent.getParent().controller_id
        },

        start: function () {
            this.set_default()
        },

        set_default: function () {
            if (this.getParent().search_view) {
                var search_default = this.getParent().search_view._search_defaults;
                this.default_value = search_default[this.name] || undefined;
                this.$el.val(this.default_value)
            }
        },

        setPlaceholder: function (field, option) {
            this.placeholder = _t(option.placeholder || '请选择' + field.string)
        },

        on_attach_callback: function () {
            var self = this;
            self._rpc({
                model: self.field.relation,
                method: 'name_search',
                kwargs: {
                    limit: null
                }
            }).then(function (results) {
                // 异步添加数据后刷新form
                self.$el.children('option:gt(0)').remove();
                results.forEach(function (item) {
                    self.$el.append('<option value="' + item[0] + '">' + item[1] + '</option>')
                });
                layui.use('form', function () {
                    var form = layui.form;
                    form.render('select', self.filter_id)
                });
            });
        },

        get_domain: function (field, operator) {
            var self = this;
            var value = self.get_value();
            if (!value || value === '') {
                return
            }
            return [[field.name, operator.value, value]];
        },

        get_value: function () {
            var select = this.$el[0];
            var option = select.options[select.selectedIndex];
            return option.value !== '' ? parseInt(option.value) : '';
        },

        reset: function () {
            this.value = '';
            var self = this;
            this.$el.val('');
            layui.use('form', function () {
                var form = layui.form;
                var field_name_obj = {};
                field_name_obj[self.field.name] = '';
                form.val(self.filter_id, field_name_obj)
            });
        }
    });

    var Boolean = Field.extend({
        tagName: 'span',
        operators: [
            {value: "=", text: _lt("is true")},
            {value: "!=", text: _lt("is false")}
        ],

        get_label: function (field, operator) {
            return this.format_label(
                _t('%(field)s %(operator)s'), field, operator);
        },

        get_value: function () {
            return true;
        }
    });

    searchExtend.funenc_search_registry
        .add('char', Char)
        .add('text', Char)
        .add('one2many', Char)
        .add('many2one', Many2one)
        .add('many2many', Char)
        .add('datetime', DateTime)
        .add('date', Date)
        .add('integer', Integer)
        .add('float', Float)
        .add('monetary', Float)
        .add('boolean', Boolean)
        .add('selection', Selection)
        .add('id', Id);

    return {
        Field: Field
    };
});
