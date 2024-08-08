from django.db import models
from accounts.models import User
from datetime import datetime, timedelta, date


class Appointment(models.Model):
    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='appointments')
    doctor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='doctor_appointments')
    specialty = models.CharField(max_length=100)
    appointment_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    
    def save(self, *args, **kwargs):
        # Automatically set end time as 45 mins after start time
        self.end_time = (datetime.combine(date.today(), self.start_time) + timedelta(minutes=45)).time()
        super(Appointment, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.patient.username} - {self.doctor.username} on {self.appointment_date} at {self.start_time}"
