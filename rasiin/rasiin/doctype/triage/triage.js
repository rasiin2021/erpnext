frappe.ui.form.on("Triage", {
    
    refresh: frm => {
        // let status = "Active"
        // frm.set_query('practitioner_name', () => {
        //     return {
        //         query: "rasiin.api.triage_practitioner_filter.practitioner_filter",
        //             filters: {
        //                         "status": status
        //                     }
        //             }
        // })
        $(frm.fields_dict.practitioner_name.input).on('focus', function(e) {
          
        })

        
        
        if(frm.is_new()) {
            frm.set_df_property("check_symptoms", "hidden", true);
            frm.set_df_property("complain", "hidden", true);
            frm.set_df_property("symptoms_select", "hidden", true);
            frm.set_df_property("symptoms", "hidden", true);
            frm.set_df_property("medical_department", "hidden", true);
            frm.set_df_property("practitioner_name", "hidden", true);
            frm.set_df_property("has_appointment", "hidden", true);
            
            frm.get_field("check_symptoms").$input.removeClass().addClass("btn btn-primary btn-sm primary-action mt-4");
            $(frm.fields_dict.check_symptoms.input).on('click', function(e) {
                let symptoms = frm.doc.symptoms;
                // console.log(symptoms)
                if(symptoms) {
                    let medical_department = [];
                    let awaitfun = [];
                    let arrOfSymptoms = symptoms.split("\n");
                    
                    if (arrOfSymptoms.length > 2) {
                        let forEachFunc = arrOfSymptoms.forEach(async symp => {
                            let docname = await frappe.db.get_doc("Symptom Test", symp);
                            medical_department.push(docname.department);
                        });
                    }
                    
                    setTimeout(() => {
                        const hashmap = medical_department.reduce( (acc, val) => {
                            acc[val] = (acc[val] || 0 ) + 1;
                            return acc;
                        },{});
                        var maxi =  Object.keys(hashmap).reduce((a, b) => hashmap[a] > hashmap[b] ? a : b);
                        console.log(maxi);
                        cur_frm.set_value("medical_department", maxi);
                    }, 500)
                    
                }
            });
            
                        if(frm.doc.patient) {
            // console.log(frm.doc.dob)
            let start_date = new Date().getFullYear()
            let end_date = new Date(frm.doc.dob).getFullYear() 
            let age = start_date -end_date; 
            cur_frm.set_value("age", age);
            console.log(age)
            
            if(age <= 15) {
                cur_frm.set_value("medical_department", "Pediatric")
                frm.set_df_property("medical_department", "hidden", false);
                frm.set_df_property("practitioner_name", "hidden", false);
                
                frm.set_df_property("check_symptoms", "hidden", true);
                frm.set_df_property("symptoms_select", "hidden", false);
                frm.set_df_property("symptoms", "hidden", false);
                // cur_frm.set_intro("Patient " + frm.doc.patient_name + "'s Age is " + frm.doc.age + " years")
                // console.log(df)
                // frm.refresh_fields()
            } else {
                // cur_frm.set_intro("")
                frm.set_df_property("check_symptoms", "hidden", false);
                frm.set_df_property("symptoms_select", "hidden", false);
                frm.set_df_property("symptoms", "hidden", false);
                frm.set_df_property("medical_department", "hidden", false);
                frm.set_df_property("practitioner_name", "hidden", false);
                frm.set_df_property("has_appointment", "hidden", false);
            }
        }

        } else {
            frm.set_df_property("check_symptoms", "hidden", true);
        }
        
    },
    patient: frm => {
        if(frm.is_new()) {
            if(frm.doc.patient) {
            // console.log(frm.doc.dob)
            let start_date = new Date().getFullYear()
            let end_date = new Date(frm.doc.dob).getFullYear() 
            let age = start_date -end_date; 
            cur_frm.set_value("age", age);
            console.log(age)
            
            if(age <= 15) {
                cur_frm.set_value("medical_department", "Pediatric")
                frm.set_df_property("medical_department", "hidden", false);
                frm.set_df_property("practitioner_name", "hidden", false);
                
                frm.set_df_property("check_symptoms", "hidden", true);
                frm.set_df_property("symptoms_select", "hidden", false);
                frm.set_df_property("symptoms", "hidden", false);
                frm.set_intro(" ")
                frm.set_intro("Patient " + frm.doc.patient_name + "'s Age is " + frm.doc.age + " years")
                // console.log(df)
                // frm.refresh_fields()
            } else {
                // cur_frm.set_intro("")
                frm.set_df_property("check_symptoms", "hidden", false);
                frm.set_df_property("symptoms_select", "hidden", false);
                frm.set_df_property("symptoms", "hidden", false);
                frm.set_df_property("medical_department", "hidden", false);
                frm.set_df_property("practitioner_name", "hidden", false);
                frm.set_df_property("has_appointment", "hidden", false);
            }
        }
        }
        
    },
    
    symptoms_select: frm =>{
        if(frm.doc.symptoms_select){
            var symptoms = null;
            var string = "";

            if(frm.doc.symptoms)
                symptoms = frm.doc.symptoms + "\n" +frm.doc.symptoms_select;
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
                    frappe.model.set_value(frm.doctype,frm.docname, "symptoms", new_array.join("\n"));
                }
                    
            });
            ;
            frappe.model.set_value(frm.doctype,frm.docname, "symptoms_select", null);
            $(frm.fields_dict.symptoms_select.input).blur();
        }
    },


	medical_department: frm => {
        // let medical_department = frm.doc.medical_department
        // let status = "Active"
        // if (medical_department) {
        //     frm.set_query('practitioner_name', () => {
        //         return {
        //             query: "rasiin.api.triage_practitioner_filter.practitioner_filter",
        //                 filters: {
        //                             "department": medical_department,
        //                             "status": status
        //                         }
        //                 }
        //             })
        // }
        // refresh_field("practitioner_name");
    },

    choices: frm => {
        if(frm.doc.choices != "Triage Doctor Choice") {
            frm.set_df_property("check_symptoms", "hidden", true);
        } else if (frm.doc.choices == "Triage Doctor Choice" && frm.doc.age <= 15) {
            frm.set_df_property("check_symptoms", "hidden", true);
        } else {
            frm.set_df_property("check_symptoms", "hidden", false);
        }
    },


});