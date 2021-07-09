import frappe
from erpnext.healthcare.doctype.patient_appointment.patient_appointment import (
    check_payment_fields_reqd
)


def validate_amounts(doc, method):
    if doc.payable_amount > doc.practitioner_charge:
        frappe.throw("Payable Amount cannot be greater than Practitioner Charger")

    if (
        doc.paid_amount > doc.payable_amount
        or doc.paid_amount > doc.practitioner_charge
    ):
        frappe.throw("Amount Paid cannot be greater than Payable Amount")


@frappe.whitelist()
def custom_check_payment_fields_reqd(patient):
    result = check_payment_fields_reqd(patient)
    if not result and frappe.db.get_single_value(
        "Healthcare Settings", "automate_appointment_invoicing"
    ):
        return True

    return result
