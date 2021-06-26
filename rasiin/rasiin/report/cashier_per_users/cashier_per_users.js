// Copyright (c) 2016, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt
/* eslint-disable */
frappe.query_reports["Cashier_per_Users"] = {
        "filters": [
            {
                "fieldname":"from_date",
                "label": __("From Date"),
                "fieldtype": "Date",
                "default": frappe.datetime.get_today(),
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
            }  
        ]

        };

                                       
