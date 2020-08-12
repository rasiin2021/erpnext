from __future__ import unicode_literals

import frappe

def after_install():
		make_custom_roles()

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
