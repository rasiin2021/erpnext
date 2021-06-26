import frappe
from erpnext.healthcare.doctype.patient_appointment import patient_appointment

old_create_sales_invoice = patient_appointment.create_sales_invoice


def create_sales_invoice(appointment_doc):
	old_create_sales_invoice(appointment_doc)
	sales_invoice = frappe.db.get_value(
		"Sales Invoice", {"appointment": appointment_doc.name}
	)

	frappe.db.set_value(
		"Sales Invoice",
		sales_invoice,
		{
			"remarks": appointment_doc.notes,
			"branch": appointment_doc.branch,
			"medical_department": appointment_doc.department,
		},
	)


patient_appointment.create_sales_invoice = create_sales_invoice
