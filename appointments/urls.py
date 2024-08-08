from django.urls import path
from .views import doctor_list, book_appointment, appointment_confirmation

urlpatterns = [
    path('doctors/', doctor_list, name='doctor_list'),
    path('doctors/<int:doctor_id>/book/', book_appointment, name='book_appointment'),
    path('appointments/<int:appointment_id>/confirmation/', appointment_confirmation, name='appointment_confirmation'),
]
