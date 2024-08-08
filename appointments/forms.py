from django import forms
from .models import Appointment

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['specialty', 'appointment_date', 'start_time']
        widgets = {
            'appointment_date': forms.SelectDateWidget(),
            'start_time': forms.TimeInput(attrs={'type': 'time'}),
        }
