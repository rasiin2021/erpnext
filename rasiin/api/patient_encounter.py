import frappe
from frappe import _
from frappe.utils import today
from frappe.model.mapper import get_mapped_doc

def enqueue_sales_orders(doc, method=None):
    frappe.enqueue(create_sales_orders, doc=doc)

def create_sales_orders(doc):
    for so_type in ("medication_so", "services_so"):
        sales_order = None
        so_name = doc.get(so_type)
        if so_name:
            sales_order = frappe.get_doc("Sales Order", so_name)
            sales_order.items = []

        table_maps = {
            "Patient Encounter": {
                "doctype": "Sales Order",
                "field_no_map": ["source"]
            },
        }

        if so_type == "medication_so":
            table_maps["Drug Prescription"] = {
                "doctype": "Sales Order Item",
                "field_map": {
                    "drug_code": "item_code",
                    "drug_name": "item_name",
                },
                "postprocess": update_item
            }
        else:
            return

        sales_order = get_mapped_doc(
            doc.doctype,
            doc.name,
            table_maps,
            sales_order
        )

        sales_order.customer = frappe.get_value("Patient", doc.patient, "customer")
        if not sales_order.customer:
            frappe.throw("Please set a Customer linked to the Patient")

        sales_order.flags.ignore_validate_update_after_submit = 1
        sales_order.delivery_date = today()
        sales_order.save()

        if so_name != sales_order.name:
            doc.db_set(so_type, sales_order.name)

def update_item(source, target, source_parent):
    if source_parent.get('branch'):
        target.branch = source_parent.branch

    target.reference_dt = source.doctype
    target.reference_dn = source.name

    if not target.qty:
        target.qty = 1
        if frappe.db.get_value("Item", source.drug_code, "stock_uom") in ("Nos", "Each"):
            target.qty = source.get_quantity()

    if not target.description:
        target.description = ""
        if source.dosage and source.period:
            target.description = _('{0} for {1}').format(
                source.dosage, source.period
            )

