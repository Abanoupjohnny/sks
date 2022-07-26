from warnings import filters
import frappe
@frappe.whitelist()
def item_check_with_sales_order(item_code_checking=None,checking_sales_order=None,search_value=None):
	matched_item=0
	item_code_from_sales_order=frappe.get_doc("Sales Order",checking_sales_order)
	total_item=item_code_from_sales_order.__dict__["items"]
	len_items=len(total_item)
	item_batch_name=[]
	item_batch_mrp=[]
	if(item_code_checking != None):
		for j in range(0,len_items,1):
			if(item_code_checking == total_item[j].__dict__["item_code"]):
				item_code=total_item[j].__dict__["item_code"]
				matched_item=matched_item+1
				if search_value:
					ts_item_barcode=frappe.get_all("Batch",{"item":item_code_checking,"disabled":0,"barcode":search_value},["name","ts_mrp"])
					if ts_item_barcode:
						if len(ts_item_barcode)==1:
							item_batch_name.append(ts_item_barcode[0]["name"])
							item_batch_mrp=[]
						else:
							for batch in ts_item_barcode:
								item_batch_name.append(batch["name"])
								item_batch_mrp.append(batch["ts_mrp"])
				break
	if(matched_item==1):
		matched_item=0
		return item_code,item_batch_name,item_batch_mrp
	else:
		return 0

@frappe.whitelist()
def mandatory_validation(doc,event):
	ts_value=frappe.db.get_single_value("Thirvu Retail Settings","allow_only_if_delivery_note_items_match_with_sales_order_items")
	if ts_value==1:
		ts_item_barcodes=""
		for item in doc.items:
			if item.against_sales_order:
				if item.item_verified == 0:
					ts_item_details=frappe.get_doc("Item",item.item_code)
					if ts_item_details.barcodes:
						ts_item_barcodes += "•"+item.item_code+'<br>'
		if ts_item_barcodes:
			frappe.throw(_("Below Items Are Not Verified, Please Check It... <br>{0}").format(ts_item_barcodes))

@frappe.whitelist()
def item_warehouse_fetching(item_code,company):
    itemname =  frappe.get_doc("Item",item_code)

    warehouse = frappe.db.get_value("Item Warehouse" ,{'company':company},'storebin')
    return warehouse

def warehouse_fetcing(doc,event):
    item = doc.items
    for i in item:
        i.warehouse = i.ts_warehouse


