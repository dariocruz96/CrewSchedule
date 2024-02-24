from django import forms
from .models import Employee

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['firstName','lastName', 'email', 'password']
        widgets = {
            'password': forms.PasswordInput(),  # Render password field as a password input
        }