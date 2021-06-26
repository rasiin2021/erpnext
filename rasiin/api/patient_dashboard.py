from __future__ import unicode_literals
from frappe import _

def get_data():
	return {
		'heatmap': True,
		'heatmap_message': _('This is based on transactions against this Patient. See timeline below for details'),
		'fieldname': 'patient',
		'transactions': [
			{
				'label': _('Appointments, Feedback and Patient Encounters'),
				'items': ['Triage', 'Patient Appointment', 'Patient Encounter', 'Follow Up', 'Feedback']
			},
			{
				'label': _('Lab Tests and Vital Signs'),
 				'items': ['Lab Test', 'Sample Collection', 'Vital Signs']
			},
			{
				'label': _('Billing'),
				'items': ['Sales Invoice']
			},
			{
				'label': _('Insurance'),
				'items': ['Insurance Assignment']
			}
		]
	}
