from __future__ import unicode_literals

import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields


def after_install():
	make_custom_roles()
	make_custom_fields()

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
