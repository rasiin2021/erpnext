import os
import frappe
from frappe.desk import query_report

REPORT_NAME_MAP = {
	"Profit And Loss Statement": "rasiin/scripts/profit_and_loss_statement.js",
	"General Ledger": "rasiin/scripts/general_ledger.js",
}

old_get_script = query_report.get_script

@frappe.whitelist()
def get_script(report_name):
	result = old_get_script(report_name)
	if not report_name in REPORT_NAME_MAP:
		return result

	with open(REPORT_NAME_MAP[report_name], "r") as f:
		custom_script = f.read()

	result['script'] += custom_script
	return result

