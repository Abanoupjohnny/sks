frappe.ui.form.on("Sales Order",{
    after_save:function(frm,cdt,cdn){
        frappe.db.get_single_value("SKS Settings","customer_transaction_history").then(value =>{
            if(value==1){
                var data=locals[cdt][cdn]
                if(cur_frm.doc.docstatus!=1){
                    frappe.call({
                        method:"sks.sks.custom.py.sales_order.customer_transaction_history",
                        args:{
                            customer:data.customer
                        },
                        callback: function(r){
                            const d = new frappe.ui.Dialog({
                                title: "Customer transaction history",
                                static: true,
                                fields:[
                                {
                                    fieldname:'table',
                                    fieldtype:'HTML',
                                    label:'Table'
                                },
                                {
                                    fieldname:'items_add',
                                    fieldtype:'MultiSelectPills',
                                    label:'Select items to be added',
                                    get_data: function() {
                                        return r.message[2]
                                    }
                                }
                                ],
                                primary_action : function(data){
                                    frappe.call({
                                        method:"sks.sks.custom.py.sales_order.item_append",
                                        args:{item_code:data.items_add,current_document:cur_frm.doc.name},
                                    callback(r){
                                        frm.reload_doc();
                                    }
                                    })
                                    d.hide()
                                }
                            })
                        var template = "<table><tbody>{% for (var row in rows) { %}<tr>{% for (var col in rows[row]) { %}<td> {{ rows[row][col] }}</td> <td> {{ days[row][col] }}</td>{% } %}</tr>{% } %}</tbody></table>"
                        d.set_df_property('table', 'options', frappe.render(template, {rows:r.message[0], days:r.message[1]}));
                        if(r.message[0].length){
                            d.show();
                        }
                        }
                    })
                }
            }
        })    
    }
 })
 

frappe.ui.form.on("Sales Order",{
    set_warehouse:function(frm,cdt,cdn){
        var data=locals[cdt][cdn]
        frappe.call({
            method:"sks.sks.custom.py.sales_order.subwarehouse",
            args:{sub_warehouse:data.set_warehouse,company:data.company},
            callback(r){
                if(frm.fields_dict["items"].grid.get_field('item_code')) {
                    frm.set_query("item_code", "items", function() {
                        return {
                            query: "erpnext.controllers.queries.item_query",
                            filters: {'item_code' : ["in", r["message"]],'is_sales_item': 1, 'customer': cur_frm.doc.customer}
                        }
                    })
                }
            }
        })
    }
})


frappe.ui.form.on("Sales Order",{
	after_save:function(frm,cdt,cdn){
        frappe.db.get_single_value("SKS Settings","reserved_stock").then(value =>{
            if(value==1){
                var status=cur_frm.doc.docstatus
                if(status==1){
                    var data=locals[cdt][cdn]
                    var item_codes=[]
                    var source_warehouse=[]
                    var required_qty=[]
                    var basic_rate=[]
                    for(var i=0;i<data.items.length;i++){
                        item_codes.push(data.items[i].item_code)
                        source_warehouse.push(data.items[i].warehouse)
                        required_qty.push(data.items[i].qty)
                        basic_rate.push(data.items[i].amount)
                    }
                    frappe.call({
                        method:"sks.sks.custom.py.sales_order.reserved_stock_for_sales_order",
                        args:{item_codes,source_warehouse,required_qty,basic_rate}
                    })
                }
            }
        })
	}
})

var loop
frappe.ui.form.on("Sales Order",{
    onload:function(){
        loop=0
    }
})
frappe.ui.form.on("Sales Order",{
	after_save:function(frm,cdt,cdn){
        if(cur_frm.doc.docstatus!=1){
            if(loop==0){
                var data1 = locals[cdt][cdn]
                var customer = data1.customer
                frappe.call({
                    method:"sks.sks.custom.py.sales_order.customer_credit_sale",
                    args:{customer},
                    callback : function(r){
                        if(r.message[2]>0){
                            var d = new frappe.ui.Dialog({
                                size: "extra large",
                                title:"Customer: "+ customer +"'s Outstanding Amount",
                                fields:[
                                    {'fieldname':'alert','fieldtype':'HTML','read_only':1,'bold':1},
                                    {'label':'Outstanding Amount','fieldname':'outstanding','fieldtype':'Currency','default':r.message[2],'read_only':1},
                                ],
                                primary_action : function(data){
                                    loop=loop+1
                                    frm.set_value("outstanding_amount",data.outstanding)
                                    var data1 = locals[cdt][cdn]
                                    var over_all_total = data1.outstanding_amount+data1.total
                                    cur_frm.set_value("outstanding_amount_and_total",over_all_total)
                                    d.hide();

                                }
                            })
                            var template=r.message[3]
                            d.set_df_property("alert","options",frappe.render(template,{}))
                            d.show();
                        }
                    }  
                })
            }
        }
        if(loop==0){
            loop=loop+1
            var data1 = locals[cdt][cdn]
            var over_all_total = data1.outstanding_amount+data1.total
            cur_frm.set_value("outstanding_amount_and_total",over_all_total)
        }
    }
})