frappe.ui.form.on("Patient Appointment", {
    setup(frm) {
        frm.events.set_payment_details = (frm) => {
            frappe.call({
                method: 'erpnext.healthcare.utils.get_service_item_and_practitioner_charge',
                args: {
                    doc: frm.doc
                },
                callback: function(r) {
                    if (!r.message || !r.message.practitioner_charge) return

                    frm.set_value({
                        'practitioner_charge': r.message.practitioner_charge,
                        'payable_amount': r.message.practitioner_charge,
                        'billing_item': r.message.service_item,
                    });
                }
            });
        }
    },
    refresh(frm) {
        if (!frm.is_new()) return;

        frm.page.set_primary_action(__('Check Availability'), function() {
            if (!frm.doc.patient) {
                frappe.msgprint({
                    title: __('Not Allowed'),
                    message: __('Please select Patient first'),
                    indicator: 'red'
                });
            } else {
                frappe.call({
                    method: 'erpnext.healthcare.doctype.patient_appointment.patient_appointment.check_payment_fields_reqd',
                    args: {'patient': frm.doc.patient},
                    callback: function(data) {
                        if (data.message == true) {
                            if (frm.doc.mode_of_payment && frm.doc.paid_amount !== undefined) {
                                check_and_set_availability(frm);
                            }
                            if (!frm.doc.mode_of_payment) {
                                frappe.msgprint({
                                    title: __('Not Allowed'),
                                    message: __('Please select a Mode of Payment first'),
                                    indicator: 'red'
                                });
                            }
                            if (frm.doc.paid_amount === undefined) {
                                frappe.msgprint({
                                    title: __('Not Allowed'),
                                    message: __('Please set the Paid Amount first'),
                                    indicator: 'red'
                                });
                            }
                        } else {
                            check_and_set_availability(frm);
                        }
                    }
                });
            }
        });
    },
    practitioner_charge(frm) {
        calculate_discount(frm, 'practitioner_charge')
    },
    discount_amount(frm) {
        if( frm.doc.discount_amount > frm.doc.practitioner_charge)
            frappe.throw('Discount Amount cannot be greater than Practitioner Charge')
        if( frm.doc.discount_amount < 0)
            frappe.throw('Discount Amount cannot be less than zero')

        calculate_discount(frm, 'discount_amount')
    },
    discount_percentage(frm) {
        if( frm.doc.discount_percentage < 0 || frm.doc.discount_percentage > 100)
            frappe.throw('Discount Percentage should be between 0 and 100')

        calculate_discount(frm, 'discount_percentage')
    },
    paid_amount(frm) {
        if( frm.doc.paid_amount > frm.doc.payable_amount)
            frappe.throw('Amount Paid cannot be greater than Payable Amount')
    }
});

function calculate_discount(frm, field) {
    let payable_amount, discount_percentage, discount_amount = 0

    if(frm.doc.practitioner_charge) {
        if(field == 'practitioner_charge') {
            if(!frm.doc.discount_percentage) {
                payable_amount = frm.doc.practitioner_charge;
            }
            else {
                discount_amount = flt(frm.doc.practitioner_charge * (frm.doc.discount_percentage / 100), 2);
                payable_amount = frm.doc.practitioner_charge - discount_amount;
            }
            discount_percentage = flt(frm.doc.discount_percentage, 4)
        }

        if(field == 'discount_amount') {
            discount_amount = frm.doc.discount_amount
            discount_percentage = flt(frm.doc.discount_amount * 100 / frm.doc.practitioner_charge, 4)
            payable_amount = frm.doc.practitioner_charge - frm.doc.discount_amount;
        }

        if(field == 'discount_percentage') {
            discount_percentage = frm.doc.discount_percentage
            discount_amount = flt(frm.doc.practitioner_charge * (frm.doc.discount_percentage / 100), 2);
            payable_amount = frm.doc.practitioner_charge - discount_amount;
        }
    }
    Object.assign(frm.doc, {
        paid_amount: payable_amount,
        payable_amount,
        discount_percentage,
        discount_amount,
    });
    frm.refresh_fields('payable_amount', 'discount_percentage', 'discount_amount', 'paid_amount');
}
