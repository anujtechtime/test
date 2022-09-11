odoo.define('point_of_sale.pos_product_image_magnify', function (require) {
"use strict";

var screens = require('point_of_sale.screens');
var gui = require('point_of_sale.gui');
var core = require('web.core');
var models = require("point_of_sale.models");
var AbstractAction = require('web.AbstractAction')
var PopupWidget = require('point_of_sale.popups');
var PosBaseWidget = require('point_of_sale.BaseWidget');
var ProductListWidget = screens.ProductListWidget;
var OrderWidget = screens.OrderWidget;
var ActionpadWidget = screens.ActionpadWidget;
var QWeb = core.qweb;
var _t = core._t;

models.load_fields("product.product", ["qty_available", "type","location_wise_qty", 'default_code','virtual_available','purchased_product_qty']);
models.load_fields("stock.picking.type", ['default_location_src_id'])



ActionpadWidget.include({
    renderElement: function() {
        var self = this;
        // this._super();
        PosBaseWidget.prototype.renderElement.call(this);
        this.$('.pay').click(function(){
            var order = self.pos.get_order();
            console.log("orderrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrr",order)
            for (var i = 0; i < self.pos.get_order().orderlines.models.length; i++) {
                if (self.pos.get_order().orderlines.models[i].product.location_wise_qty < 1){
                    console.log("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
                    self.gui.show_popup('error',{
                        'title': _t('An anonymous order cannot be confirmed'),
                        'body':  _t('Please select a product who have on hand quantity greater than 0 !'),
                    });
                    return;
                }
            }
            var has_valid_product_lot = _.every(order.orderlines.models, function(line){
                return line.has_valid_product_lot();
            });

            var has_no_quantity = _.every(order.orderlines.models, function(lines){
                console.log("lines@@@@@@@@@@@@@@@@@@@@@@@@@",lines)
                // return line.has_valid_product_lot();
            });
            if(!has_valid_product_lot){
                self.gui.show_popup('confirm',{
                    'title': _t('Empty Serial/Lot Number'),
                    'body':  _t('One or more product(s) required serial/lot number.'),
                    confirm: function(){
                        self.gui.show_screen('payment');
                    },
                });
            }else{
                self.gui.show_screen('payment');
            }
        });
        this.$('.set-customer').click(function(){
            self.gui.show_screen('clientlist');
        });
    }
});



OrderWidget.include({
    init: function(parent, options) {
        var self = this;
        this._super(parent,options);

        this.numpad_state = options.numpad_state;
        this.numpad_state.reset();
        this.numpad_state.bind('set_value',   this.set_value, this);

        this.pos.bind('change:selectedOrder', this.change_selected_order, this);

        this.line_click_handler = function(event){
            // $('.orderline')[0].removeClass("selected");
            self.click_line(this.orderline, event);
        var data = this;
            self._rpc({
                model: 'pos.session',
                method: 'get_on_hand_location',
                args: [0, this.orderline.product.id],
            }).then(function(result){  
                var res_id = result
                var dict = {}
                var quant_line = 0
                for(var i = 0, len = result.length; i < len; i++){
                    var quant_line = 0;
                    if (result[i] != false){
                        var quant_line = self.pos.db.get_stock_quantity(result[i])[0]

                    }
                    dict[i] = quant_line;

                }
                console.log("purchased_product_qty1111111111111111111",data.orderline.product.purchased_product_qty)
                self.gui.show_popup('order_line_ids',{orderline:data.orderline,'discount' : data.orderline.discount ,'margin': data.orderline.get_margin(),'base_price' : data.orderline.get_base_price(),'quantity' : data.orderline.quantity, 'new_price' : data.orderline.price, 'price': data.orderline.product.lst_price, 
        'title': data.orderline.product.display_name,'virtual_available': data.orderline.product.purchased_product_qty,'code': data.orderline.product.default_code,'sale_price': data.orderline.product.lst_price, 'cost_price': data.orderline.product.standard_price,'product_id': data.orderline.product.id,'qty_available' : data.orderline.product.qty_available,'res_id0': dict[0],'res_id1' :dict[1] ,
                    'res_id2': dict[2],'res_id3':dict[3],'res_id4': dict[4],'res_id5': dict[5],'res_id6': dict[6],'res_id7': dict[7]});
            })
            .catch(function(err){
                self.gui.show_popup('order_line_ids',{orderline:data.orderline,'discount' : data.orderline.discount ,'margin': data.orderline.get_margin(),'base_price' : data.orderline.get_base_price(),'quantity' : data.orderline.quantity, 'new_price' : data.orderline.price, 'price': data.orderline.product.lst_price, 
        'title': data.orderline.product.display_name,'virtual_available': data.orderline.product.purchased_product_qty,'code': data.orderline.product.default_code,'sale_price': data.orderline.product.lst_price, 'cost_price': data.orderline.product.standard_price,'product_id': data.orderline.product.id,'qty_available' : data.orderline.product.qty_available});
            });
            // console.log("self.orderline@@@@@@@@@@@@@@@888888888888888888",self.Class);
        //     self.gui.show_popup('order_line_ids',{orderline:this.orderline,'discount' : this.orderline.discount ,'quantity' : this.orderline.quantity, 'new_price' : this.orderline.price, 'price': this.orderline.product.lst_price, 
        // 'title': this.orderline.product.display_name,'sale_price': this.orderline.product.lst_price, 'cost_price': this.orderline.product.standard_price,'product_id': this.orderline.product.id,'qty_available' : this.orderline.product.qty_available});
        };

        if (this.pos.get_order()) {
            this.bind_order_events();
        }

    },



    render_orderline: function(orderline){
        var el_str  = QWeb.render('Orderline',{widget:this, line:orderline}); 
        var el_node = document.createElement('div');
            el_node.innerHTML = _.str.trim(el_str);
            el_node = el_node.childNodes[0];
            el_node.orderline = orderline;
            console.log("el_node@@@@@@@@@@@@@@@@@@@@@@@@@@@@2222222222",el_node)
            el_node.addEventListener('dblclick',this.line_click_handler);
        orderline.node = el_node;
        return el_node;
    },

    orderline_add: function(){
        
        
        // var data = this;
        //     self._rpc({
        //         model: 'pos.session',
        //         method: 'get_on_hand_location',
        //         args: [0, this.orderline.product.id],
        //     }).then(function(result){  
        //         var res_id = result
        //         var dict = {}
        //         var quant_line = 0
        //         for(var i = 0, len = result.length; i < len; i++){
        //             var quant_line = 0;
        //             if (result[i] != false){
        //                 var quant_line = self.pos.db.get_stock_quantity(result[i])[0]

        //             }
        //             dict[i] = quant_line;

        //         }
        //         self.gui.show_popup('order_line_ids',{orderline:data.orderline,'discount' : data.orderline.discount ,'quantity' : data.orderline.quantity, 'new_price' : data.orderline.price, 'price': data.orderline.product.lst_price, 
        // 'title': data.orderline.product.display_name,'sale_price': data.orderline.product.lst_price, 'cost_price': data.orderline.product.standard_price,'product_id': data.orderline.product.id,'qty_available' : data.orderline.product.qty_available,'res_id0': dict[0],'res_id1' :dict[1] ,
        //             'res_id2': dict[2],'res_id3':dict[3],'res_id4': dict[4],'res_id5': dict[5],'res_id6': dict[6],'res_id7': dict[7]});
        //     });
        this.numpad_state.reset();
        this.renderElement('and_scroll_to_bottom');
        console.log("change_selected_order@@@@@@@@@@@@@@@@@@w23343234323443234323324432",this.pos.get_order().orderlines.models.length)
        for (var i = 0; i < this.pos.get_order().orderlines.models.length; i++) {
            console.log("this.pos.get_order().orderlines.models[i].selected@@@@@@@@@@@@@@@",this.pos.get_order().orderlines.models[i].selected)
            if (this.pos.get_order().orderlines.models[i].selected == true || this.pos.get_order().orderlines.models.length == 1){
                if (this.pos.get_order().orderlines.models.length == 1){
                    var model_data = this.pos.get_order().orderlines.models[i]
                    var productid = this.pos.get_order().orderlines.models[i].product.id
                }
                else{
                    var model_data = this.pos.get_order().orderlines.models[i + 1]
                    var productid = this.pos.get_order().orderlines.models[i + 1].product.id
                }

                this.pos.get_order().select_orderline(this.pos.get_order().orderlines.models[i]);
                var data = this;
            var rpc_call = data._rpc({
                model: 'pos.session',
                method: 'get_on_hand_location',
                args: [0, productid],
            }).then(function(result){  
                var res_id = result
                var dict = {}
                var quant_line = 0
                for(var i = 0, len = result.length; i < len; i++){
                    var quant_line = 0;
                    if (result[i] != false){
                        var quant_line = data.pos.db.get_stock_quantity(result[i])[0]

                    }
                    dict[i] = quant_line;

                }
                console.log("data.pos.get_order().orderlines.models[i]@@@@@@@@@@@@@@@",model_data.discount)
                data.gui.show_popup('order_line_ids',{orderline:model_data,'discount' : model_data.discount ,'margin': model_data.get_margin(),'base_price' : model_data.get_base_price(),'quantity' : model_data.quantity, 'new_price' : model_data.price, 'price': model_data.product.lst_price, 
        'title': model_data.product.display_name,'virtual_available': model_data.product.purchased_product_qty,'code': model_data.product.default_code,'sale_price': model_data.product.lst_price, 'cost_price': model_data.product.standard_price,'product_id': model_data.product.id,'qty_available' : model_data.product.qty_available,'res_id0': dict[0],'res_id1' :dict[1] ,
                    'res_id2': dict[2],'res_id3':dict[3],'res_id4': dict[4],'res_id5': dict[5],'res_id6': dict[6],'res_id7': dict[7]});
            })
            .catch(function(err){
                console.log("errrrrrrrrrrrrrrrrrrrrrr",err)
                data.gui.show_popup('order_line_ids',{orderline:model_data,'discount' : model_data.discount ,'margin': model_data.get_margin(),'base_price' : model_data.get_base_price(),'quantity' : model_data.quantity, 'new_price' : model_data.price, 'price': model_data.product.lst_price, 
        'title': model_data.product.display_name,'virtual_available': model_data.product.purchased_product_qty,'code': model_data.product.default_code,'sale_price': model_data.product.lst_price, 'cost_price': model_data.product.standard_price,'product_id': model_data.product.id,'qty_available' : model_data.product.qty_available});
            });

            console.log("rpc_call@@@@@@@@@@@@@@@@@@@@@",rpc_call)
            }
        }
    },
    
});

ProductListWidget.include({
    init: function(parent, args) {
        this._super(parent, args);
        this.options = {};
        
    },
    renderElement: function() {
    var el_str  = QWeb.render(this.template, {widget: this});
    var el_node = document.createElement('div');
        el_node.innerHTML = el_str;
        el_node = el_node.childNodes[1];


    var self = this;
    let picking_type_id = self.pos.config.picking_type_id[0];
    self._rpc({
        model: 'product.product',
        method: 'get_location_qty',
        args: [picking_type_id],
    }).then(function(return_value) {
        var returned_values = return_value;
        $.each(returned_values, function(placeholder, product_location_qty ){
            var product_id = self.pos.db.get_product_by_id(product_location_qty.id);
            if (product_id) {
                product_id.location_wise_qty = product_location_qty.location_wise_qty;
                var product_node = self.render_product(product_id);
                product_node.querySelector('.qty-tag').innerHTML = product_location_qty.location_wise_qty
                
            }
        });
    });

    if(this.el && this.el.parentNode){
        this.el.parentNode.replaceChild(el_node,this.el);
        }
    this.el = el_node;
    var list_container = el_node.querySelector('.product-list');
    for(var i = 0, len = this.product_list.length; i < len; i++){
        var product_node = this.render_product(this.product_list[i]);
        product_node.addEventListener('click',this.click_product_handler);
        list_container.appendChild(product_node);
        }
    },
    get_product_image_large: function(product){
        return window.location.origin + "/web/image/product.product/" + product.id + "/image_128";
    },

    on_click_pos_product_magnify: function (e) {
        console.log("eeeeeeeeeeeeeeeeeeeee@",e)
        var self = this;
        e.stopPropagation();
        var $target = $(e.currentTarget).parent();
        var product_id = $target.data('product-id');
        var product = this.pos.db.get_product_by_id(product_id);
        console.log("product@@@@@@@@@@@@@@@@@@",product)
        var image_url = this.get_product_image_large(product);
        var sale_price = this.pos.db.get_product_by_id(product_id).lst_price;
        var cost_price = this.pos.db.get_product_by_id(product_id).standard_price;
        var qty_available = this.pos.db.get_product_by_id(product_id).qty_available;
        var stoc_location = this.pos.db.get_stock_picking_id(this.pos.config.picking_type_id[0]);
        var location = this.pos.config.picking_type_id[1]


        this.target_product_id = product_id
        self._rpc({
                model: 'pos.session',
                method: 'get_on_hand_location',
                args: [0, product.id],
            }).then(function(result){  
                console.log("result@@@@@@@@@@@@@@@",result)
                var res_id0 = result[0];
                var res_id1 = result[1];
                var res_id2 = result[2];
                var res_id3 = result[3];
                var res_id4 = result[4];
                var res_id5 = result[5];
                var res_id6 = result[6];
                var res_id7 = result[7];
                self.gui.show_popup('product_image',{image_url:image_url, 'title': product.display_name,'sale_price': sale_price, 'cost_price': cost_price,'res_id0': res_id0, 'res_id1' :res_id1 ,
                    'res_id2': res_id2,'res_id3':res_id3,'res_id4': res_id4,'res_id5': res_id5,'res_id6': res_id6,'res_id7': res_id7,'product_id': product_id,'qty_available' : qty_available});

            });
        
    },
});

var ProductZoomPopupWidget = PopupWidget.extend({
    template: 'ProductZoomPopupWidget',
    events: _.extend({}, PopupWidget.prototype.events, {
        'change #cars':'onclick_SetClosingBalance',
        }),

    onclick_SetClosingBalance: function(event){
        console.log("eeeeeeeeeeeeeeeeeeeqqqqqqqqqqq1111111111111111qqqqqq",this.pos.config_id)
            var self = this;
            var $target = $(event.currentTarget)
            var balance = $target.attr('value');


            // self._rpc({
            //     model: 'pos.session',
            //     method: 'set_location_for_inventory',
            //     args: [0, event.currentTarget.value , this.pos.config_id],
            // }).then(function(rests){  
            //     console.log("v@@@@@@@@@@@@@wwwwwwwwwwwwwwwwwww@@@@@@@@@@@",rests)
                
            //     document.getElementById("product_location").innerHTML = rests;
            
            // });

            var check = "";
            self._rpc({
                model: 'pos.session',
                method: 'get_on_hand_location_onchange',
                args: [0, event.currentTarget.value , balance],
            }).then(function(rest){  
                console.log("v@@@@@@@@@@@@@@@@@@@@@@@@",rest)
                if (rest != undefined){
                document.getElementById("on_hand").innerHTML = rest;
            }
            });
        },

    show: function(options){
        console.log("optionsWWWWWWWWWWWWWWWWWWWWWW",options)
        options = options || {};
        var self = this;
        this._super(options);
        this.image_url    = options.image_url
        this.renderElement();
    }
});
gui.define_popup({name:'product_image', widget: ProductZoomPopupWidget});



var OrderLineZoomPopupWidget = PopupWidget.extend({
    template: 'OrderLineZoomPopupWidget',
    events: _.extend({}, PopupWidget.prototype.events, {
        'click .confirm':'onclick_SetClosingBalance',
        'change #new_price':'onchange_net_price',
        'change #quantity':'onchange_quantity',
        'change #discount':'onchange_discount',
        }),


onchange_net_price: function(ev){
        console.log("ev@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@",ev)
        var price = this.$('#price').val();
        var new_price = this.$('#new_price').val();
        // this.pos.get_order().get_selected_orderline().set_unit_price(new_price);
            console.log("new_price@@@@@@@@@@@@@@@",new_price)
            var quantity = this.$('#quantity').val();
            // this.$('#discount')[0].value = ((price - new_price) * quantity).toFixed(2);
            this.$('#discount')[0].value = (((price - new_price) / price) * 100).toFixed(2);
            var discount = this.$('#discount').val();
            this.pos.get_order().get_selected_orderline().set_discount(discount);
            this.$('#subtotal')[0].value = (quantity * new_price).toFixed(2);
           this.$('#margin')[0].value = ((new_price - this.pos.get_order().get_selected_orderline().product.standard_price) / price * 100).toFixed(2);
        //     self.discount = (price - new_price) / price * 100
        // if self.net_price > 0 and self.price_unit > 0:        
        //     self.margin = (self.net_price - self.product_id.standard_price) /  self.net_price * 100
        // self.net_price = self.price_unit * (1 - (self.discount or 0.0) / 100.0)
    },

    onchange_quantity: function(ev){
        console.log("ev@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@",ev)
        var quantity = this.$('#quantity').val();
        var new_price = this.$('#new_price').val();
        var discount = this.$('#discount').val();
        var price = this.$('#price').val();
        // this.$('#discount')[0].value = ((price - new_price) * quantity).toFixed(2);
        this.$('#discount')[0].value = (((price - new_price) / price) * 100).toFixed(2);
        // this.$('#subtotal')[0].value = ((quantity * price) -  discount).toFixed(2);
        this.$('#subtotal')[0].value = (quantity * new_price).toFixed(2);
                   this.$('#margin')[0].value = ((new_price - this.pos.get_order().get_selected_orderline().product.standard_price) / price * 100).toFixed(2);

            // console.log("new_price@@@@@@@@@@@@@@@",new_price)
            // var quantity = this.$('#quantity').val() = ;
            // var discount = this.$('#discount').val() = ;
    },

    onchange_discount: function(ev){
        console.log("ev@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@",ev);
        var quantity = this.$('#quantity').val();
        var new_price = this.$('#new_price').val();
        var discount = this.$('#discount').val();
        var price = this.$('#price').val();



        
        // this.$('#new_price')[0].value = (price - (discount / quantity)).toFixed(2);
        this.$('#new_price')[0].value = price * (1 - discount / 100.0).toFixed(2);
        // this.$('#new_price')[0].value = (price - (price / discount)).toFixed(2)
        // this.$('#subtotal')[0].value = ((quantity * price) -  discount).toFixed(2);
        var new_price = price * (1 - discount / 100.0)
        this.$('#subtotal')[0].value = (quantity * new_price).toFixed(2);

        this.$('#margin')[0].value = ((new_price - this.pos.get_order().get_selected_orderline().product.standard_price) / price * 100).toFixed(2);


            console.log("new_price@@@@@@@@@@@@@@@",new_price)
            // var quantity = this.$('#quantity').val() = ;
            // var discount = this.$('#discount').val() = ;
    },



    onclick_SetClosingBalance: function(event){
            var self = this;
            var $target = $(event.currentTarget).parent()
            console.log("$target@@@@@@@@@@@@@@@@@@@@@",$target)
            var balance = $target.attr('value');


            var new_price = this.$('#new_price').val();
            console.log("new_price@@@@@@@@@@@@@@@",new_price)
            var quantity = this.$('#quantity').val();
            var discount = this.$('#discount').val();
            // this.orderline.discount = 50;
            // this.orderline.discountStr = 50;
            this.orderline.price = new_price;
            if (this.orderline.product.location_wise_qty <= 0){
                self.gui.show_popup('error',{
                        'title': _t('An anonymous order cannot be confirmed'),
                        'body':  _t('Please select a product who have on hand quantity greater than 0 !'),
                    });
                    return false;
            }
            // this.orderline.quantity = 7;
            // this.orderline.quantityStr = 8
            // {orderline:this.orderline,'discount' : this.orderline.discount ,'quantity' : this.orderline.quantity, 'new_price' : this.orderline.price, 'price': this.orderline.product.lst_price});
            var order_line  = this.pos.get_order().select_orderline(this.orderline)
            var selected_orderline = this.pos.get_order().get_selected_orderline();
                selected_orderline.price_manually_set = true;
                selected_orderline.set_unit_price(new_price);
            this.pos.get_order().get_selected_orderline().set_unit_price(new_price);
            this.pos.get_order().get_selected_orderline().set_quantity(quantity);
            this.pos.get_order().get_selected_orderline().set_discount(discount);
            this.trigger('change',this);

            // set_unit_price(val);
            // set_discount
        this.gui.close_popup();

        },


    show: function(options){
        console.log("options@@@@@@@@@@@@@@@",options)
        options = options || {};
        var self = this;
        this._super(options);
        this.orderline    = options.orderline
        this.renderElement();
    }
});
gui.define_popup({name:'order_line_ids', widget: OrderLineZoomPopupWidget});



var models = require('point_of_sale.models');


// models.Product = models.Product.extend({
//         location_wise_qty: function() {
//             return this.location_qty;
//         },
//     });

models.load_models([

{

 model:  'stock.location',
    fields: ['name', 'id','usage'],
    loaded: function(self, brand){

        console.log("brand@@@@@@@@@@@@@",brand)
        self.db.get_brand_by_id(brand);
        self.location_id = brand;
    },
},
{

 model:  'stock.picking.type',
    fields: ['name', 'id', 'default_location_src_id'],
    loaded: function(self, stock){

        self.db.get_stock_picking_id(stock);
        self.stock_id = stock;
    },
},
{
// models.load_fields("stock.quant", ['product_id',"quantity","location_id"])
 model:  'stock.quant',
    fields: ['product_id',"quantity","location_id"],
    loaded: function(self, qty){
        console.log("qty@@@@@@@@@@@@@@@@@@@",qty)
        self.db.get_stock_quantity(qty);
        self.qty_id = qty;
    }
},],{'after': 'product.product'});



var DB = require('point_of_sale.DB');
    var utils = require('web.utils');
    // models.load_fields('product.product', 'product_brand_id');
    
    DB.include({
        init: function(options){
        options = options || {};
        this.name = options.name || this.name;
        this.limit = options.limit || this.limit;
        
        if (options.uuid) {
            this.name = this.name + '_' + options.uuid;
        }

        //cache the data in memory to avoid roundtrips to the localstorage
        this.cache = {};

        this.product_by_id = {};
        this.product_by_barcode = {};
        this.product_by_category_id = {};
        this.product_by_brand = {};
        this.partner_sorted = [];
        this.partner_by_id = {};
        this.partner_by_barcode = {};
        this.partner_search_string = "";
        this.partner_write_date = null;

        this.category_by_id = {};
        this.root_category_id  = 0;
        this.category_products = {};
        this.category_ancestors = {};
        this.brand_ancestors ={};
        this.category_childs = {};
        this.brand_product = {};
        this.loc_qty = {};
        this.category_parent    = {};
        this.category_search_string = {};
        this.stock_picking_type_id = {};
    },

    get_brand_by_id: function(brand){
        var brand_list  = this.brand_product;
        
            var list = [];
            for(var i = 0, len = brand.length; i < len; i++){
                   if(brand[i].usage == "internal"){
                brand_list[brand[i].name] = [brand[i]];
            }
            }
            return brand;
    },

    get_stock_quantity: function(qty){
        var qty_list  = this.loc_qty;
        if(qty instanceof Array){
            var list = [];
            for(var i = 0, len = qty.length; i < len; i++){
                qty_list[qty[i].id] = [qty[i].quantity, qty[i].location_id[1]];
            }
            return qty;
        }
        else{

            return this.loc_qty[qty];
        }
    },

    get_stock_picking_id: function(stock){
        var stock_list  = this.stock_picking_type_id;
        if(stock instanceof Array){
            var list = [];
            for(var i = 0, len = stock.length; i < len; i++){
                stock_list[stock[i].id] = [stock[i]];
            }
            return stock;
        }
        else{
            return this.stock_picking_type_id[stock];
        }
    },



         

    });

});

