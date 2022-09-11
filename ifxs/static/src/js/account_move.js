odoo.define('account.move', function (require) {
"use strict";

var AbstractField = require('web.AbstractField');
var AbstractController = require("web.AbstractController");
var core = require('web.core');

var ListController = require('web.ListController');
var ListView = require('web.ListView');

var field_registry = require('web.field_registry');
var field_utils = require('web.field_utils');

var BasicController = require('web.BasicController');

var QWeb = core.qweb;
var _t = core._t;




// $(function() {
//         (function($) {
//             $(document).on('click', '.o_list_button_fetch_data', function (e) {
//                 console.log("test##################");
//                 event.preventDefault();
//         var self = this;
//         console.log("self@@@@@@@@@@@@@@@@@",self);
//         var id = $(event.target).data('id') || false;
//         this._rpc({
//                 model: 'account.move',
//                 method: 'action_done_test',
//                 args: [],
//             }).then(function () {
//                 console.log("test###############")
//                 self.trigger_up('reload');
//             });
//             // e.stopPropagation();
//         });
//     }) (jQuery);
//     });



    // var LeadMiningRequestListController = ListController.extend({
    //     willStart: function() {
    //         var self = this;
    //         var ready = this.getSession().user_has_group('sales_team.group_sale_manager')
    //             .then(function (is_sale_manager) {
    //                 if (is_sale_manager) {
    //                     self.buttons_template = 'LeadMiningRequestListView.buttons';
    //                 }
    //             });
    //         return Promise.all([this._super.apply(this, arguments), ready]);
    //     },
    //     renderButtons: function () {
    //         this._super.apply(this, arguments);
    //         renderGenerateLeadsButton.apply(this, arguments);
    //     }
    // });


var ShowPaymentLineWidgetAccount = BasicController.extend({
    /**
     * This key contains the name of the buttons template to render on top of
     * the list view. It can be overridden to add buttons in specific child views.
     */
    // buttons_template: 'ListView.buttons',
    events: _.extend({}, BasicController.prototype.events, {
        // 'click .o_list_export_xlsx': '_onDirectExportData',
        'click .o_list_button_fetch_data' : "_onOutstandingCreditAssign",
    }),
// var  = ListController.extend({
//     buttons_template: 'ListView.buttons',
//     events: _.extend({}, ListController.prototype.events, {
//         'click .o_list_button_fetch_data': '_onOutstandingCreditAssign',
//     }),

    // events: _.extend({
    //     'click .o_list_button_fetch_data': '_onOutstandingCreditAssign',
    // }, ListController.prototype.events),
    // supportedFieldTypes: ['char'],

    // custom_events: _.extend({}, AbstractController.prototype.custom_events, {}),

    //--------------------------------------------------------------------------
    // Public
    //--------------------------------------------------------------------------
    init: function (parent, model, renderer, params) {
      this._super.apply(this, arguments);
    },


    _onOutstandingCreditAssign: function (event) {
        cccccccccccc
        event.stopPropagation();
        event.preventDefault();
        var self = this;
        var id = $(event.target).data('id') || false;
        this._rpc({
                model: 'account.move',
                method: 'js_assign_outstanding_line',
                args: [JSON.parse(this.value).move_id, id],
            }).then(function () {
                self.trigger_up('reload');
            });
    },
    
});

// field_registry.add('payment', ShowPaymentLineWidget);

return ShowPaymentLineWidgetAccount
    
});
