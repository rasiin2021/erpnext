import frappe 
@frappe.whitelist()
def getSubitem(parent = None):
	res = frappe.db.sql(f"""select * from `tabClinical Procedure subitems` where parent = '{parent}' ; """ , as_dict = True )
	return res

@frappe.whitelist()
def getLabSubitem(parent = None):
        res = frappe.db.sql(f"""select * from `tabLab Subitems` where parent = '{parent}' ; """ , as_dict = True )
        return res
