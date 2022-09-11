/**
 * fx theme action manager
 */
odoo.define('fx_theme.ActionManager', function (require) {
    "use strict";

    var core = require('web.core');
    var dom = require('web.dom');
    var ActionManager = require('web.ActionManager');
    var fxThemePageHeader = require("fx_theme.page_header")
    var fxPageFooter = require('fx_theme.page_footer')

    var _t = core._t;

    var FxTHemeActionManager = ActionManager.include({
        template: "fx_theme.action_manager",
        pageHeader: undefined,
        pagerFooter: undefined,

        /**
         * append the action to the action box
         * @param {*} controller 
         */
        _appendController: function (controller) {
            // put the container to the action container
            dom.append(this.$('.fx_theme_action_container'), controller.widget.$el, {
                in_DOM: this.isInDOM,
                callbacks: [{ widget: controller.widget }],
            });

            if (controller.scrollPosition) {
                this.trigger_up('scrollTo', controller.scrollPosition);
            }
        },

        /*
        * add the pager header and page footer
        */
        start: function () {
            var self = this;
            return this._super.apply(this, arguments).then(function () {
                // header
                self.pageHeader = new fxThemePageHeader(self)
                self.pageHeader.appendTo(self.$('.page-header'))
                // footer
                self.pagerFooter = new fxPageFooter(self)
                self.pagerFooter.appendTo(self.$('.page-footer'))
            })
        },

        /**
         * change the default behavor
         * @param {*} controller 
         */
        // _pushController: function (controller) {
        //     var self = this;

        //     if (controller.viewType == 'form') {

        //         // 设置form
        //         // detach the current controller
        //         // this._detachCurrentController();

        //         // push the new controller to the stack at the given position, and
        //         // destroy controllers with an higher index
        //         var toDestroy = this.controllerStack.slice(controller.index);

        //         // reject from the list of controllers to destroy the one that we are
        //         // currently pushing, or those linked to the same action as the one
        //         // linked to the controller that we are pushing
        //         toDestroy = _.reject(toDestroy, function (controllerID) {
        //             return controllerID === controller.jsID ||
        //                 self.controllers[controllerID].actionID === controller.actionID;
        //         });
        //         this._removeControllers(toDestroy);

        //         this.controllerStack = this.controllerStack.slice(0, controller.index);
        //         this.controllerStack.push(controller.jsID);

        //         // append the new controller to the DOM
        //         this._appendController(controller);

        //         // notify the environment of the new action
        //         this.trigger_up('current_action_updated', {
        //             action: this.getCurrentAction(),
        //             controller: controller,
        //         });

        //         // close all dialogs when the current controller changes
        //         core.bus.trigger('close_dialogs');

        //         // toggle the fullscreen mode for actions in target='fullscreen'
        //         this._toggleFullscreen();
        //     } else {
        //         // detach the current controller
        //         this._detachCurrentController();

        //         // push the new controller to the stack at the given position, and
        //         // destroy controllers with an higher index
        //         var toDestroy = this.controllerStack.slice(controller.index);

        //         // reject from the list of controllers to destroy the one that we are
        //         // currently pushing, or those linked to the same action as the one
        //         // linked to the controller that we are pushing
        //         toDestroy = _.reject(toDestroy, function (controllerID) {
        //             return controllerID === controller.jsID ||
        //                 self.controllers[controllerID].actionID === controller.actionID;
        //         });
        //         this._removeControllers(toDestroy);
        //         this.controllerStack = this.controllerStack.slice(0, controller.index);
        //         this.controllerStack.push(controller.jsID);

        //         // append the new controller to the DOM
        //         this._appendController(controller);

        //         // notify the environment of the new action
        //         this.trigger_up('current_action_updated', {
        //             action: this.getCurrentAction(),
        //             controller: controller,
        //         });

        //         // close all dialogs when the current controller changes
        //         core.bus.trigger('close_dialogs');

        //         // toggle the fullscreen mode for actions in target='fullscreen'
        //         this._toggleFullscreen();
        //     }

        // },
    })

    return FxTHemeActionManager
});