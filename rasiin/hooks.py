# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from . import __version__ as app_version

app_name = "rasiin"
app_title = "Rasiin"
app_publisher = "Resilient Tech"
app_description = "Customisations to Frappe / ERPNext for Rasiin"
app_icon = "octicon octicon-file-directory"
app_color = "grey"
app_email = "sagar@resilient.tech"
app_license = "MIT"
after_install = "rasiin.install.after_install"

app_include_js = "/assets/js/rasiin.min.js"

doctype_js = {
	"Sales Invoice": "scripts/sales_invoice.js",
	"Material Request": "scripts/material_request.js",
	"Lab Test": "scripts/lab_test.js"
}

doctype_list_js = {
	"Issue": "scripts/issue_list.js",
	"Patient Appointment": "scripts/patient_appointment_list.js"
}

doc_events = {
	"Sales Invoice": {
		"validate": "rasiin.api.sales_invoice.validate_discount_level"
	}
}

override_doctype_class = {
	"Patient Appointment": "rasiin.override.patient_appointment.CustomPatientAppointment",
}

override_doctype_dashboards = {
	"Patient": "rasiin.api.patient_appointment.get_data",
	"Patient Appointment": "rasiin.api.patient_appointment_dashboard.get_data",
}
override_whitelisted_methods = {
	"frappe.desk.query_report.get_script.": (
		"rasiin.override.query_report.get_script"
	),
}
