odoo.define('payment_cashfree.cashfree', function(require) {
    "use strict";

    var ajax = require('web.ajax');
    var core = require('web.core');
    var _t = core._t;
    var qweb = core.qweb;
    ajax.loadXML('/payment_cashfree/static/src/xml/cashfree_templates.xml', qweb);

    // The following currencies are integer only, see
    // https://stripe.com/docs/currencies#zero-decimal
    var int_currencies = [
        'BIF', 'XAF', 'XPF', 'CLP', 'KMF', 'DJF', 'GNF', 'JPY', 'MGA', 'PYG',
        'RWF', 'KRW', 'VUV', 'VND', 'XOF'
    ];

    if ($.blockUI) {
        // our message needs to appear above the modal dialog
        $.blockUI.defaults.baseZ = 2147483647; //same z-index as StripeCheckout
        $.blockUI.defaults.css.border = '0';
        $.blockUI.defaults.css["background-color"] = '';
        $.blockUI.defaults.overlayCSS["opacity"] = '0.9';
    }

    require('web.dom_ready');
    if (!$('.o_payment_form').length) {
        return $.Deferred().reject("DOM doesn't contain '.o_payment_form'");
    }

    var observer = new MutationObserver(function(mutations, observer) {
        for(var i=0; i<mutations.length; ++i) {
            for(var j=0; j<mutations[i].addedNodes.length; ++j) {
                if(mutations[i].addedNodes[j].tagName.toLowerCase() === "form" && mutations[i].addedNodes[j].getAttribute('provider') == 'cashfree') {
                    display_cashfree_form($(mutations[i].addedNodes[j]));
                }
            }
        }
    });


    function display_cashfree_form(provider_form) {

        // Open Checkout with further options
        var payment_form = $('.o_payment_form');
        if(!payment_form.find('i').length)
            payment_form.append('<i class="fa fa-spinner fa-spin"/>');
            payment_form.attr('disabled','disabled');

        var get_input_value = function(name) {
            return provider_form.find('input[name="' + name + '"]').val();
        }

        var paymentMode = get_input_value("paymentMode");
        var paymentSessionId = get_input_value("paymentSessionId");
        var returnUrl = get_input_value("returnUrl");

        // Search if the user wants to save the credit card information
        var form_save_token = false;

        const cashfree = Cashfree({
				mode: paymentMode
		});
		let checkoutOptions = {
			paymentSessionId: paymentSessionId,
			returnUrl: returnUrl
		}
		cashfree.checkout(checkoutOptions).then(function(result){
			if(result.error){
				alert(result.error.message)
			}
			if(result.redirect){
				console.log('success')
			}
		});
    }

    $.getScript("https://sdk.cashfree.com/js/v3/cashfree.js", function(data, textStatus, jqxhr) {
        observer.observe(document.body, {childList: true});
        display_cashfree_form($('form[provider="cashfree"]'));
    });
});
