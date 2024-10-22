from django import forms
from .models import Employee, Shift, EmployeeShift, Rota
from django.forms.widgets import DateInput,TimeInput

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['firstName','lastName', 'email', 'password']
        widgets = {
            'password': forms.PasswordInput(),  # Render password field as a password input
        }

class ShiftForm(forms.ModelForm):
    class Meta:
        model = Shift
        fields = ['start_time', 'end_time', 'date']
        widgets = {
            'start_time': forms.TimeInput(attrs={'type': 'time'}),  # Use  TimeInput widget for start_time
            'end_time': forms.TimeInput(attrs={'type': 'time'}),    # Use  TimeInput widget for end_time
            'date': forms.DateInput(attrs={'type': 'date'})  # Use DateInput widget for the 'date' field
        }
class EmployeeShiftForm(forms.ModelForm):
    # Define a field to select employees for the shift
    employees = forms.ModelMultipleChoiceField(queryset=Employee.objects.all(), required=False)

    class Meta:
        model = EmployeeShift
        fields = ['employee', 'shift', 'is_assigned']

class EmployeeAssignmentForm(forms.ModelForm):
    class Meta:
        model = Rota
        fields = ['shift', 'employee']