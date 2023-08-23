odoo.define('web.AutoComplete', function (require) {
"use strict";

var Widget = require('web.Widget');

return Widget.extend({
    template: "SearchView.autocomplete",

    // Parameters for autocomplete constructor:
    //
    // parent: this is used to detect keyboard events
    //
    // options.source: function ({term:query}, callback).  This function will be called to
    //      obtain the search results corresponding to the query string.  It is assumed that
    //      options.source will call callback with the results.
    // options.select: function (ev, {item: {facet:facet}}).  Autocomplete widget will call
    //      that function when a selection is made by the user
    // options.get_search_string: function ().  This function will be called by autocomplete
    //      to obtain the current search string.
    init: function (parent, options) {
        this._super(parent);
        this.$input = options.$input;
        this.source = options.source;
        this.select = options.select;
        this.get_search_string = options.get_search_string;


        this.current_result = null;

        this.searching = true;
        this.search_string = '';
        this.current_search = null;
        this._isInputComposing = false;
    },
    start: function () {
        var self = this;
        this.$input.on('compositionend', function (ev) {
            self._isInputComposing = false;
        });
        this.$input.on('compositionstart', function (ev) {
            self._isInputComposing = true;
        });
        this.$input.on('keyup', function (ev) {
            if (ev.which === $.ui.keyCode.RIGHT && !self._isInputComposing) {
                self.searching = true;
                ev.preventDefault();
                return;
            }
            if (ev.which === $.ui.keyCode.ENTER && !self._isInputComposing) {
                if (self.search_string.length) {
                    self.select_item(ev);
                }
                return;
            }
            self._updateSearch();
        });
        this.$input.on('input', function (ev) {
            if (ev.originalEvent &&
                ev.originalEvent.inputType === 'insertCompositionText' ||
                ev.originalEvent.inputType === 'insertFromPaste') {
                // click inside keyboard IME suggestions menu
                self._updateSearch();
            }
        });
        this.$input.on('keypress', function (ev) {
            if (ev.which > 31 && ev.which !== 127) {
                // we filter control character out of the search string
                self.search_string = self.search_string + String.fromCharCode(ev.which);
            }
            if (self.search_string.length) {
                self.searching = true;
                var search_string = self.search_string;
                self.initiate_search(search_string);
            } else {
                self.close();
            }
        });
        this.$input.on('keydown', function (ev) {
            if (self._isInputComposing) {
                return;
            }
            switch (ev.which) {
                case $.ui.keyCode.ENTER:

                // TAB and direction keys are handled at KeyDown because KeyUp
                // is not guaranteed to fire.
                // See e.g. https://github.com/aef-/jquery.masterblaster/issues/13
                case $.ui.keyCode.TAB:
                    if (self.search_string.length) {
                        self.select_item(ev);
                    }
                    break;
                case $.ui.keyCode.DOWN:
                    self.move('down');
                    self.searching = false;
                    ev.preventDefault();
                    break;
                case $.ui.keyCode.UP:
                    self.move('up');
                    self.searching = false;
                    ev.preventDefault();
                    break;
                case $.ui.keyCode.RIGHT:
                    if(self.$input[0].selectionStart < self.search_string.length) {
                        ev.stopPropagation();
                        return;
                    }
                    self.searching = false;
                    var current = self.current_result;
                    if (current && current.expand && !current.expanded) {
                        self.expand();
                        self.searching = true;
                        ev.stopPropagation();
                    }
                    ev.preventDefault();
                    break;
                case $.ui.keyCode.LEFT:
                     if(self.$input[0].selectionStart > 0) {
                        ev.stopPropagation();
                     }
                     break;
                case $.ui.keyCode.ESCAPE:
                    self.close();
                    self.searching = false;
                    break;
            }
        });
    },
    initiate_search: function (query) {
        if (query === this.search_string && query !== this.current_search) {
            this.search(query);
        }
    },
    search: function (query) {
        var self = this;
        this.current_search = query;
        this.source({term:query}, function (results) {
            if (results.length) {
                self.render_search_results(results);

               var ddgst = $('.data_filter_data');
                // console.log("ddgst[0]@@@@@@@@@@@@@@@@@@@",ddgst)

                if (ddgst.length > 0){

                var ddgst = document.getElementsByClassName('data_filter_data');
        // console.log("o_filters_menu_button@@@@@@@@@@@@@@@@@@@@@",ddgst[0].childNodes[3])

        var ddgst_student = document.getElementsByClassName('data_filter_data_student_type');
        var ddgst_department = document.getElementsByClassName('data_filter_data_department');
        var ddgst_year = document.getElementsByClassName('data_filter_data_year');
        var ddgst_status = document.getElementsByClassName('data_filter_data_status');
        var ddgst_shift = document.getElementsByClassName('data_filter_data_shift');
        var ddgst_level = document.getElementsByClassName('data_filter_data_level');
        var ddgst_year_acceptance = document.getElementsByClassName('data_filter_data_year_acceptance');

        var ddgst_new_data = document.getElementsByClassName('data_filter_data_new_data');


        console.log("ddgst_year@@@@@@@@@@@@@@@@@",ddgst_year)
        
        
        
        var i = 1;
        var j = 1;
        var k = 1;
        var l = 1;
        var m = 1;
        var n = 1;
        var o = 1;
        var p = 1;
        var q = 1;

        if (ddgst[0] ||  ddgst_student[0] ||  ddgst_department[0] ||  ddgst_year[0]){

        for (i = 1; i < ddgst[0].childNodes.length; i++) {
        
            if (ddgst[0].childNodes[i].childNodes[1].value == 'true') {
                // nval = 'college';
                self.focus_element(self.$('li:nth-child(3)'));
                ddgst[0].childNodes[i].childNodes[1].value = '';
            }

            i = i + 1
        }

        for (p = 1; p < ddgst_year_acceptance[0].childNodes.length; p++) {
        
            if (ddgst_year_acceptance[0].childNodes[p].childNodes[1].value == 'true') {
                // nval = 'year_of_acceptance_1';
                self.focus_element(self.$('li:nth-child(4)'));
                ddgst_year_acceptance[0].childNodes[p].childNodes[1].value = '';
            }
            p = p + 1
        }

        for (q = 1; q < ddgst_new_data[0].childNodes.length; q++) {
        
            if (ddgst_new_data[0].childNodes[q].childNodes[1].value == 'true') {
                // nval = 'data_one';
                self.focus_element(self.$('li:nth-child(5)'));
                ddgst_new_data[0].childNodes[q].childNodes[1].value = '';
            }
            q = q + 1
        }

        for (m = 1; m < ddgst_status[0].childNodes.length; m++) {
        
            if (ddgst_status[0].childNodes[m].childNodes[1].value == 'true') {
                // nval = 'Status';
                self.focus_element(self.$('li:nth-child(7)'));
                ddgst_status[0].childNodes[m].childNodes[1].value = '';
            }

            m = m + 1
        }

        for (n = 1; n < ddgst_shift[0].childNodes.length; n++) {
        
            if (ddgst_shift[0].childNodes[n].childNodes[1].value == 'true') {
                // nval = 'shift';
                self.focus_element(self.$('li:nth-child(7)'));
                ddgst_shift[0].childNodes[n].childNodes[1].value = '';
            }

            n = n + 1
        }

        for (o = 1; o < ddgst_level[0].childNodes.length; o++) {
        
            if (ddgst_level[0].childNodes[o].childNodes[1].value == 'true') {
                // nval = 'level';
                self.focus_element(self.$('li:nth-child(7)'));
                ddgst_level[0].childNodes[o].childNodes[1].value = '';
            }

            o = o + 1
        }




        for (j = 1; j < ddgst_student[0].childNodes.length; j++) {
        
            if (ddgst_student[0].childNodes[j].childNodes[1].value == 'true') {
                // nval = 'student_type';
                self.focus_element(self.$('li:nth-child(6)'));
                ddgst_student[0].childNodes[j].childNodes[1].value = '';
            }
            j = j + 1
        }

        for (k = 1; k < ddgst_department[0].childNodes.length; k++) {
        
            if (ddgst_department[0].childNodes[k].childNodes[1].value == 'true') {
                // nval = 'department';
                self.focus_element(self.$('li:nth-child(7)'));
                ddgst_department[0].childNodes[k].childNodes[1].value = '';
            }
            k = k + 1
        }

        for (l = 1; l < ddgst_year[0].childNodes.length; l++) {
        
            if (ddgst_year[0].childNodes[l].childNodes[1].value == 'true') {
                // nval = 'year';
                self.focus_element(self.$('li:nth-child(2)'));
                ddgst_year[0].childNodes[l].childNodes[1].value = '';
            }
            l = l + 1
        }

        }
        }
        else{
            self.focus_element(self.$('li:first-child'))
        }


                
                // console.log("self.focus_element(self.$('li:first-child'))@@@@@@@@@@@@@@@@@",self.$('li:nth-child(2)'))
            } else {
                self.close();
            }
        });
    },
    render_search_results: function (results) {
        var self = this;
        var $list = this.$el;
        $list.empty();
        results.forEach(function (result) {
            var $item = self.make_list_item(result).appendTo($list);
            result.$el = $item;
        });
        // IE9 doesn't support addEventListener with option { once: true }
        this.el.onmousemove = function (ev) {
            self.$('li').each(function (index, li) {
                li.onmouseenter = self.focus_element.bind(self, $(li));
            });
            var targetFocus = ev.target.tagName === 'LI' ?
                ev.target :
                ev.target.closest('li');
            self.focus_element($(targetFocus));
            self.el.onmousemove = null;
        };
        this.show();
    },
    make_list_item: function (result) {
        var self = this;
        var $li = $('<li>')
            .mousedown(function (ev) {
                if (ev.button === 0) { // left button
                    self.select(ev, {item: {facet: result.facet}});
                    self.close();
                }
            })
            .data('result', result);
        if (result.expand) {
            var $expand = $('<a class="o-expand" href="#">').appendTo($li);
            $expand.mousedown(function (ev) {
                ev.stopPropagation();
                ev.preventDefault(); // to prevent dropdown from closing
                if (result.expanded) {
                    self.fold();
                } else {
                    self.expand();
                }
            });
            $expand.click(function(ev) {
                ev.preventDefault(); // to prevent url from changing due to href="#"
            });
            result.expanded = false;
        }
        if (result.indent) $li.addClass('o-indent');
        $li.append($('<a href="#">').html(result.label));
        return $li;
    },
    expand: function () {
        var self = this;
        var current_result = this.current_result;
        current_result.expand(this.get_search_string()).then(function (results) {
            (results || [{label: '(no result)'}]).reverse().forEach(function (result) {
                result.indent = true;
                var $li = self.make_list_item(result);
                current_result.$el.after($li);
            });
            self.current_result.expanded = true;
            self.current_result.$el.find('a.o-expand').removeClass('o-expand').addClass('o-expanded');
        });
    },
    fold: function () {
        var $next = this.current_result.$el.next();
        while ($next.hasClass('o-indent')) {
            $next.remove();
            $next = this.current_result.$el.next();
        }
        this.current_result.expanded = false;
        this.current_result.$el.find('a.o-expanded').removeClass('o-expanded').addClass('o-expand');
    },
    focus_element: function ($li) {
        this.$('li').removeClass('o-selection-focus');
        console.log("$wwwwwwwwwwwwwwwwwwwwwwwww",$(".o_filters_menu_button_year"));
        $li.addClass('o-selection-focus');
        console.log("$li###################",$li)
        this.current_result = $li.data('result');
    },
    select_item: function (ev) {
        console.log("this.current_result#################",this.current_result)
        if (this.current_result == null){

        }
        else {
        this.select(ev, {item: {facet: this.current_result.facet}});
    }
        this.close();
    },
    show: function () {
        this.$el.show();
    },
    close: function () {
        this.current_search = null;
        this.search_string = '';
        this.searching = true;
        this.$el.hide();
    },
    move: function (direction) {
        var $next;
        if (direction === 'down') {
            $next = this.$('li.o-selection-focus').next();
            if (!$next.length) $next = this.$('li').first();
        } else {
            $next = this.$('li.o-selection-focus').prev();
            if (!$next.length) $next = this.$('li').last();
        }
        this.focus_element($next);
    },
    is_expandable: function () {
        return !!this.$('.o-selection-focus .o-expand').length;
    },
    is_expanded: function() {
        return this.$el[0].style.display === "block";
    },
    /**
     * Update search dropdown menu based on new input content.
     *
     * @private
     */
    _updateSearch: function () {
        var search_string = this.get_search_string();
        if (this.search_string !== search_string) {
            if (search_string.length) {
                this.search_string = search_string;
                this.initiate_search(search_string);
            } else {
                this.close();
            }
        }
    },
});
});
