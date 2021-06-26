# -*- coding: utf-8 -*-
# Copyright (c) 2020, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe.core.doctype.sms_settings.sms_settings import send_sms

class VaccineInternal(Document):
	def on_submit(self):
               fam_care_msg(self)

def fam_care_msg(doc):
            if frappe.db.get_value("Healthcare Settings", None, "vaccine") == '1':
                    message = frappe.db.get_value("Healthcare Settings", None, "vaccine_msg")
                   	# send_message(doc, message)

def send_message(doc, message):
        patient = frappe.get_doc("Patient", doc.patient)
        if patient.mobile:
                context = {"doc": doc, "alert": doc, "comments": None}
                if doc.get("_comments"):
                        context["comments"] = json.loads(doc.get("_comments"))

                # jinja to string convertion happens here
                message = frappe.render_template(message, context)
                number = [patient.mobile]
                try:
                        send_sms(number, message)
                except Exception as e:
                        frappe.msgprint(_("SMS not send Please check your SMS Settings"), alert=True)
