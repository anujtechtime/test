odoo.define('fx_theme.page_header', function (require) {
    "use strict";

    var core = require('web.core');
    var Widget = require('web.Widget');

    var fxThemePageHeader = Widget.extend({
        template: 'fx_theme.page_header',

        events: _.extend({}, Widget.prototype.events, {
            'click .hz-navigation-toggler': "_on_toggler_click"
        }), 

        start: function () {
            this._super.apply(this, arguments)
            // update the bread crumb
            core.bus.on('update_bread_crumbs', this, this.update_bread_crumbs);
        },

        update_bread_crumbs: function (data) {
            var self = this;
            var bcDescriptors = data
            var breadcrumbs = bcDescriptors.map(function (bc, index) {
                return self._renderBreadcrumbsItem(
                    bc, index, bcDescriptors.length, data.noDisplayContent);
            });
            this.$('.breadcrumb_box').html(breadcrumbs);
            var title = _.last(bcDescriptors)
            this.update_title(title.title || '')
        },

        _renderBreadcrumbsItem: function (bc, index, length, noDisplayContent) {
            var is_last = (index === length - 1);
            var li_content = bc.title && _.escape(bc.title.trim()) || noDisplayContent;
            var $bc = $(core.qweb.render('fx_theme.breadcrumb_item',
                { content: li_content, is_last: is_last }))
            $bc.click(function (ev) {
                ev.preventDefault();
                // the home page icon
                if (!bc.controllerID) {
                    return
                }
                core.bus.trigger('fx_theme.breadcrumb_clicked', bc.controllerID);
            });

            var secondLast = index === length - 2;
            if (secondLast) {
                $bc.attr('accessKey', 'b');
            }

            return $bc;
        },

        update_title: function (title) {
            this.$('.title').text(title)
        },

        _on_toggler_click: function(event) {
            event.preventDefault();
            event.stopPropagation();

            var self = this;
            var $window = $(window);
            var $body = $('body');

            // create overlay when the size is below 1200
            if ($window.width() < 1200) {
                self.createOverlay();
                $body.addClass("navigation-show");
            } else {
                if (!$body.hasClass("hz-navigation-toggle-one") 
                && !$body.hasClass("hz-navigation-toggle-none")) {
                    $body.removeClass("hz-navigation-toggle-one");
                    $body.addClass("hz-navigation-toggle-none");
                } else if ($body.hasClass("hz-navigation-toggle-one")) {
                    $body.removeClass("hz-navigation-toggle-one");
                    $body.addClass("hz-navigation-toggle-none");
                } else {
                    $body.removeClass("hz-navigation-toggle-none");
                    $body.addClass("hz-navigation-toggle-one");
                }
            }
        }
    });

    return fxThemePageHeader;
});
