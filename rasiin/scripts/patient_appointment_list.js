/*
(c) ESS 2015-16
*/
frappe.listview_settings['Patient Appointment'] = {
	onload: function(listview) {
		this.add_button("Re-Visit" , "default" , function() {
		frappe.route_options = {
			"state" : ["=", "fallow"],
			"appointment_date" : ["=", frappe.datetime.nowdate()]
		};
		frappe.set_route("List" , "Patient Appointment");

	}
)
},
	add_button(name , type , action, wrapper_class = ".page-actions") {
	const button = document.createElement("button");
	button.classList.add("btn" , "btn-" + type , "btn-sm" , "ml-2");
	button.innerHTML = name;
	button.onclick = action;
	document.querySelector(wrapper_class).prepend(button);
	},
};
