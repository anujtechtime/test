odoo.define('fx.pager', function (require) {
    "use strict";

    var Widget = require('web.Widget');
    var core = require('web.core');

    var fxPager = Widget.extend({

        events: _.extend({}, Widget.prototype.events, {
            "click .fx_pager_pager": "_onPagerClick",
            "click .fx_pager_prev": "_onPrevclick",
            "click .fx_pager_next": "_onNextClick",
            "click .fx_pager_page": "_onPagerClick"
        }),

        init: function (parent, options) {

            this.total_number = options.total_number || 0
            this.page_size = options.page_size || 20
            this.limit = options.limit

            this.current_page = options.current_page || 1
            this.page_range = options.page_range || 10
            this.range_start = this.current_page - this.page_range
            this.range_end = this.current_page + this.page_range
            this.ellipsis_text = this.ellipsis_text || '...'
            this.hide_less_than_one_page = this.hide_when_less_than_one_page || false

            if (this.range_end > this.total_page) {
                this.range_end = this.total_page;
                this.range_start = this.total_page - this.page_range * 2;
                this.range_start = this.range_start < 1 ? 1 : this.range_start;
            }

            if (this.range_start <= 1) {
                this.range_start = 1
                this.range_end = Math.min(this.page_range * 2 + 1, this.total_page);
            }

            this.show_prev = options.show_prev || true
            this.show_next = options.show_next || true
            this.show_page_numbers = options.show_page_numbers || true

            this.show_navigator = options.show_navigator || true
            this.show_go_input = options.show_go_input || true
            this.show_go_button = options.show_go_button || true
            this.prev_text = options.prev_text || 'prev'
            this.next_text = options.next_text || 'next'
            this.ellipsis_text = options.ellipsis_text || '...'
            this.go_button_text = options.go_button_text || 'go'
            this.active_class_name = options.active_class_name || 'fx_pager_active'
            this.disable_class_name = options.disable_class_name || 'fx_pager_disabled'
            this.auto_hide_previouse = options.auto_hide_previouse || false
            this.page_link = '#'

            return this._super.apply(this, arguments);
        },

        // get the page num
        getTotalPage: function () {
            return Math.ceil(this.getTotalNumber() / this.page_size);
        },

        // Get total number
        getTotalNumber: function () {
            return this.total_number || 0;
        },

        // jump to the spec page
        _onPagerClick: function (event) {
            var current = $(event.currentTarget);
            var pageNumber = $.trim(current.attr('data-num'));
            if (!pageNumber) {
                return;
            }
            this.goToPage(pageNumber);
        },

        // jump to the next page
        _onNextClick: function (event) {
            var current = $(event.currentTarget);
            var pageNumber = $.trim(current.attr('data-num'));
            if (!pageNumber) return;
            this.goToPage(pageNumber);
        },

        _onPrevclick: function (event) {
            var current = $(event.currentTarget);
            var pageNumber = $.trim(current.attr('data-num'));
            if (!pageNumber) return;
            this.goToPage(pageNumber);
        },

        _normalize: function () {

            this.total_page = this.getTotalPage();
            this.range_start = this.current_page - this.page_range;
            this.range_end = this.current_page + this.page_range;

            if (this.range_end > this.total_page) {
                this.range_end = this.total_page;
                this.range_start = this.total_page - this.page_range * 2;
                this.range_start = this.range_start < 1 ? 1 : this.range_start;
            }

            if (this.range_start <= 1) {
                this.range_start = 1;
                this.range_end = Math.min(this.page_range * 2 + 1, this.total_page);
            }
        },

        render: function () {
            this._normalize()

            this.$el.empty()
            $(this.generateHTML()).appendTo(this.$el)
            this.renderSelection()

            if (this.hide_less_than_one_page) {
                if (this.total_page <= 1) {
                    this.hide()
                } else {
                    this.show()
                }
            }
        },

        renderSelection: function () {
            var $sel = $(core.qweb.render('fx_pager_limit'));
            $sel.appendTo(this.$el.find('.fx_pager'))
            $sel.find('select').select2({
                minimumResultsForSearch: 'Infinity'
            });
        },

        updateState: function (state, options) {
            this.state = _.extend(this.state, state);

            this.total_number = state.size;
            this.page_size = state.limit;
            this.current_page = state.current_min;
            this.render();

            // if (options && options.notifyChange) {
            //     this.trigger('pager_changed', _.clone(this.state));
            // }
        },

        // Generate HTML content from the template
        generateHTML: function () {

            var current_page = this.current_page;
            var total_page = this.getTotalPage();

            var html = '';
            var go_input = '<input type="text" class="go_number form-control">';
            var go_button = '<input type="button" class="go_button btn" value="' + this.go_button_text + '">';

            var auto_hide_prev = this.autoHidePrev;
            var auto_hide_next = this.autoHideNext;

            if (this.show_prev || this.show_page_numbers || this.show_next) {
                html += '<div class="fx_pager">';
                html += '<ul class="fx_pager_list">';

                // Whether to display the Previous button
                if (this.show_prev) {
                    if (current_page <= 1) {
                        // if page less than 1 then hede the prev button
                        if (!auto_hide_prev) {
                            html += '<li class="fx_pager_prev fx_pager_disabled"><a><i class="fa fa-angle-left"></i></a><\/li>';
                        }
                    } else {
                        html += '<li class="fx_pager_prev" data-num="' + (this.current_page - 1) + '" title="previous page"><a href="' + this.page_link + '"><i class="fa fa-angle-left"></i></a><\/li>';
                    }
                }

                // Whether to display the pages
                if (this.show_page_numbers) {
                    html += this.renderPageNumbers();
                }

                // Whether to display the Next button
                if (this.show_next) {
                    if (this.current_page >= this.total_page) {
                        if (!auto_hide_next) {
                            html += '<li class="fx-pager-next fx_pager_disabled"><a><i class="fa fa-angle-right"></i></a></li>';
                        }
                    } else {
                        html += '<li class="fx-pager-next" data-num="' + (this.current_page + 1) + '" title="Next page"><a href="' + this.page_link + '"><i class="fa fa-angle-right"></i></a><\/li>';
                    }
                }
                html += '<\/ul>';
            }

            // Whether to display the navigator
            if (this.show_navigator) {
                html += '<div class="fx_pager_nav">total: ' + total_page + '<\/div>';
            }

            // Whether to display the Go input
            if (this.show_go_input) {
                html += '<div class="go_input">' + go_input + '</div>';
            }

            // Whether to display the Go button
            if (this.show_go_button) {
                html += '<div class="go_button">' + go_button + '</div>';
            }

            return html;
        },

        // Go to the specified page
        goToPage: function (pageNumber) {
            if (this.disabled) return;

            var pageNumber = pageNumber;
            pageNumber = parseInt(pageNumber);

            var totalPage = this.getTotalPage();
            if (!pageNumber || pageNumber < 1 || pageNumber > totalPage) return;

            this.current_page = pageNumber
            this.generateHTML()

            this.trigger('pager_changed', {
                size: this.totalNumber,
                current_min: pageNumber * (this.currentPage - 1),
                limit: this.limit,
            });
        },

        disable: function() {

        },

        enable: function() {

        },

        // gen the page numbers
        renderPageNumbers: function () {
            var html = '';

            // disable page range, display all the pages
            if (this.page_range === null) {
                for (var i = 1; i <= this.total_page; i++) {
                    if (i == this.current_page) {
                        html += '<li class="fx_pager_page fx_pager_pages active data-num="' + i + '"><a>' + i + '<\/a><\/li>';
                    } else {
                        html += '<li class="fx_pager_page data-num="' + i + '"><a href="#">' + i + '<\/a><\/li>';
                    }
                }
                return html;
            }

            if (this.range_start <= 3) {
                for (var i = 1; i < this.range_start; i++) {
                    if (i == this.current_page) {
                        html += '<li class="fx_pager_pager active" data-num="' + i + '"><a>' + i + '<\/a><\/li>';
                    } else {
                        html += '<li class="fx_pager_page data-num="' + i + '"><a href="' + this.page_link + '">' + i + '<\/a><\/li>';
                    }
                }
            } else {
                // show first page
                if (this.show_first_on_ellipsis_show) {
                    html += '<li class="fx_pager_page fx_pager_first data-num="1"><a href="' + this.page_link + '">1<\/a><\/li>';
                }
                html += '<li class="fx_pager_ellipsis fx_pager_disabled"><a>' + this.ellipsis_text + '<\/a><\/li>';
            }

            for (var i = this.range_start; i <= this.range_end; i++) {
                if (i == this.current_page) {
                    html += '<li class="fx_pager_page active data-num="' + i + '"><a>' + i + '<\/a><\/li>';
                } else {
                    html += '<li class="fx_pager_page" data-num="' + i + '"><a href="' + this.page_link + '">' + i + '<\/a><\/li>';
                }
            }

            if (this.range_end >= this.total_page - 2) {
                for (var i = this.range_end + 1; i <= this.total_page; i++) {
                    html += '<li class="fx_pager_page data-num="' + i + '"><a href="' + this.page_link + '">' + i + '<\/a><\/li>';
                }
            } else {
                html += '<li class="fx_pager_ellipsis fx_pager_disabled"><a>' + this.ellipsis_text + '<\/a><\/li>';
                if (this.show_last_on_ellipsis_show) {
                    html += '<li class="fx_pager_page fx_pager_page_last" data-num="' + this.total_page + '"><a href="' + this.page_link + '">' + this.total_page + '<\/a><\/li>';
                }
            }
            return html;
        }
    });

    return fxPager;
});
