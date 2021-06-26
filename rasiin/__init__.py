# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import frappe

__version__ = '0.0.1'

# for web patches
old_get_hooks = frappe.get_hooks

def get_hooks(*args, **kwargs):
	if "rasiin" in frappe.get_installed_apps():
		import rasiin.monkey_patches

	return old_get_hooks(*args, **kwargs)

frappe.get_hooks = get_hooks


# for scheduler patches
old_connect = frappe.connect

def connect(*args, **kwargs):
	old_connect(*args, **kwargs)
	if "rasiin" in frappe.get_installed_apps():
		import rasiin.monkey_patches

frappe.connect = connect
