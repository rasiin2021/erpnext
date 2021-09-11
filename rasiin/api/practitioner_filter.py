import frappe
from frappe.desk.reportview import get_filters_cond, get_match_cond
from frappe.utils import  unique
@frappe.whitelist()
@frappe.validate_and_sanitize_search_inputs
def practitioner_filter(doctype, txt, searchfield, start, page_len, filters):
    department = filters.get('department')
    status = filters.get('status')
    conditions = []
    fields = get_fields(doctype, ["practitioner_name", "department", "status"])
    if department and status:
        return frappe.db.sql("""select {fields} from `tabHealthcare Practitioner`
                where department = '{department}' 
                    and status = '{status}'
                    and ({key} like %(txt)s
                        or practitioner_name like %(txt)s)
                    {fcond} {mcond}
                order by
                    if(locate(%(_txt)s, name), locate(%(_txt)s, name), 99999),
                    if(locate(%(_txt)s, practitioner_name), locate(%(_txt)s, practitioner_name), 99999),
                    idx desc,
                    name, practitioner_name
                limit %(start)s, %(page_len)s""".format(**{
                    'fields': ", ".join(fields),
                    'key': searchfield,
                    'department': department,
                    'status': status,
                    'fcond': get_filters_cond(doctype, filters, conditions),
                    'mcond': get_match_cond(doctype)
                }), {
                    'txt': "%%%s%%" % txt,
                    '_txt': txt.replace("%", ""),
                    'start': start,
                    'page_len': page_len
                })
                
    
    return frappe.db.sql("""select {fields} from `tabHealthcare Practitioner`
                where status = '{status}'
                    and ({key} like %(txt)s
                        or practitioner_name like %(txt)s)
                    {fcond} {mcond}
                order by
                    if(locate(%(_txt)s, name), locate(%(_txt)s, name), 99999),
                    if(locate(%(_txt)s, practitioner_name), locate(%(_txt)s, practitioner_name), 99999),
                    idx desc,
                    name, practitioner_name
                limit %(start)s, %(page_len)s""".format(**{
                    'fields': ", ".join(fields),
                    'key': searchfield,
                    'status': status,
                    'fcond': get_filters_cond(doctype, filters, conditions),
                    'mcond': get_match_cond(doctype)
                }), {
                    'txt': "%%%s%%" % txt,
                    '_txt': txt.replace("%", ""),
                    'start': start,
                    'page_len': page_len
                })
    # return frappe.throw(filters)
 

def get_fields(doctype, fields=None):
    if fields is None:
        fields = []
    meta = frappe.get_meta(doctype)
    fields.extend(meta.get_search_fields())

    if meta.title_field and not meta.title_field.strip() in fields:
        fields.insert(1, meta.title_field.strip())

    return unique(fields)