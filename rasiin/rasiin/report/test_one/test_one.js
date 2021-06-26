// Copyright (c) 2016, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Test One"] = {
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
                "fieldname":"medical_department",
                "label": __("Medical Department"),
                "fieldtype": "link",	
                "reqd": 1,
                "width": "60px"
            }	
        ]
}

