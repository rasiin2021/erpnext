import frappe
from frappe import _
from frappe.utils import getdate
from frappe.model.mapper import map_doc


def enqueue_sales_orders(doc, method=None):
    frappe.enqueue(create_sales_orders, doc=doc)


def create_sales_orders(doc):
    for so_type in ("medication_so", "services_so"):
        sales_order = None
        so_name = doc.get(so_type)
        if so_name:
            sales_order = frappe.get_doc("Sales Order", so_name)
        else:
            sales_order = frappe.new_doc("Sales Order")

        map_doc(
            doc,
            sales_order,
            {
                "Patient Encounter": {
                    "doctype": "Sales Order",
                    "field_no_map": ["source", "docstatus"],
                },
            },
        )

        sales_order.__updated_items = []
        sales_order.delivery_date = getdate()
        sales_order.customer = frappe.db.get_value("Patient", doc.patient, "customer")
        if not sales_order.customer:
            frappe.throw("Please set a Customer linked to the Patient")

        if so_type == "medication_so":
            add_drug_items(sales_order, doc)

        elif so_type == "services_so":
            add_visit_charge(sales_order, doc)
            add_service_items(sales_order, doc)

        sales_order.items = [
            row
            for row in sales_order.get("items", default=[])
            if row.reference_dn in sales_order.__updated_items
        ]

        if not sales_order.items and not sales_order.name:
            continue

        sales_order.flags.ignore_links = 1
        sales_order.flags.ignore_validate_update_after_submit = 1
        sales_order.flags.ignore_permissions = 1

        if sales_order.name:
            if not sales_order.items:
                sales_order.reload()
                sales_order.cancel()
                doc.db_set(so_type, "", notify=True)
                continue

            sales_order.db_set("docstatus", 0, update_modified=False)

        sales_order.save()
        sales_order.submit()

        if so_name != sales_order.name:
            doc.db_set(so_type, sales_order.name, notify=True)


def add_drug_items(so, doc):
    for row in doc.drug_prescription:
        so_item = find_or_create_item(row, so, doc)
        so_item.item_code = row.drug_code
        so_item.item_name = row.drug_name
        so_item.qty = 1
        if frappe.db.get_value("Item", row.drug_code, "stock_uom") in (
            "Nos",
            "Each",
            "Pcs",
        ):
            so_item.qty = row.get_quantity()

        so_item.description = ""
        if row.dosage and row.period:
            so_item.description = _("{0} for {1}").format(row.dosage, row.period)


def add_visit_charge(so, doc):
    if not doc.appointment or (
        doc.inpatient_record
        and frappe.db.get_single_value(
            "Healthcare Settings", "do_not_bill_inpatient_encounters"
        )
    ):
        return

        practitioner_charge = 0
        income_account = None
        service_item = None

        if doc.practitioner:
            details = get_service_item_and_practitioner_charge(doc)
            service_item = details.get("service_item")
            practitioner_charge = details.get("practitioner_charge")
            income_account = get_income_account(doc.practitioner, doc.company)

        so_item = find_or_create_item(doc, so, doc)
        so_item.update(
            {
                "item_code": service_item,
                "rate": practitioner_charge,
                "income_account": income_account,
            }
        )


def add_service_items(so, doc):
    for child_table in ("lab_test_prescription", "procedure_prescription"):
        for row in doc.get(child_table):
            item, is_billable = get_item_and_is_billable(row)
            if not item or not is_billable:
                continue

            so_item = find_or_create_item(row, so, doc)
            so_item.item_code = item
            so_item.qty = 1


def get_item_and_is_billable(row):
    if row.doctype == "Lab Prescription":
        return frappe.get_cached_value(
            "Lab Test Template", row.lab_test_code, ("item", "is_billable")
        )
    elif row.doctype == "Procedure Prescription":
        return frappe.get_cached_value(
            "Clinical Procedure Template", row.procedure, ("item", "is_billable")
        )


def find_or_create_item(row, so, doc):
    for item in so.get("items"):
        if item.reference_dn == row.name:
            break
    else:
        item = so.append("items")
        item.reference_dt = row.doctype
        item.reference_dn = row.name

    if doc.get("branch"):
        item.branch = doc.branch

    so.__updated_items.append(item.reference_dn)
    return item
