import frappe
from erpnext.stock.doctype import material_request_item


def on_doctype_update():
	frappe.db.add_index(
		"Material Request Item", ["item_code", "warehouse", "medical_department"]
	)

material_request_item.on_doctype_update = on_doctype_update
