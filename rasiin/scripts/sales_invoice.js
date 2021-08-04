frappe.ui.form.on("Sales Invoice", {
	write_off_percentage(frm) {
		frm.set_value('write_off_amount',
			flt(
				(flt(frm.doc.total) + flt(frm.doc.total_taxes_and_charges))
				* flt(frm.doc.write_off_percentage) / 100, 4
			)
		);
	},

	write_off_amount(frm) {
		const write_off_percentage = flt(
			flt(frm.doc.write_off_amount) /
			(flt(frm.doc.total) + flt(frm.doc.total_taxes_and_charges)), 4
		) * 100;

		validate_discount_level(frm, write_off_percentage);
		frm.doc.write_off_percentage = write_off_percentage;
		frm.refresh_field('write_off_percentage');
	},

	async paid_amount(frm) {
		if (frm.doc.is_return || !frm.doc.is_pos || frm.doc.docstatus) return;

		await frm.set_value("write_off_amount", 0);
		if (flt(frm.doc.paid_amount) <= flt(frm.doc.grand_total)) return;

		const payments_length = frm.doc.payments && frm.doc.payments.length;
		if (payments_length) {
			const sum = frm.doc.payments
				.slice(0, -1)
				.reduce((a, b) => a + (b.amount || 0), 0);
			if (sum <= frm.doc.grand_total) {
				const row = frm.doc.payments[payments_length - 1];
				frappe.model.set_value(
					row.doctype,
					row.name,
					"amount",
					flt(frm.doc.grand_total - sum)
				);
			} else {
				for (const row of frm.doc.payments) {
					row.amount = 0;
				}

				const first_row = frm.doc.payments[0];
				frappe.model.set_value(
					first_row.doctype,
					first_row.name,
					"amount",
					frm.doc.grand_total
				);
			}
		}

		frappe.validated = false;

		frappe.throw(
			`Paid amount <strong>
      (${format_currency(frm.doc.paid_amount, frm.doc.currency)})
      </strong> cannot be greater than Grand Total <strong>
      (${format_currency(frm.doc.grand_total, frm.doc.currency)})
      </strong>`
		);
	},

	validate(frm) {
		frm.trigger("paid_amount");
	},
});

function validate_discount_level(frm, write_off_percentage) {
	const discount_levels = frappe.boot.discount_levels;
	if (!discount_levels) return;

	for (const role of Object.keys(discount_levels).sort((a, b) => discount_levels[b] - discount_levels[a])) {
		if (!frappe.user.has_role(role)) continue;

		const discount_allowed = discount_levels[role];
		if (write_off_percentage > discount_allowed) {
			frm.set_value('write_off_percentage', discount_allowed);
			frappe.throw(
				`You are not permitted to give a discount greater than
					 ${discount_allowed}% of Grand Total Before Discount`
			)
		}
		break;
	}
}

// var get_healthcare_services_to_invoice = function(frm) {
// 	var me = this;
// 	let selected_patient = '';
// 	let selected_encounter = '';
// 	var dialog = new frappe.ui.Dialog({
// 		title: __("Get Items from Healthcare Services"),
// 		fields:[
// 			{
// 				fieldtype: 'Link',
// 				options: 'Patient',
// 				label: 'Patient',
// 				fieldname: "patient",
// 				reqd: true
// 			},
// 			{ fieldtype: 'Data', read_only:1, fieldname: 'patient_name', depends_on:'eval:doc.patient', label: 'Patient Name'},
// 			{ fieldtype: 'Column Break'},
// 		 	{ fieldtype: 'Link', options: 'Patient Encounter', label: 'Patient Encounter', fieldname: "encounter", reqd: true,
//                                 description:'',
//                                 get_query: function(doc) {
//                                         return {
//                                                 filters: {
//                                                         patient: dialog.get_value("patient"),
//                                                         docstatus: ["<", 2]

//                                                 }
//                                         };
//                                 }
//                         },
// 			{ fieldtype: 'Data', read_only:1, fieldname: 'encounter_id', depends_on:'eval:doc.encounter', label: 'Encounter Reference'},
// 			{ fieldtype: 'Column Break'},
//                         { fieldtype: 'Data', read_only:1, fieldname: 'practitioner_name', depends_on:'eval:doc.encounter', label: 'Practitioner Name'},
//                         { fieldtype: 'Data', read_only:1, fieldname: 'medical_department', depends_on:'eval:doc.encounter', label: 'Department'},
// 			{ fieldtype: 'Section Break'	},
// 			{ fieldtype: 'HTML', fieldname: 'results_area' }
// 		]
// 	});
// 	var $wrapper;
// 	var $results;
// 	var $placeholder;
// 	dialog.set_values({
// 		'patient': frm.doc.patient
// 	});

// 	dialog.fields_dict["encounter"].df.onchange = () => {
// 		const encounter = dialog.get_value('encounter');
// 		//Halkan waxan kudarnay Patient Encounter data
// 		frappe.db.get_value(
// 			"Patient Encounter",
// 			encounter,
// 			['healthcare_practitioner_name', 'visit_department', 'name'], function(r) {
// 				if(!r) return;
// 				dialog.set_values({
// 					'practitioner_name': r.healthcare_practitioner_name,
// 					'medical_department': r.visit_department,
// 					'encounter_id': r.name,
// 				});
// 			}
// 		);

// 		//Halkan waxan kudarnay Parameter dheerad Si Encounter ID Marki lagaliyo oo usoo baxo Dalabka Quseeyo oo kaliya
// 		var patient = dialog.fields_dict.patient.input.value;
// 		if(patient && encounter && encounter!=selected_encounter){
// 				selected_encounter = encounter;
// 				var method = "erpnext.healthcare.utils.get_healthcare_services_to_invoice";
// 				var args = {patient: patient ,encounter: encounter, company:frm.doc.company};
// 				var columns = {"item_code": "Service", "medical_department": "Department", "encounter_date": "post Date", "item_name": "Item Name", "reference_dn": "Reference Name", "reference_dt": "Reference Type"};
// 				get_healthcare_items(frm, true, $results, $placeholder, method, args, columns);
// 		} else if(!patient || !encounter){
// 			selected_patient = '';
// 			selected_encounter = '';
// 			$results.empty();
// 			$results.append($placeholder);
// 		}
// 	}

// 	dialog.fields_dict["patient"].df.onchange = () => {
// 			frappe.db.get_value("Patient", dialog.get_value('patient'), 'patient_name', function(r) {
// 					if(r && r.patient_name){
// 							dialog.set_values({
// 									'patient_name': r.patient_name
// 							});
// 					}
// 			});
// 	}

// 	$wrapper = dialog.fields_dict.results_area.$wrapper.append(`<div class="results"
// 		style="border: 1px solid #d1d8dd; border-radius: 3px; height: 300px; overflow: auto;"></div>`);

// 	$results = $wrapper.find('.results');
// 	$placeholder = $(`<div class="multiselect-empty-state">
// 				<span class="text-center" style="margin-top: -40px;">
// 					<i class="fa fa-2x fa-heartbeat text-extra-muted"></i>
// 					<p class="text-extra-muted">No billable Healthcare Services found</p>
// 				</span>
// 			</div>`);
// 	$results.on('click', '.list-item--head :checkbox', (e) => {
// 		$results.find('.list-item-container .list-row-check')
// 			.prop("checked", ($(e.target).is(':checked')));
// 	});
// 	set_primary_action(frm, dialog, $results, true);
// 	dialog.show();
// };
// var fields = [];
// var get_healthcare_items = function(frm, invoice_healthcare_services, $results, $placeholder, method, args, columns) {
// 	var me = this;
// 	$results.empty();
// 	frappe.call({
// 		method: method,
// 		args: args,
// 		callback: function(data) {
// 			if(data.message){
// 				$results.append(make_list_row(columns, invoice_healthcare_services));
// 				for(let i=0; i<data.message.length; i++){
// 					if (args["encounter"] == data.message[i].encounter){
// 						$results.append(make_list_row(columns, invoice_healthcare_services, data.message[i]));
// 					}
// 				}
// 			}else {
// 				$results.append($placeholder);
// 			}
// 		}
// 	});
// }

// var set_primary_action= function(frm, dialog, $results, invoice_healthcare_services) {
// 	var me = this;
// 	dialog.set_primary_action(__('Add'), function() {
// 		let checked_values = get_checked_values($results);
// 		if(checked_values.length > 0){
// 			// Additional Medical Department feild
// 			//if(invoice_healthcare_services) {
// 				frm.set_value("patient", dialog.fields_dict.patient.input.value);
// 				frm.set_value("medical_department", dialog.fields_dict.medical_department.value);
// 				frm.set_value("practitioner", dialog.fields_dict.practitioner_name.value);
// 				frm.set_value("encounter_reference_id", dialog.fields_dict.encounter_id.value);

// 			//}
// 			frm.set_value("items", []);
// 			add_to_item_line(frm, checked_values, invoice_healthcare_services);
// 			dialog.hide();
// 		}
// 		else{
// 			if(invoice_healthcare_services){
// 				frappe.msgprint(__("Please select Healthcare Service"));
// 			}
// 			else{
// 				frappe.msgprint(__("Please select Drug"));
// 			}
// 		}
// 	});
// };

// var get_drugs_to_invoice = function(frm) {
// 	var me = this;
// 	let selected_encounter = '';
// 	//One More additional feild Medical Department Line
// 	var dialog = new frappe.ui.Dialog({
// 		title: __("Get Items from Prescriptions"),
// 		fields:[
// 			{ fieldtype: 'Link', options: 'Patient', label: 'Patient', fieldname: "patient", reqd: true },
// 			{ fieldtype: 'Data', read_only:1, fieldname: 'patient_name', depends_on:'eval:doc.patient', label: 'Patient Name'},
// 			{ fieldtype: 'Column Break'},
// 			{ fieldtype: 'Link', options: 'Patient Encounter', label: 'Patient Encounter', fieldname: "encounter", reqd: true,
// 				description:'',
// 				get_query: function(doc) {
// 					return {
// 						filters: {
// 							patient: dialog.get_value("patient"),
// 							docstatus: ["<", 2]
// 						}
// 					};
// 				}
// 			},
// 			{ fieldtype: 'Data', read_only:1, fieldname: 'encounter_id', depends_on:'eval:doc.encounter', label: 'Encounter Reference'},
// 			{ fieldtype: 'Column Break'},
// 			{ fieldtype: 'Data', read_only:1, fieldname: 'practitioner_name', depends_on:'eval:doc.encounter', label: 'Practitioner Name'},
// 			{ fieldtype: 'Data', read_only:1, fieldname: 'medical_department', depends_on:'eval:doc.encounter', label: 'Department'},
// 			{ fieldtype: 'Section Break' },
// 			{ fieldtype: 'HTML', fieldname: 'results_area' }
// 		]
// 	});
// 	var $wrapper;
// 	var $results;
// 	var $placeholder;
// 	dialog.set_values({
// 		'patient': frm.doc.patient,
// 		'encounter': ""
// 	});
// 	dialog.fields_dict["encounter"].df.onchange = () => {
// 		frappe.db.get_value("Patient Encounter", dialog.get_value('encounter'), 'healthcare_practitioner_name', function(r) {
// 			if(r && r.healthcare_practitioner_name){
// 				console.log(r);
// 				dialog.set_values({
// 					'practitioner_name': r.healthcare_practitioner_name
// 				});
// 			}
// 		});

// 		 frappe.db.get_value("Patient Encounter", dialog.get_value('encounter'), 'visit_department', function(r) {
//                         if(r && r.visit_department){
//                                 console.log(r);
//                                 dialog.set_values({
//                                         'medical_department': r.visit_department
//                                 });
//                         }
//                 });

// 		 frappe.db.get_value("Patient Encounter", dialog.get_value('encounter'), 'name', function(r) {
// 											 if(r && r.name){
// 															 console.log(r);
// 															 dialog.set_values({
// 																			 'encounter_id': r.name
// 															 });
// 											 }
// 								});

// 		var encounter = dialog.fields_dict.encounter.input.value;
// 		if(encounter && encounter!=selected_encounter){
// 			selected_encounter = encounter;
// 			var method = "erpnext.healthcare.utils.get_drugs_to_invoice";
// 			var args = {encounter: encounter};
// 			var columns = {"item_code": "Drug Code", "item_name": "Item Name", "medical_department": "Department", "encounter_date": "Post Date", "qty": "quantity", "description": "description"};
// 			get_healthcare_items(frm, false, $results, $placeholder, method, args, columns);
// 		}
// 		else if(!encounter){
// 			selected_encounter = '';
// 			$results.empty();
// 			$results.append($placeholder);
// 		}
// 	}
// 	dialog.fields_dict["patient"].df.onchange = () => {
// 		frappe.db.get_value("Patient", dialog.get_value('patient'), 'patient_name', function(r) {
// 			if(r && r.patient_name){
// 				dialog.set_values({
// 					'patient_name': r.patient_name
// 				});
// 			}
// 		});
// 	}
// 	$wrapper = dialog.fields_dict.results_area.$wrapper.append(`<div class="results"
// 		style="border: 1px solid #d1d8dd; border-radius: 3px; height: 300px; overflow: auto;"></div>`);
// 	$results = $wrapper.find('.results');
// 	$placeholder = $(`<div class="multiselect-empty-state">
// 				<span class="text-center" style="margin-top: -40px;">
// 					<i class="fa fa-2x fa-heartbeat text-extra-muted"></i>
// 					<p class="text-extra-muted">No Drug Prescription found</p>
// 				</span>
// 			</div>`);
// 	$results.on('click', '.list-item--head :checkbox', (e) => {
// 		$results.find('.list-item-container .list-row-check')
// 			.prop("checked", ($(e.target).is(':checked')));
// 	});
// 	set_primary_action(frm, dialog, $results, false);
// 	dialog.show();
// };
