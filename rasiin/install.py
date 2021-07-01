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
	("Lab Test", "result_date", "allow_on_submit", 1),
	("Normal Test Result", "result_value", "allow_on_submit", 1),
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
	("Healthcare Service Unit", None, "track_seen", 1),
	("Healthcare Service Unit", None, "track_views", 1),
	("Healthcare Service Unit Type", None, "track_changes", 1),
	("Healthcare Service Unit Type", None, "track_seen", 1),
	("Healthcare Service Unit Type", None, "track_views", 1),
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
	"Patient Encounter": [
		{
			"fieldname": "symptoms_txt",
			"fieldtype": "Small Text",
			"label": "Symptoms",
			"insert_after": "symptoms",
			"hidden": 1,
		},
		{
			"fieldname": "diagnosis_txt",
			"fieldtype": "Small Text",
			"label": "Diagnosis",
			"insert_after": "diagnosis",
			"hidden": 1,
		}
	],
	"Drug Prescription": [
		{
			"fieldname": "medical_department",
			"fieldtype": "Link",
			"label": "Department",
			"options": "Medical Department",
			"insert_after": "dosage_form",
		},
		{
			"fetch_from": "drug_code.description",
			"fieldname": "dosage_test",
			"fieldtype": "Data",
			"label": "Dosage Test",
			"insert_after": "medical_department",
		}
	],
	"Healthcare Practitioner": [
		{
			"fieldname": "abbr",
			"fieldtype": "Data",
			"label": "Abbr",
		},
	],
	"Healthcare Settings": [
		{
			"default": "0",
			"fieldname": "new_born",
			"fieldtype": "Check",
			"label": "Newborn"
		},
		{
			"default": "Asc, Hooyo {{doc.patient_name}}, isbitaalka waxa uu kugu hambalyaynayaa {{doc.gender}} kuugu dhashay taariikhda: {{doc.baby_birth_date}}\nBaaraka Allah.",
			"depends_on": "new_born",
			"fieldname": "new_born_msg",
			"fieldtype": "Small Text",
			"label": "Newborn Message",
			"insert_after": "new_born",
		},
		{
			"default": "0",
			"fieldname": "vaccine",
			"fieldtype": "Check",
			"label": "Vaccine",
			"insert_after": "new_born_msg",
		},
		{
			"default": "Asc,  {{doc.patient_name}}, Waxaa lagaaray xiligi talaalka:{{doc.douse_one_date}}  {{doc.douse_two_date}} {{doc.douse_three_date}} ee isbitaalka Somali Sudanese Specialized hospital.",
			"depends_on": "vaccine",
			"fieldname": "vaccine_msg",
			"fieldtype": "Small Text",
			"label": "Vaccine Message",
			"insert_after": "vaccine",
		},
		{
			"default": "0",
			"fieldname": "nigh_shift_manager",
			"fieldtype": "Check",
			"label": "Nigh Shift Manager",
			"insert_after": "vaccine_msg",
		},
		{
			"default": "Asc, {{doc.patient_name}},Cawada waxad ku qorantahay Night shift sidaa lasoco, Mahadsanid.",
			"depends_on": "nigh_shift_manager",
			"fieldname": "nigh_shift_manager_message",
			"fieldtype": "Small Text",
			"label": "Nigh Shift Manager Message",
			"insert_after": "nigh_shift_manager",
		}
	],
	"Lab Prescription": [
		{
			"fetch_from": "department.visit_department",
			"fieldname": "medical_department",
			"fieldtype": "Link",
			"label": "Department",
			"options": "Medical Department",
			"insert_after": "lab_test_name",
		}
	],
}
