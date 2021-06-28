from __future__ import unicode_literals

import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields
from frappe.custom.doctype.property_setter.property_setter import make_property_setter

def after_install():
	make_custom_roles()
	make_custom_fields()
	make_property_setters()

def make_custom_roles():
	for role_name in ["Accounting Manager"]:
		role = frappe.new_doc("Role")
		role.update({
			"role_name": role_name,
			"desk_access": 1
		})
		try:
			role.save()
		except frappe.DuplicateEntryError:
			pass

	frappe.db.commit()


def make_custom_fields():
	create_custom_fields(custom_fields)
	frappe.db.commit()

def make_property_setters():
	for doctype, fields in insert_after_map.items():
		for fieldname, previous_field in fields.items():
			make_property_setter(doctype, fieldname, "is_custom_field", 1, "")
			make_property_setter(doctype, fieldname, "insert_after", previous_field, "")

	for property_setter in property_setters:
		for_doctype = False
		if not fieldname:
			for_doctype = True

		make_property_setter(*property_setter, "", for_doctype=for_doctype)

	frappe.db.commit()

insert_after_map = {
	"Sales Invoice": {
		"customer_group": "customer_name",
		"payments": "total_qty",
	},
	"Customer": {
		"customer_group": "address_html",
	}
}

property_setters = (
	("Normal Test Result", "bold", "hidden", 1),
	("Normal Test Result", "italic", "hidden", 1),
	("Normal Test Result", "underline", "hidden", 1),
	("Patient", "phone", "hidden", 1),
	("Stock Entry", "purpose", "options", "Material Issue"),
	("Patient Appointment", "status", "read_only", 0),
	("Patient Encounter", "patient_age", "allow_in_quick_entry", 1),
	("Patient Encounter", "patient_age", "in_list_view", 1),
	("Patient Encounter", "patient_age", "in_global_search", 1),
	("Patient Encounter", "patient_age", "in_preview", 1),
	("Patient Encounter", "patient_age", "in_standard_filter", 1),
	("Patient Encounter", None, "track_views", 1),
	("Employee", None, "track_seen", 1),
	("Employee", None, "track_views", 1),
	("Material Request Item", "item_code", "columns", 0),
	("Material Request Item", "item_code", "print_width", ""),
	("Material Request Item", "item_code", "width", ""),
	("Material Request Item", "item_code", "search_index", 0),
	("Material Request Item", "item_name", "in_global_search", 0),
	("Material Request Item", "item_name", "print_hide", 0),
	("Material Request Item", "item_name", "print_width", ""),
	("Material Request Item", "item_name", "width", ""),
	("Material Request Item", "warehouse", "columns", 0),
	("Material Request Item", "warehouse", "print_width", ""),
	("Material Request Item", "warehouse", "width", ""),
	("Material Request Item", "schedule_date", "columns", 0),
	("Material Request Item", "schedule_date", "print_width", ""),
	("Material Request Item", "schedule_date", "width", ""),
	("Material Request Item", "rate", "print_hide", 1),
	("Material Request Item", "rate", "report_hide", 1),
	("Material Request Item", "amount", "print_hide", 1),
	("Material Request Item", "amount", "report_hide", 1),
	("Material Request Item", "expense_account", "print_hide", 1),
	("Vital Signs", "company", "hidden", 1),
	("Vital Signs", "appointment", "label", "Appointment"),
	("Vital Signs", "appointment", "report_hide", 1),
	("Vital Signs", "encounter", "report_hide", 1),
	("Vital Signs", None, "search_fields", "patient, patient_name, signs_date"),
	("Vital Signs", None, "show_preview_popup", 1),
	("Vital Signs", None, "track_views", 1),
	("Procedure Prescription", "procedure", "label", "Procedure"),
	("Procedure Prescription", "procedure", "reqd", 0),
	("Procedure Prescription", "procedure_name", "read_only", 1),
	("Procedure Prescription", "practitioner", "label", "Referral"),
	("Procedure Prescription", "practitioner", "ignore_user_permissions", 1),
	("Procedure Prescription", "comments", "in_list_view", 1),
)

custom_fields = {
	"Selling Settings": [
		{
			"fieldname": "discount_levels_section",
			"fieldtype": "Section Break",
			"label": "Discount Levels",
			"insert_after": "hide_tax_id",
		},
		{
			"fieldname": "discount_levels",
			"fieldtype": "Table",
			"options": "Discount Level",
			"insert_after": "hide",
		}
	],
	"Sales Invoice Item": [
		{
			"fieldname": "insurance_claim_coverage",
			"fieldtype": "Percent",
			"label": "Insurance Claim Coverage",
			"insert_after": "amount",
		},
		{
			"fieldname": "insurance_claim_amount",
			"fieldtype": "Currency",
			"label": "Insurance Claim Amount",
			"insert_after": "insurance_claim_coverage",
		},
		{
			"fieldname": "insurance_approval_number",
			"fieldtype": "Data",
			"label": "Insurance Approval Number",
			"insert_after": "insurance_claim_amount",
		},
		{
			"fieldname": "reference_dt",
			"fieldtype": "Link",
			"label": "Reference DocType",
			"options": "DocType",
			"insert_after": "edit_references",
		},
		{
			"fieldname": "reference_dn",
			"fieldtype": "Dynamic Link",
			"label": "Reference Name",
			"options": "reference_dt",
			"insert_after": "reference_dt",
		}
	],
	"Material Request": [
		{
			"fetch_if_empty": 1,
			"fieldname": "recommended_by",
			"fieldtype": "Link",
			"label": "Recommended By",
			"options": "Purchase Users",
			"insert_after": "requested_by",
		},
		{
			"fieldname": "column_break_15",
			"fieldtype": "Column Break",
			"insert_after": "recommended_by",
		},
	],
	"Material Request Item": [
		{
			"bold": 1,
			"columns": 4,
			"fieldname": "medical_department",
			"fieldtype": "Link",
			"in_list_view": 1,
			"in_preview": 1,
			"in_standard_filter": 1,
			"label": "Medical Department",
			"options": "Medical Department",
			"print_width": "80px",
			"search_index": 1,
			"width": "80px",
			"insert_after": "accounting_dimensions_section",
		}
	],
	"Task Depends On": [
		{
			"fieldname": "color",
			"fieldtype": "Color",
			"label": "Color",
			"insert_after": "column_break_2",
		},
		{
			"fieldname": "exp_end_date",
			"fieldtype": "Date",
			"label": "Exp End Date",
			"read_only": 1,
			"insert_after": "color",
		},
		{
			"fieldname": "status",
			"fieldtype": "Select",
			"label": "Status",
			"options": "Open\nWorking\nPending Review\nOverdue\nCompleted\nCancelled",
			"read_only": 1,
			"insert_after": "exp_end_date",
		}
	],
	"Vital Signs": [
		{
			"fieldname": "rbg",
			"fieldtype": "Data",
			"label": "RBG",
			"insert_after": "abdomen",
		},
		{
			"fieldname": "spo2",
			"fieldtype": "Data",
			"label": "SPO2",
			"insert_after": "rbg",
		}
	],
	"Procedure Prescription": [
		{
			"fetch_from": "procedure.item_group",
			"fieldname": "item_group",
			"fieldtype": "Data",
			"label": "item group",
			"insert_after": "comments"
		}
	],
}
