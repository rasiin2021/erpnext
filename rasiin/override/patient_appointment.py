import datetime
import frappe
from frappe import _
from frappe.utils import getdate, get_time, flt
from erpnext.healthcare.doctype.patient_appointment.patient_appointment import PatientAppointment

class CustomPatientAppointment(PatientAppointment):
	def validate_overlaps(self):
		end_time = datetime.datetime.combine(
			getdate(self.appointment_date), get_time(self.appointment_time)
		) + datetime.timedelta(minutes=flt(self.duration))

		overlaps = frappe.db.sql("""
		select
			name, practitioner, patient, appointment_time, duration, notes, department
		from
			`tabPatient Appointment`
		where
			appointment_date=%s and name!=%s and status NOT IN ("Closed", "Cancelled")
			and (practitioner=%s or patient=%s) and
			((appointment_time<%s and appointment_time + INTERVAL duration MINUTE>%s) or
			(appointment_time>%s and appointment_time<%s) or
			(appointment_time=%s))
		""", (self.appointment_date, self.name, self.practitioner, self.patient,
		self.appointment_time, end_time.time(), self.appointment_time, end_time.time(), self.appointment_time))

		if overlaps:
			overlapping_details = _("Appointment overlaps with ")
			overlapping_details += (
				"<b><a href='/app/Form/Patient Appointment/{0}'>{0}</a></b><br>".format(
					overlaps[0][0]
				)
			)
			overlapping_details += _(
				"{0} has appointment scheduled with {1} at {2} having {3} minute(s) duration."
			).format(overlaps[0][1], overlaps[0][2], overlaps[0][3], overlaps[0][4])
			frappe.throw(overlapping_details, title=_("Appointments Overlapping"))

