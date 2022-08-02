import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields
from frappe.custom.doctype.property_setter.property_setter import make_property_setter

def stock_entry_details():
    stock_entry_details_custom_fields = {
        "Stock Entry Detail": [
                dict(fieldname='expire_dates', label='Expire Date', fieldtype='Date',insert_after='batch_no',depends_on = "eval:doc.t_warehouse"),
                dict(fieldname='valuation_rates', label='Valuation Rate', fieldtype='Currency',insert_after='expire_dates',fetch_from = 'batch_no.ts_valuation_rate'),
                dict(fieldname='selling_rates', label='Selling Rate', fieldtype='Currency',insert_after='valuation_rates',depends_on = "eval:doc.t_warehouse"),
                dict(fieldname='mrp_rates', label='Mrp', fieldtype='Currency',insert_after='selling_rates',fetch_from = 'item_code.mrp',depends_on = "eval:doc.t_warehouse"),
        ]}
    
    create_custom_fields(stock_entry_details_custom_fields)

def item_property_setter():                
    make_property_setter("Stock Entry Detail", "basic_rate", "fetch_from", "batch_no.ts_valuation_rate", "Small Text")
    make_property_setter("Stock Entry Detail", "basic_rate", "in_list_view", 0, "Check")
    make_property_setter("Stock Entry Detail", "batch_no", "in_list_view", 1, "Check")
    

    
    