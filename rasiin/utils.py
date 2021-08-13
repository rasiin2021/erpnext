import frappe
from frappe.utils import flt


def get_discount_levels():
    return {
        row.role: flt(row.discount_allowed)
        for row in frappe.get_all("Discount Level", fields=("role", "discount_allowed"))
    }


def get_allowed_discount():
    discount_levels = get_discount_levels()
    if not discount_levels:
        return 100

    roles = frappe.get_roles()
    discount_levels = [
        discount_allowed
        for role, discount_allowed in discount_levels.items()
        if role in roles
    ]
    return max(discount_levels) if discount_levels else 0
