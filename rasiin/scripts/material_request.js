frappe.ui.form.on("Material Request", {
  onload(frm) {
    frm.fields_dict["medical_department"].grid.get_field("medical_department").get_query = function (doc) {
      return {
        filters: { company: doc.company },
      };
    };
    set_medical_department(frm);
  },
});
