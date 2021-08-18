const settings = frappe.listview_settings['Sales Invoice'];

settings.has_indicator_for_draft = true;
settings.add_fields.push('workflow_state');
settings.get_indicator = function (doc) {
	const status_color = {
		"Draft": "red",
		"Discount Approval Pending": "yellow",
		"Discount Rejected": "red",
		"Approved": "green",
		"Unpaid": "orange",
		"Paid": "green",
		"Return": "gray",
		"Credit Note Issued": "gray",
		"Unpaid and Discounted": "orange",
		"Overdue and Discounted": "red",
		"Overdue": "red",
		"Internal Transfer": "darkgrey"
	};
	if (doc.docstatus === 0) {
		return [__(doc.workflow_state), status_color[doc.workflow_state], "status,=," + doc.workflow_state];
	}
	return [__(doc.status), status_color[doc.status], "status,=," + doc.status];
};