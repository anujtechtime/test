odoo.define('aspl_pos_close_session.pos_session', function(require) {
	"use strict";
	
	var session = require('web.session');
	var chrome = require('point_of_sale.chrome');  
	var gui = require('point_of_sale.gui');
	var models = require('point_of_sale.models');
	var PopupWidget = require('point_of_sale.popups');
	var core = require('web.core');
	var QWeb = core.qweb;
	var _t = core._t;
	
	/** POS Session- Set Closing Balance - POP-UP widget * */
	var PopupBalanceWidget = PopupWidget.extend({
	    template: 'PopupBalanceWidget', 
	    events: _.extend({}, PopupWidget.prototype.events, {
	        'click .cashbox-add': 'onclick_cashboxadd',
	        'click .cashbox-delete': 'onclick_cashboxdelete',		
	        'blur .cashbox-edit' : 'onchange_text',
	    }),
	    
	    onclick_cashboxadd: function(e){
	    	console.log("eeeeeeeeeeeeeeeeeeee",e)
		   var self = this;		  			
		   var table = document.getElementById('cashbox-grid');			
		   var rowCount = table.getElementsByTagName("tbody")[0].getElementsByTagName("tr").length;
		   
		   var newRow = table.insertRow(rowCount);
		   var row = rowCount-1 ;
		   newRow.id = row;
	        
		   var col1html = "";
		   var col2html = "<input id='cashbox_"+row+"_coin_value' value='0' name='coin_value' class='cashbox-edit'/>";
		   var col3html = "<input id='cashbox_"+row+"_number' value='0' name='number' class='cashbox-edit' onkeypress='return (event.charCode &gt;= 48 &amp;&amp; event.charCode &lt;= 57) || (event.charCode == 0 || event.charCode == 08 || event.charCode == 127)'/>";
		   var col4html = "";
		   var col5html = "<span class='cashbox-delete fa fa-trash-o' name='delete'/>";
		
		   var col1 = newRow.insertCell(0); col1.style="display:none"; col1.innerHTML=col1html;
		   var col2 = newRow.insertCell(1); col2.innerHTML=col2html;
		   var col3 = newRow.insertCell(2); col3.innerHTML=col3html;
		   var col4 = newRow.insertCell(3); col4.id ="cashbox_"+row+"_subtotal"; col4.innerHTML=col4html;
		   var col5 = newRow.insertCell(4);
		   if(self.options.pos_cashbox_line[0]['is_delete']){
			   col5.innerHTML=col5html;       
		   }
		  
	    },
	    
	    onclick_cashboxdelete: function(e){
	    	var self = this;       	        
	    	var tr = $(e.currentTarget).closest('tr');	    	  
	    	var record_id = tr.find('td:first-child').text(); 
	    	if(parseInt(record_id))
	    		tr.find("td:not(:first)").remove();
	    	else
		    	tr.find("td").remove(); 
	    	tr.hide();
	    	var tr_id = tr.attr('id');
	    	var tbl = document.getElementById("cashbox-grid");				
		    var row = tbl.getElementsByTagName("tbody")[0].getElementsByTagName("tr");	
		    var total = 0;
   	        for (var i = 0; i < row.length-1; i++) 
   	        {	
   	        	var cell_count = row[i].cells.length;
   	        	if(cell_count > 1)
   	        	{
   	        		var subtotal = document.getElementById("cashbox_" + i + "_subtotal").innerHTML;
   	        		if(subtotal)
   	        			total += parseFloat(subtotal);
   	        	}
   	        }
   	        document.getElementById("cashbox_total").innerHTML = total ;
	    },
	    
	    onchange_text: function(e){
	    	var self = this;
	    	var tr = $(e.currentTarget).closest('tr');
	    	var tr_id = tr.attr('id');
	        var number = document.getElementById("cashbox_" + tr_id + "_number").value;
	        var coin_value = document.getElementById("cashbox_" + tr_id + "_coin_value").value;
	        document.getElementById("cashbox_" + tr_id + "_subtotal").innerHTML = number * coin_value;  
	        var tbl = document.getElementById("cashbox-grid");				
		    var row = tbl.getElementsByTagName("tbody")[0].getElementsByTagName("tr");	
		    var total = 0;
   	        for (var i = 0; i < row.length-1; i++) 
   	        {		
   	        	var cell_count = row[i].cells.length;
   	        	if(cell_count > 1)
   	        	{
   	        		var subtotal = document.getElementById("cashbox_" + i + "_subtotal").innerHTML;
   	        		if(subtotal)
   	        			total += parseFloat(subtotal);
   	        	}
   	        }
   	        document.getElementById("cashbox_total").innerHTML = total ;
	    },
	});
    gui.define_popup({name:'popupBalance', widget: PopupBalanceWidget});
	
	/** POS Session- PutMoneyIn - POP-UP widget * */
	var PopupMoneyWidget = PopupWidget.extend({
	    template: 'PopupMoneyWidget', 
	});
    gui.define_popup({name:'popupMoney', widget: PopupMoneyWidget});
	
	/** Session POP-UP widget * */
	var PopupSessionWidget = PopupWidget.extend({
	    template: 'PopupSessionWidget',
	    events: _.extend({}, PopupWidget.prototype.events, {
	        'click .PutMoneyIn': 'onclick_PutMoneyIn',
	        'click .TakeMoneyOut': 'onclick_TakeMoneyOut',	
	        'click .SetClosingBalance': 'onclick_SetClosingBalance',
	        'click .EndOfSession': 'onclick_EndOfSession',
	        'click .ValidateClosingControl': 'onclick_vcpentries',
	        'click .printstatement': 'onclick_printstatement',	
	    }),
	    
	    onclick_PutMoneyIn: function(){
	    	var self = this;	    	
	    	self.pos.gui.show_popup('popupMoney',{
                'title': _t('Put Money In'),
                'body': _t('Fill in this form if you put money in the cash register:'),
                confirm: function(){                	
                	var values ={};

                	console.log("ccccccccccccccccccccccccc")   
                	values.reason = this.$('.reason').val();
                	values.amount = this.$('.amount').val();
                	values.session_id = self.pos.pos_session.id;    
                	
                	self._rpc({
                		model: 'cash.box.in',
    	                method: 'run_from_ui',
    	                args: [0,values],
    	            }).then(function (result) {
    	            	if(result)
    	            		self.pos.gui.show_popup('error',{
    	            			'title': _t('Put Money In'),
    	            			'body': _t(JSON.stringify(result)),				                    
    	            		});
    	            	else
    	            		$('#close_session').trigger('click');
    	            });                	
                },
                cancel: function(){
                	$('#close_session').trigger('click');
                },
     		});		      
	    },	
	    
	    onclick_TakeMoneyOut: function(){
	    	var self = this;	

	    	self.pos.gui.show_popup('popupMoney',{
                'title': _t('Take Money Out'),
                'body': _t('Describe why you take money from the cash register:'),
                confirm: function(){    
                	var values ={};
                	console.log("ccccccccccccccccccccccccc11111111111")   
                	values.reason = this.$('.reason').val();
                	values.amount = this.$('.amount').val();
                	values.session_id = self.pos.pos_session.id;
                	self._rpc({
                		model: 'cash.box.out',
    	                method: 'run_from_ui',
    	                args: [0,values],
    	            }).then(function(result){ 
    	            	if(result){
    	            		xxxxxxxxxxxxxxx
    	            	}
    	       
    	            	else{
    	            		xcccccccccccccc
    	            	}
    	            		
    	         
    	            });               	
                },
                cancel: function(){
                	self.gui.show_popup('cash_control',{
                            title:'Closing Cash Control',
                            statement_id:self.statement_id,
                    });
                },
     		});	
	    },
	    
	    onclick_SetClosingBalance: function(e){
	    	var self = this;
	    	var tr = $(e.currentTarget);
	    	var balance = tr.attr('value');
	    	var check = "";
	    	self._rpc({
                model: 'pos.session',
                method: 'get_cashbox',
                args: [0, self.pos.pos_session.id,balance,check],
            }).then(function(result){ 						
            	self.pos.gui.show_popup('popupBalance',{
            		'title': _t('Cash Control'),
            		'pos_cashbox_line': result,
            		confirm: function(){       			                   
            			var values = [];
            			var tbl = document.getElementById("cashbox-grid");				
            			var row = tbl.getElementsByTagName("tbody")[0].getElementsByTagName("tr");	    			      		   
            			if (tbl != null) {	
            				for (var i = 0; i < row.length-1; i++) 
            				{		    			           	            	
            					var id=null, number=null,coin_value=null;
            					var cell_count = row[i].cells.length;
            					for (var j = 0; j < cell_count ? 3 : 0; j++)
            					{	    			           	                		    			           	                	
            						if(j==0)
            							id = row[i].cells[j].innerHTML;	    			                           	
            						var children = row[i].cells[j].childNodes;
            						for (var k = 0; k < children.length; k++)
            						{	    			           	                		
            							if(children[k].value)
            							{	    			           	                			
            								if(j==1)
            									coin_value = children[k].value;
            								if(j==2)
            									number = children[k].value;	
            							}
            						}	    			           	                
            					}
            					if(cell_count > 0)
            						values.push({'id':parseInt(id),number,coin_value});	
            				}	
            			} 
            			self._rpc({
            				model: 'account.bank.statement.cashbox',
            				method: 'validate_from_ui',
            				args: [0,self.pos.pos_session.id,balance,values],
            			}).then(function(result){ 
            				if(result)
            					self.pos.gui.show_popup('alert',{
            						'title': _t('Cash Control !!!!'),
            						'body': _t(JSON.stringify(result)),	
            						'cancel' : function() {	
            							$('.session').trigger('click');
            						}
            					}); 							
            				else
            					$('.session').trigger('click');
            			});
            		},
            		cancel: function(){
            			$('.session').trigger('click');
            		},
            	}); 							
            });
	    },
	    
	    onclick_vcpentries: function(){
	    	var self = this;
	    	var id = self.pos.pos_session.id;
	    	self._rpc({
	    		model: 'pos.session',
                method: 'action_pos_session_validate',
                args: [id],
            }).then(function(result){  
            	self.gui.close_popup();
            	self.gui.close();
			},function(err,event){
				event.preventDefault();
	            var err_msg = 'Please verify the details given or Check the Internet Connection./n';
	            if(err.data.message)
	            	err_msg = err.data.message;
	            self.gui.show_popup('alert',{
	            	'title': _t('Odoo Warning'),
	                'body': _t(err_msg),
	                cancel: function(){
	                }
	            });
			}); 
	    },
	    
	    onclick_EndOfSession: function(){
	    	var self = this;
	    	var id = self.pos.pos_session.id;   
	    	self._rpc({
                model: 'pos.session',
                method: 'action_pos_session_closing_control',
                args: [id],
	    	}).then(function(result){  
	    		$('.session').trigger('click');
			},function(err,event){
	            event.preventDefault();
	            var err_msg = 'Please verify the details given or Check the Internet Connection./n';
	            if(err.data.message)
	            	err_msg = err.data.message;
	            self.gui.show_popup('alert',{
	                'title': _t('Odoo Warning'),
	                'body': _t(err_msg),
	            });
	        });  
	    },
	    
	    /** Session Report ** */
	    onclick_printstatement: function(){
	    	var self = this;
	    	var id = self.pos.pos_session.id;
	    	self.chrome.do_action('aspl_pos_close_session.pos_session_report',
	    			{additional_context:{active_ids:[id],}
	    			});
	    },
	    
	});
    gui.define_popup({name:'popupsession', widget: PopupSessionWidget});

    
    /** * Render Session Button - Session Click Action ** */
	chrome.OrderSelectorWidget.include({	
		template : 'OrderSelectorWidget',
		
		init: function(parent, options) {
	        this._super(parent, options);
	    },
	    
	    renderElement: function() {
	        var self = this;
	        this._super();		              		        
	        this.$('.session').click(function(event){
	        	self._rpc({
	                model: 'pos.session',
	                method: 'get_pos_session',
	                args: [0, self.pos.pos_session.id],
	            }).then(function(result){ 
	            	if(result)
	            		self.pos.gui.show_popup('popupsession',{
	            			'title': _t('Sessions'),
	            			'pos_session': result,
	            		}); 							
	            	else
	            		self.pos.gui.show_popup('error',{
	            			'title': _t('Sessions'),
	            			'body': _t('No Opened Session.'),	                   
	            		});	
	            });
	        	
	        	self.pos.gui.show_popup('popupsession',{
	        		'title': _t('Sessions'),
	        		'body': _t('Loading...'),
	        	});
	        });
	    },		    
	});
});