import frappe
@frappe.whitelist()
def item_check_with_sales_order(item_code_checking=None,checking_sales_invoice=None):
	matched_item=0
	item_code_from_sales_order=frappe.get_doc("Sales Order",checking_sales_invoice)
	total_item=item_code_from_sales_order.__dict__["items"]
	len_items=len(total_item)
	if(item_code_checking != None):
		for j in range(0,len_items,1):
			if(item_code_checking == total_item[j].__dict__["item_code"]):
				item_code=total_item[j].__dict__["item_code"]
				matched_item=matched_item+1
				break
	if(matched_item==1):
		matched_item=0
		return item_code
	else:
		return 0



@frappe.whitelist(allow_guest=True)
def payment_entry(amount,mode,customer,pending_invoice,company,ref_no=None,ref_date=None):
    mode_of_payment = frappe.get_doc("Mode of Payment",mode).accounts
    for i in mode_of_payment:
        if(i.company==company):
            acc_paid_to=i.default_account
            break
    try:
        if(acc_paid_to):pass
    except:
        frappe.throw(("Please set Company and Default account for ({0}) mode of payment").format(mode))
    bank_account_type = frappe.db.get_value("Account", acc_paid_to, "account_type")
    if bank_account_type == "Bank":
        if(ref_no == None or ref_date == None):
            frappe.throw("Reference No and Reference Date is mandatory for Bank transaction")
    acc_currency = frappe.db.get_value('Account',acc_paid_to,'account_currency')
    pending_invoice = eval(pending_invoice)
    doc = frappe.new_doc('Payment Entry')
    references=[]
    amount1 = float(amount)
    for i in pending_invoice:
        amount_allocated = 0
        if(amount1 >= pending_invoice[i]):
            amount_allocated = pending_invoice[i]
            amount1 -= pending_invoice[i]
        else:
            amount_allocated=amount1
            amount1 -= amount_allocated
        if(amount_allocated>0):
            references.append({
                'reference_doctype':'Sales Invoice',
                'reference_name': i,
                'total_amount':pending_invoice[i],
                'exchange_rate': 1,
                'allocated_amount': amount_allocated
            })
    doc.update({
        'company':company,
        'payment_type':"Receive",
        'docstatus': 1,
        'mode_of_payment':mode,
        'party_type': 'Customer',
        'party': customer,
        'paid_amount':float(amount),
        'source_exchange_rate':1,
        'references':references,
        'received_amount':float(amount),
        'target_exchange_rate':1,
        'paid_to': acc_paid_to,
        'paid_to_account_currency': acc_currency,
    })
    if(bank_account_type == 'Bank'):
        doc.update({
            'reference_no':ref_no,
            'reference_date':ref_date
        })
    doc.insert()
    doc.submit()
    frappe.db.commit()
    return doc.paid_amount,mode


def feed_back_form(doc, action): 
    si=frappe.get_all('Customer Feedback Form', 
		    filters={'customer_name': doc.customer},
		    fields=['name'])
    
    compliants_dict={}
    print(frappe.get_meta("Customer Feedback Form").fields[0].__dict__)
    for i in frappe.get_meta("Customer Feedback Form").fields:
        compliants_dict[i.fieldname]=i.label
    
    if si:
        cff=frappe.get_doc("Customer Feedback Form", si[0]['name'])
        compliants_list=[]
        feedback1=cff.invoice_no
        feedback2=cff.customer_name
        feedback3=cff.ratings
        feedback4=cff.compliant1
        if(cff.compliant1==1):
            compliants_list.append("<li>"+compliants_dict['compliant1']+"</li>")
        
        if(cff.compliant2==1):
            compliants_list.append("<li>"+compliants_dict['compliant2']+"</li>")
        
        if(cff.compliant3==1):
            compliants_list.append("<li>"+compliants_dict['compliant3']+"</li>")
        
        if(cff.compliant4==1):
            compliants_list.append("<li>"+compliants_dict['compliant4']+"</li>")
        
        if(cff.compliant5==1):
            compliants_list.append("<li>"+compliants_dict['compliant5']+"</li>")
       
        if(cff.compliant6==1):
            compliants_list.append("<li>"+compliants_dict['compliant6']+"</li>")
        
        if(cff.compliant7==1):
            compliants_list.append("<li>"+compliants_dict['compliant7']+"</li>")
        
        if(cff.compliant8==1):
            compliants_list.append("<li>"+compliants_dict['compliant8']+"</li>")
        
        if(cff.compliant9==1):
            compliants_list.append("<li>"+compliants_dict['compliant9']+"</li>")
        
        if(cff.compliant10==1):
            compliants_list.append("<li>"+compliants_dict['compliant10']+"</li>")
        feedback5=cff.others
        if(cff.others_check==1):
            compliants_list.append("<p>"+feedback5+"</p>")
        frappe.msgprint('<b>Rating: </b> '+('⭐'*feedback3)+'<p><b>Feedback: </b> </p><ul>'+" ".join(compliants_list)+'</ul>')


            
            