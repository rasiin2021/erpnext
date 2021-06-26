// Copyright (c) 2020, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

//frappe.ui.form.on('Share Test', {
	// refresh: function(frm) {
	frappe.ui.form.on("Share Test", "title", function(frm,cdt,cdn) {
	d = locals[cdt][cdn]
        frm.doc.share_balance = d.haraa
});
	}
})
