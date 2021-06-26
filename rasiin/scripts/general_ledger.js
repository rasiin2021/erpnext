frappe.query_reports["General Ledger"]["filters"].forEach((filter) => {
	if (filter.fieldname == "party_name") filter.hidden = 0;
});
