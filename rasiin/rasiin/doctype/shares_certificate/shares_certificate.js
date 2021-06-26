// Copyright (c) 2020, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt
// -*- coding: utf-8 -*-
// Copyright (c) 2017, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt
/* eslint-disable */

// Copyright (c) 2020, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

frappe.ui.form.on("Shares Certificate", "title", function(frm) {
        if(frm.doc.title){
                frappe.call({
                        "method": "frappe.get_doc('Shareholder', shareholder).share_balance",
                        args: {
                                doctype: "Shareholder",
                                name: frm.doc.title
                        },
                        callback: function (data) {
                                frappe.model.set_value(frm.doctype,frm.docname, "balance",data.message.share_balance);
                                console.log("share_balance");
                        }
                });
        }
});

~                                                                                                                                                                        
~                                                                                                                                                                                            
~                                                                                                                                                                        
~                            

