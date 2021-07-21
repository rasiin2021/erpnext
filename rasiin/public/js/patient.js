modifyMethod("frappe.ui.form.QuickEntryForm", "setup", function () {
  set_mode_of_payment(this.dialog);
});

frappe.ui.form.on("Patient", {
  onload(frm) {
    if (!frm.is_new()) return;
    set_mode_of_payment(frm);
  },
});

function set_mode_of_payment(object) {
  frappe
    .xcall("rasiin.api.patient.get_mode_of_payment")
    .then((r) => r && object.set_value("mode_of_payment", r));
}
