import frappe

def validate_amounts(doc, method):
	if doc.payable_amount > doc.practitioner_charge:
		frappe.throw('Payable Amount cannot be greater than Practitioner Charger')

	if doc.paid_amount > doc.payable_amount or doc.paid_amount > doc.practitioner_charge:
		frappe.throw('Amount Paid cannot be greater than Payable Amount')

