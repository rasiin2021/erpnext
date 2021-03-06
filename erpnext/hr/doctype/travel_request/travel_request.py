# -*- coding: utf-8 -*-
# Copyright (c) 2018, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from erpnext.hr.utils import validate_active_employee

class TravelRequest(Document):
	def validate(self):
		validate_active_employee(self.employee)
