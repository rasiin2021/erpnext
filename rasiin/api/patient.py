import frappe
from erpnext.stock.get_item_details import get_pos_profile
from erpnext.accounts.doctype.sales_invoice.sales_invoice import (
    set_account_for_mode_of_payment,
)


def invoice_registration(doc, method=None):
    invoice_info = doc.invoice_patient_registration()
    invoice = frappe.get_doc("Sales Invoice", invoice_info["invoice"])
    invoice.patient = doc.name

    fee_item = invoice.items[0]
    fee_item.item_name = fee_item.description = "Registration Fee"

    if doc.collect_registration_fee:
        invoice.is_pos = True
        invoice.append(
            "payments",
            {"mode_of_payment": doc.mode_of_payment, "amount": invoice.grand_total},
        )
        invoice.set_missing_values()
        invoice.update_stock = 0
        set_account_for_mode_of_payment(invoice)

    invoice.flags.ignore_permissions = True
    invoice.submit()


@frappe.whitelist()
def get_mode_of_payment():
    company = frappe.defaults.get_user_default("company") or frappe.db.get_single_value(
        "Global Defaults", "default_company"
    )

    if not company:
        return

    pos_profile = get_pos_profile(company)
    if not pos_profile:
        return

    pos_profile = frappe.get_doc("POS Profile", pos_profile.get("name"))
    if not pos_profile.payments:
        return

    for payment in pos_profile.payments:
        if payment.default:
            return payment.mode_of_payment
    else:
        return pos_profile.payments[0].mode_of_payment
