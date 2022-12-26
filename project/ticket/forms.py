from django import forms
from .models import *


class SignupForm(forms.ModelForm):
    class Meta:
        model= CustomUserModel
        fields=('email','mobile', 'first_name', 'last_name', 'role', 'profile_pic','status')
        # fields = "__all__"


class DateInput(forms.DateInput):
    input_type = 'date'


class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['user','mobile','assets','priority','serial_no','model_no','ticketstatus','assigned_to']





    # widgets = {
    #             'birthdate': SelectDateWidget(attrs = {
    #              },years = range(1920, 2017),),
    #          }