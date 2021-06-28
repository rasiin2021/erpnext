from __future__ import unicode_literals

import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields
from frappe.custom.doctype.property_setter.property_setter import make_property_setter

def after_install():
	make_custom_roles()
	make_custom_fields()
	make_property_setters()

def make_custom_roles():
	for role_name in ['Accounting Manager']:
		role = frappe.new_doc('Role')
		role.update({
			'role_name': role_name,
			'desk_access': 1
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
	'Sales Invoice': {
		'customer_group': 'customer_name',
		'payments': 'total_qty'
	},
	'Customer': {
		'customer_group': 'address_html'
	}
}

property_setters = (
	("Patient", "phone", "hidden", 0),
)

custom_fields = {
	'Selling Settings': [
		{
			'fieldname': 'discount_levels_section',
			'fieldtype': 'Section Break',
			'label': 'Discount Levels',
			'insert_after': 'hide_tax_id',
		},
		{
			'fieldname': 'discount_levels',
			'fieldtype': 'Table',
			'options': 'Discount Level',
			'insert_after': 'hide'
		}
	],
}
