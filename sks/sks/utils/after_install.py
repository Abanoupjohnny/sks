from sks.sks.utils.buying.purchase_order.purchase_order_custom_fields import purchase_order_customization
from sks.sks.utils.buying.purchase_receipt.purchase_receipt_custom import purchase_receipt_customization
from sks.sks.utils.buying.purchase_invoice.purchase_invoice_custom_fields import purchase_invoice_customization          
from sks.sks.utils.selling.delivery_note.delivery_note_custom_fields import delivery_note_customization
from sks.sks.utils.selling.sales_order.sales_order_custom_fields import sales_order_customization
from sks.sks.utils.stock.item.item_custom_fields import item_customization
def after_install():
    delivery_note_customization()
    sales_order_customization()
    item_customization()
    purchase_invoice_customization()
    purchase_receipt_customization()


