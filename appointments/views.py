from django.shortcuts import render, redirect
from .models import Appointment
from .forms import AppointmentForm
from accounts.models import User
from googleapiclient.discovery import build
from google.oauth2 import service_account
from datetime import datetime, timedelta
import pytz
from django.conf import settings
import os

def get_google_calendar_service():
    SCOPES = ['https://www.googleapis.com/auth/calendar']
    SERVICE_ACCOUNT_FILE = os.path.join(
    settings.BASE_DIR, 'appointments', 'client_secret_500191717141-53tqlkevi1u7gn3rurpultvmfqa3jr8i.apps.googleusercontent.com.json'
)

    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)

    service = build('calendar', 'v3', credentials=credentials)
    return service

def doctor_list(request):
    doctors = User.objects.filter(user_type='doctor')
    return render(request, 'doctor_list.html', {'doctors': doctors})

def book_appointment(request, doctor_id):
    doctor = User.objects.get(id=doctor_id)
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.patient = request.user
            appointment.doctor = doctor
            
            start_time = datetime.combine(appointment.appointment_date, appointment.start_time)
            appointment.end_time = start_time + timedelta(minutes=45) 
            
            appointment.save()  
            
            create_google_calendar_event(appointment)  
            
            return redirect('appointment_confirmation', appointment.id)
    else:
        form = AppointmentForm()
    return render(request, 'book_appointment.html', {'form': form, 'doctor': doctor})

def appointment_confirmation(request, appointment_id):
    appointment = Appointment.objects.get(id=appointment_id)
    return render(request, 'confirmation.html', {'appointment': appointment})

def create_google_calendar_event(appointment):
    service = get_google_calendar_service() 

    start_time = datetime.combine(appointment.appointment_date, appointment.start_time)
    end_time = start_time + timedelta(minutes=45)

    event = {
        'summary': f'Appointment with {appointment.patient.username}', 
        'description': 'Doctor Appointment',
        'start': {
            'dateTime': start_time.isoformat(),
            'timeZone': 'Asia/Kolkata', 
        },
        'end': {
            'dateTime': end_time.isoformat(),
            'timeZone': 'Asia/Kolkata',
        },
        'reminders': {
            'useDefault': False,
            'overrides': [
                {'method': 'email', 'minutes': 24 * 60},  
                {'method': 'popup', 'minutes': 10}, 
            ],
        },
    }

    doctor_email = appointment.doctor.email  
    service.events().insert(calendarId=doctor_email, body=event).execute()
