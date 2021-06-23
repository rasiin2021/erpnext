# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from . import __version__ as app_version

app_name = "rasiin"
app_title = "Rasiin"
app_publisher = "Resilient Tech"
app_description = "Customisations to Frappe / ERPNext for Rasiin"
app_icon = "octicon octicon-file-directory"
app_color = "grey"
app_email = "sagar@resilient.tech"
app_license = "MIT"
after_install = "rasiin.install.after_install"

app_include_js = "/assets/js/rasiin.min.js"

doctype_js = {
    "Sales Invoice": "scripts/sales_invoice.js"
}

doc_events = {
    "Sales Invoice": {
        "validate": "rasiin.api.sales_invoice.validate_discount_level"
    }
}
