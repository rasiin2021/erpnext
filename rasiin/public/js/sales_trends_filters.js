// Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
// License: GNU General Public License v3. See license.txt

Object.defineProperty(erpnext, "get_sales_trends_filters", {
  value: function () {
    return [
      {
        fieldname: "period",
        label: __("Period"),
        fieldtype: "Select",
        options: [
          { value: "Monthly", label: __("Monthly") },
          { value: "Quarterly", label: __("Quarterly") },
          { value: "Half-Yearly", label: __("Half-Yearly") },
          { value: "Yearly", label: __("Yearly") },
        ],
        default: "Monthly",
      },
      {
        fieldname: "based_on",
        label: __("Based On"),
        fieldtype: "Select",
        options: [
          { value: "Item", label: __("Item") },
          { value: "Item Group", label: __("Item Group") },
          { value: "Customer", label: __("Customer") },
          { value: "Customer Group", label: __("Customer Group") },
          { value: "Territory", label: __("Territory") },
          { value: "Project", label: __("Project") },
        ],
        default: "Item",
      },
      {
        fieldname: "group_by",
        label: __("Group By"),
        fieldtype: "Select",
        options: [
          "",
          { value: "Item", label: __("Item") },
          { value: "Customer", label: __("Customer") },
        ],
        default: "",
      },
      {
        fieldname: "from_date",
        label: __("From Date"),
        fieldtype: "Date",
        default: frappe.datetime.add_months(frappe.datetime.get_today(), -1),
        reqd: 1,
        width: "60px",
      },
      {
        fieldname: "to_date",
        label: __("To Date"),
        fieldtype: "Date",
        default: frappe.datetime.get_today(),
        reqd: 1,
        width: "60px",
      },
      {
        fieldname: "fiscal_year",
        label: __("Fiscal Year"),
        fieldtype: "Link",
        options: "Fiscal Year",
        default: frappe.sys_defaults.fiscal_year,
      },
      {
        fieldname: "company",
        label: __("Company"),
        fieldtype: "Link",
        options: "Company",
        default: frappe.defaults.get_user_default("Company"),
      },
    ];
  },
  enumerable: true, // will show in Object.keys and for..in loop
  configurable: false, // can't be deleted
  writable: false, // can't be redefined
});
