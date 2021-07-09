import frappe


def invoice_registration(doc, method=None):
    invoice_info = doc.invoice_patient_registration()
    invoice = frappe.get_doc("Sales Invoice", invoice_info["invoice"])
    invoice.patient = doc.name

    fee_item = invoice.items[0]
    fee_item.item_name = fee_item.description = "Registration Fee"

    invoice.flags.ignore_permissions = True
    invoice.submit()
