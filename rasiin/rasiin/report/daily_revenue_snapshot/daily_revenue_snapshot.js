// Copyright (c) 2016, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Daily Revenue Snapshot"] = {
	"filters": [
            {
                "fieldname":"company",
                "label": __("Company"),
                "fieldtype": "Link",
                "options": "Company",
                "default": frappe.defaults.get_user_default("company")
            },
            {
                "fieldname":"from_date",
                "label": __("From Date"),
                "fieldtype": "Date",
                "default": frappe.datetime.add_months(frappe.datetime.get_today(), -1),
                "reqd": 1,
                "width": "60px"
            },
            {
                "fieldname":"to_date",
                "label": __("To Date"),
                "fieldtype": "Date",
                "default": frappe.datetime.get_today(),
                "reqd": 1,
                "width": "60px"
            },
            {
                "fieldname":"department",
                "label": __("Medical Department"),
                "fieldtype": "Link",
                "options": "Medical Department"
            }

        ]
}

erpnext.dimension_filters.forEach((dimension) => {
        frappe.query_reports["General Ledger"].filters.splice(15, 0 ,{
                "fieldname": dimension["fieldname"],
                "label": __(dimension["label"]),
                "fieldtype": "Link",
                "options": dimension["document_type"]
        });
});
