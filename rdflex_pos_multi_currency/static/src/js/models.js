odoo.define('rdflex_pos_multi_currency.models', function (require) {
var core = require('web.core');

var models = require('point_of_sale.models');
var PosBaseWidget = require('point_of_sale.BaseWidget');
var _t = core._t;

models.load_models({
    model: 'res.currency',
    fields: ['name','symbol','position','rounding','rate'],
    loaded: function (self, currencies) {
        self.multi_currencies = currencies;
    }
});

models.load_models({
    model: 'pos.payment.method',
    fields: ['id','currency_id'],
    loaded: function (self, currencies) {
        self.multi_payment_method = currencies;
    }
});

var _super_Order = models.Order.prototype;
models.Order = models.Order.extend({
    initialize: function () {
        _super_Order.initialize.apply(this, arguments);
        this.currency = this.pos.currency;
    },
    init_from_JSON: function (json) {
        _super_Order.init_from_JSON.apply(this, arguments);
        this.currency = json.currency;
    },
    export_as_JSON: function () {
        var values = _super_Order.export_as_JSON.apply(this, arguments);
        values.currency = this.currency;
        return values;

    },
    set_currency: function (currency) {
        console.log("currency@@@@@@@@@@@@@@@@@@",currency)
        if (this.currency.id === currency.id) {
            return;
        }
        var form_currency = this.currency || this.pos.currency;
        var to_currency = currency;
        this.orderlines.each(function (line) {
            line.set_currency_price(form_currency, to_currency);
        });
        this.currency = currency;
    },
    get_currency: function (){
        return this.currency;
    },
    add_paymentline: function (cashregister) {
        var paymentlines = this.get_paymentlines();
        var is_multi_currency = false;
        _.each(paymentlines, function (line) {
            console.log("line@@@@@@@@@@@@@@@@@@",line);
            if (line.payment_method.id !== cashregister.id) {
                is_multi_currency = true;
            }
        });
        if (is_multi_currency) {
            this.pos.gui.show_popup('alert', {
                title : _t("Payment Error"),
                body  : _t("Payment of order should be in same currency. Payment could not be done with two different currency"),
            });
        } else {

            
            console.log("cashregister@@@@@@@@@@@@@@",cashregister);
            console.log("this.currency@@@@@@@@@@@@",this);
            var journal_currency_id = cashregister.id;
            if (this.currency.id !== journal_currency_id) {
                console.log("journal_currency_id@@@@@@@@@@@@@@@@@@@@@@@@@",journal_currency_id)
                console.log("this.pos@@@@@@@@@@@@@@@@@@@@@",this.pos)
                var payment_method  = _.findWhere(this.pos.multi_payment_method, {id:journal_currency_id})
                console.log("payment_method@@@@@@@@@@@@@@",payment_method.currency_id[0]);

                
                var currency = _.findWhere(this.pos.multi_currencies, {id:payment_method.currency_id[0]})
                console.log("currency@@@@@@@@@@@@@@@@@",currency)
                if (currency){
                    this.set_currency(currency);
                }
            }
            _super_Order.add_paymentline.apply(this, arguments);
        }
    },
});

models.Orderline = models.Orderline.extend({
    set_currency_price: function (form_currency, to_currency){
        console.log("to_currency@@@@@@@@@@@@@",to_currency);
        console.log("form_currency@@@@@@@@@@@@@@@@@@",form_currency);
        var conversion_rate =  to_currency.rate / form_currency.rate;
        console.log("conversion_rate@@@@@@@@@@@@@@",conversion_rate)
        this.price = this.price * conversion_rate;
    },
});


PosBaseWidget.include({
    format_currency: function (amount,precision){
        var currency = (this.pos && this.pos.currency) ? this.pos.currency : {symbol:'$', position: 'after', rounding: 0.01, decimals: 2};
        amount = this.format_currency_no_symbol(amount, precision);
        currency = this.pos.get_order().currency || currency;
        if (currency.position === 'after') {
            return amount + ' ' + (currency.symbol || '');
        } else {
            return (currency.symbol || '') + ' ' + amount;
        }
    },
});


});
