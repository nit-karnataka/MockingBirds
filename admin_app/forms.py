from django import forms
import datetime
from django.db import models
from .models import *
from django.contrib.admin import widgets
from django.forms.fields import DateField


class DateInput(forms.DateInput):
    input_type = 'date'

class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

class SignupForm(forms.Form):
    name = forms.CharField()
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

class StudentDetailsForm(forms.ModelForm):

    class Meta:
        model = student_model
        fields = ['name','email', 'research_department_email','faculty_incharge_email','faculty_incharge_name','faculty_incharge_phone','phone_no','research_area','date_of_tenure_completion','keywords','research_department_name','research_department_phone']
        exclude=['date_of_query',]
        widgets = {
                    'date_of_tenure_completion': DateInput(),
                }
class StudentUpdateEmail(forms.Form):
    email = forms.EmailField()

class and_or_search(forms.ModelForm):

    class Meta:
        model = and_or_search_model
        fields=['and_or_search','frequency']
        exclude=['email','date_of_query']
