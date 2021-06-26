const to_remove = {
  "Purchase Receipt": [
    "Purchase Return",
    "Make Stock Entry",
    "Retention Stock Entry",
    "Subscription",
  ],
  "Material Request": [
      "Purchase Order",
      "Supplier Quotation"
  ],
  "Supplier Quotation": [
      "Quotation",
      "Subscription"
  ],
  "Purchase Order": [
      "Invoice",
      "Subscription",
      "Payment Request",
      "Payment"
  ]
};

modifyMethod(
  "frappe.ui.form.Form",
  "add_custom_button",
  function (label, fn, group) {
    const buttons_to_remove = to_remove[this.doctype];
    if (typeof group != "string" || !buttons_to_remove) return;

    group = group.toLowerCase();
    if (
      (group === "create" || group === "get items from") &&
      buttons_to_remove.indexOf(label) !== -1
    )
      return "return";
  },
  true
);
