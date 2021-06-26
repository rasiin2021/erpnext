from __future__ import unicode_literals
from frappe import _

def get_data():
	return {
		'fieldname': 'appointment',
		'non_standard_fieldnames': {
			'Patient Medical Record': 'reference_name'
		},
		'transactions': [
			{
				'label': _('Follow UP'),
				'items': ['Patient FollowUp', 'Vital Signs']
			}
		]
	}
