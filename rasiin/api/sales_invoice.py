import frappe
from frappe.utils import flt


def validate_discount_level(doc, method=None):
    if doc.discount_amount > 0:
        frappe.throw("Discount Amount is not allowed, please set Write Off Amount instead")

    discount_levels = get_discount_levels()

    if not discount_levels:
        return

    current_discount = (
        flt(
            flt(doc.write_off_amount)
            / (flt(doc.total) + flt(doc.total_taxes_and_charges)),
            5,
        )
        * 100
    )

    user_roles = frappe.get_roles()

    for role in sorted(discount_levels, key=discount_levels.get, reverse=True):
        if role not in user_roles:
            continue

        discount_allowed = discount_levels[role]
        if current_discount > discount_allowed:
            frappe.throw(
                "You are not permitted to give a discount greater than "
                "{}% of Grand Total Before Discount".format(discount_allowed)
            )
        break


def get_discount_levels():
    return {
        row.role: flt(row.discount_allowed)
        for row in frappe.get_all("Discount Level", fields=("role", "discount_allowed"))
    }


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
