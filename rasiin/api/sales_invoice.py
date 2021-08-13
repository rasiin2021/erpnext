import frappe


def validate_discount_level(doc, method=None):
    if doc.discount_amount:
        frappe.throw(
            "Discount Amount is not allowed, please set Write Off Amount instead"
        )


def validate_paid_amount(doc, method=None):
    if doc.is_return or not doc.is_pos or doc.docstatus:
        return

    def get_currency_display(fieldname):
        return frappe.bold(doc.get_formatted(fieldname))

    if doc.paid_amount > doc.grand_total:
        frappe.throw(
            "Paid Amount ({0}) cannot be greater than Grand Total ({1})".format(
                get_currency_display("paid_amount"),
                get_currency_display("grand_total"),
            )
        )
