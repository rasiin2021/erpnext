import frappe
from frappe.utils import flt

def validate_discount_level(doc, method=None):
    discount_levels = {
        row.role: flt(row.discount_allowed)
        for row in frappe.get_all(
            "Discount Level", fields=("role", "discount_allowed")
        )
    }

    if not discount_levels:
        return

    current_discount = flt(
        flt(doc.discount_amount) / (
            flt(doc.total) + flt(doc.total_taxes_and_charges)
        ), 5
    ) * 100

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
