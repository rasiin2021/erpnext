frappe.ui.form.on('Patient Encounter', {
    async refresh(frm) {
    //       let status = "Active"
    // frm.set_query('practitioner', () => {
    //     return {
    //         query: "rasiin.api.practitioner_filter.practitioner_filter",
    //             filters: {
    //                         "status": status
    //                     }
    //             }
    // })

    if (!frm.is_new()) {
        // frm.doc.drug_prescription.forEach((el , index) => {
        //     console.log(el.invoiced)
        //     if(el.invoiced){ 
        //         frm.set_df_property("drug_prescription", "read_only", true);
        //         // let df = frappe.meta.get_docfield("Procedure Prescription","procedure", frm.doc.name);
        //         // df.read_only = 1;
        //     }
        // });

        // frm.doc.raidiolgy.forEach((el , index) => {
        //     console.log(el.invoiced)
        //     if(el.invoiced){ 
        //         frm.set_df_property("raidiolgy", "read_only", true);
        //         // let df = frappe.meta.get_docfield("Procedure Prescription","procedure", frm.doc.name);
        //         // df.read_only = 1;
        //     }
        // });

        frm.doc.lab_test_prescription.forEach((el , index) => {
            console.log("this test is " + el.invoiced)
            if(el.invoiced){ 
                frm.set_df_property("lab_test_prescription", "read_only", true);
                // let df = frappe.meta.get_docfield("Procedure Prescription","procedure", frm.doc.name);
                // df.read_only = 1;
            }
        });

        frm.doc.procedure_prescription.forEach((el , index) => {
            console.log(el.invoiced)
            if(el.invoiced){ 
                frm.set_df_property("procedure_prescription", "read_only", true);
                // let df = frappe.meta.get_docfield("Procedure Prescription","procedure", frm.doc.name);
                // df.read_only = 1;
            }
        });
        
    }
// on blur function
    // $(frm.fields_dict.patient.input).on('blur', function(e) {
    //     if(frm.doc.patient) {
    //         let patient = frm.doc.patient
    //         console.log(patient)
    //         frappe.call({
    //             method: "rasiin.api.patient_encounter.appointment_type",
    //             args: { "patient": patient}, //dotted path to server method
    //             callback: function(r) {
    //                 // console.log(r.message)
    //                 cur_frm.set_value("appointment", r.message);
    //             }
    //         })
    //     }

    // })
        
        
    // your code here
    // if(frm.doc.appointment){
    //     let appoinment = frm.doc.appointment;
    //     var docname = await frappe.db.get_doc("Patient Appointment", appoinment);
    //   //  console.log(docname)
    //     cur_frm.set_value("symptom", docname.symptoms);

    // }
},
symptoms_select: function(frm) {
       if(frm.doc.symptoms_select){
            var symptoms = null;
            var string = "";
            if(frm.doc.symptom)
                    symptoms = frm.doc.symptom + "\n" +frm.doc.symptoms_select;
            else
            symptoms = frm.doc.symptoms_select;

            string += symptoms;
            var array = string.split("\n");
            let new_array = [];
            array.forEach((sym, idx) => {
                if(new_array.includes(sym)){
                    // pass
                } else {
                    let new_sym = sym;
                    new_array.push(new_sym);
                    // console.log(new_array.join("\n"))
                    frappe.model.set_value(frm.doctype,frm.docname, "symptom", new_array.join("\n"));
                }
                    
            });
            frappe.model.set_value(frm.doctype,frm.docname, "symptoms_select", null);
            $(frm.fields_dict.symptoms_select.input).blur();
    }
    
},

diagnosis_select:function(frm) {
       
         if(frm.doc.diagnosis_select){
            var diagnosis = null;
            var string = "";

            if(frm.doc.diagnos)
                    diagnosis = frm.doc.diagnos + "\n" +frm.doc.diagnosis_select;
            else
                    diagnosis = frm.doc.diagnosis_select;

                    string += diagnosis;
                    var array = string.split("\n");
                    let new_array = [];
                    array.forEach((sym, idx) => {
                        if(new_array.includes(sym)){
                            // pass
                        } else {
                            let new_sym = sym;
                            new_array.push(new_sym);
                            // console.log(new_array.join("\n"))
                            frappe.model.set_value(frm.doctype,frm.docname, "diagnos", new_array.join("\n"));
                        }
                            
                    });
            frappe.model.set_value(frm.doctype,frm.docname, "diagnosis_select", null);
            $(frm.fields_dict.diagnosis_select.input).blur();
    }
},


// Still to be tested
patient: frm => {
    // if(frm.doc.patient) {
    //     let patient = frm.doc.patient
    //     console.log(patient)
    //     frappe.call({
    //         method: "rasiin.api.patient_encounter.appointment_type",
    //         args: { "patient": patient}, //dotted path to server method
    //         callback: function(r) {
    //             // console.log(r.message)
    //             cur_frm.set_value("appointment", r.message);
    //         }
    //     })
    // }
},

setup: frm => {

    frm.sub_item_readonly = frm => {
        frm.doc.procedure_prescription.forEach((el , index) => {
            console.log(el.sub_item)
            if(el.sub_item){
                let df = frappe.meta.get_docfield("Procedure Prescription","procedure", frm.doc.name);
                df.read_only = 1; 
            }
            // let df = frappe.meta.get_docfield("Procedure Prescription","procedure", frm.doc.name);
            // df.read_only = 1;  
        });
    }
    
    // check item duplicate
    frm.check_items_duplicate = (frm, row) => {
        // console.log(row)
        if(frm.doc.procedure_prescription){
            frm.doc.procedure_prescription.forEach(item => {
                // console.log(item)
                if(row.procedure == ''  || row.idx == item.idx){
                    // pass
                } else {
                    if(row.procedure == item.procedure){
                        // clear field
                        row.procedure = '';
                        
                        frappe.throw(__(`${item.procedure} already exists in row ${item.idx}`));
                        row.procedure_name = '';
                        frm.refresh.field('procedure_prescription')
                    }
                }
            });
        }
        

        if(frm.doc.lab_test_prescription) {
            frm.doc.lab_test_prescription.forEach(item => {
                // console.log(item)
                if(row.lab_test_code == ''  || row.idx == item.idx){
                    // pass
                } else {
                    if(row.lab_test_code == item.lab_test_code){
                        // clear field
                        row.lab_test_code = '';
                        row.lab_test_name = '';
                        frappe.throw(__(`${item.lab_test_code} already exists in row ${item.idx}`));
                        frm.refresh.field('lab_test_prescription')
                    }
                }
            });
        }


        if(frm.doc.drug_prescription){
            frm.doc.drug_prescription.forEach(item => {
                // console.log(item)
                if(row.drug_code == ''  || row.idx == item.idx){
                    // pass
                } else {
                    if(row.drug_code == item.drug_code){
                        // clear field
                        row.drug_code = '';
                        
                        frappe.throw(__(`${item.drug_code} already exists in row ${item.idx}`));
                        row.drug_name = '';
                        frm.refresh.field('drug_prescription')
                    }
                }
            });
        }
    }
    
    frm.sub_item = async (frm, row) => {
        if (row.procedure){
        let procedure = await frappe.db.get_doc("Clinical Procedure Template", row.procedure)
        console.log(row.idx)
        let pro_sub_item = procedure.sub_items;
        let pro_sub_list = []
        let pro_sub = pro_sub_item.forEach(item => {
            pro_sub_list.push(item.item)
        })
        // console.log(pro_sub_list)
// 		Loop throug child table
        frm.doc.procedure_prescription.forEach((el , index) => {
          //  console.log(el)
        
            if((pro_sub_list.includes(el.procedure)) && (el.sub_item === 1)){
                    // console.log(el.)
                    el.sub_item = 0
                    frm.get_field("procedure_prescription").grid.grid_rows[row.idx - 1].remove()
                    // frm.doc.procedure_prescription.splice(frm.doc.procedure_prescription[el.idx]);
                    // frm.refresh_field('procedure_prescription')
                    // console.log(el.idx)
            }
                
        
        });
    }
    }
},





})


frappe.ui.form.on('Procedure Prescription', {

procedure: function(frm,cdt,cdn){
    //alert('ok')
        let row = locals[cdt][cdn]
        parent = row.procedure
        console.log(row.procedure)
        if(!frm.check_items_duplicate(frm, row)) {
         frappe.call({
        method: "rasiin.api.procedure_prescription.getSubitem", //dotted path to server method
        args : {"parent" :parent },
        callback: function(r) {
            // code snippet
            r.message.forEach( (data) => {
                //   console.log(data.name)
            
                let row = frm.add_child('procedure_prescription', {
            procedure: data.item,
            procedure_name: data.item,
            sub_item: 1
            
            });

            // frm.sub_item_readonly(frm)
            frm.refresh_field('procedure_prescription');

            })
          
        }
    })
        }
    

    
},

procedure_prescription_add: (frm, cdt, cdn) =>{
    // let df = frappe.meta.get_docfield("Procedure Prescription","procedure", frm.doc.name);
    // df.read_only = 0;
    // frm.refresh_field('procedure_prescription');
},

before_procedure_prescription_remove: (frm, cdt, cdn) => {
    let row = locals[cdt][cdn];
    if(!row.sub_item) {
        frm.sub_item(frm, row);
       // frappe.throw("You cannot delete sub item row")
    } else {
        frappe.throw("You cannot delete sub item row")
    }
    
    
    
}

})


frappe.ui.form.on('Lab Prescription', {
    lab_test_code: function(frm,cdt,cdn){
    //alert('ok')
        let row = locals[cdt][cdn]
        parent = row.lab_test_code
        // console.log(row.procedure)
        if(!frm.check_items_duplicate(frm, row)) {
         frappe.call({
        method: "rasiin.api.procedure_prescription.getLabSubitem", //dotted path to server method
        args : {"parent" :parent },
        callback: function(r) {
            // code snippet
            r.message.forEach( (data) => {
                //   console.log(data.name)
                  
            let row = frm.add_child('lab_test_prescription', {
            lab_test_code: data.item,
            lab_test_name: data.item
             });
            
            frm.refresh_field('lab_test_prescription');
            
                          
                    })
          
        }
    })    
    }
},

})


frappe.ui.form.on('Drug Prescription', {
    refresh(frm) {
        // your code here
    },
        drug_code: function(frm,cdt,cdn){
        //alert('ok')
            let row = locals[cdt][cdn]
            parent = row.lab_test_code
            // console.log(row.procedure)
            frm.check_items_duplicate(frm, row)
    },
    
    })