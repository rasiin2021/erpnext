import frappe
from frappe import _
from frappe.utils import getdate
from erpnext.healthcare.doctype.patient_appointment.patient_appointment import get_receivable_account, get_appointment_item
from erpnext.healthcare.doctype.patient_appointment import patient_appointment

def create_sales_invoice(appointment_doc):
	sales_invoice = frappe.new_doc('Sales Invoice')
	sales_invoice.patient = appointment_doc.patient
	sales_invoice.customer = frappe.get_value('Patient', appointment_doc.patient, 'customer')
	sales_invoice.appointment = appointment_doc.name
	sales_invoice.due_date = getdate()
	sales_invoice.company = appointment_doc.company
	sales_invoice.debit_to = get_receivable_account(appointment_doc.company)

	sales_invoice.remarks = appointment_doc.notes
	sales_invoice.branch = appointment_doc.branch
	sales_invoice.medical_department = appointment_doc.department
	sales_invoice.apply_discount_on = "Grand Total"
	sales_invoice.discount_amount = appointment_doc.discount_amount


	item = sales_invoice.append('items', {})
	item = get_appointment_item(appointment_doc, item)
	item.rate = appointment_doc.practitioner_charge

	# Add payments if payment details are supplied else proceed to create invoice as Unpaid
	if appointment_doc.mode_of_payment and appointment_doc.paid_amount:
		sales_invoice.is_pos = 1
		payment = sales_invoice.append('payments', {})
		payment.mode_of_payment = appointment_doc.mode_of_payment
		payment.amount = appointment_doc.paid_amount

	sales_invoice.set_missing_values(for_validate=True)
	sales_invoice.flags.ignore_mandatory = True
	sales_invoice.save(ignore_permissions=True)
	sales_invoice.submit()
	frappe.msgprint(_('Sales Invoice {0} created').format(sales_invoice.name), alert=True)
	frappe.db.set_value('Patient Appointment', appointment_doc.name, {
		'invoiced': 1,
		'ref_sales_invoice': sales_invoice.name
	})

patient_appointment.create_sales_invoice = create_sales_invoice
