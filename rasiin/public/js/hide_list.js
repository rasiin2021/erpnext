modifyMethod('frappe.views.BaseList', 'get_args', function(args) {
	if ( (this.doctype == 'Patient Appointment' && !frappe.user.has_role(['Physician', 'Accounting Manager']))
	|| (this.doctype == 'Sales Invoice' && !frappe.user.has_role(['Accounting Manager'])) ) {
		args.filters.push([this.doctype, 'name', '=', '']);
	}

	return args;
})