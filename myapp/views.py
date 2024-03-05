from django.shortcuts import render, redirect, get_object_or_404
from .forms import EmployeeForm, ShiftForm, EmployeeAssignmentForm
from .models import Employee, EmployeeAssignment, Shift, Rota
from datetime import datetime, timedelta


def get_week_start_end_dates(selected_date):
    # Calculate the start date of the week (Monday)
    start_of_week = selected_date - timedelta(days=selected_date.weekday())

    # Calculate the end date of the week (Sunday)
    end_of_week = start_of_week + timedelta(days=6)

    return start_of_week, end_of_week

def home_view(request):
    # Fetch necessary data for the rota
    employees = Employee.objects.all()
    rota = Rota.objects.all()  # Assuming rota model contains the assignments

    # Define days of the week
    days_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

    # Pass the data to the template
    return render(request, 'home.html', {
        'employees': employees,
        'days_of_week': days_of_week,
        'rota': rota,
    })

def login_view(request):
    return render(request, 'login.html')

# Start of employee views----------------------------------------------------
def employee_list(request):
    employees = Employee.objects.all()
    return render(request, 'employee_list.html', {'employees': employees})

def employee_detail(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    return render(request, 'employee_detail.html', {'employee': employee})

def employee_create(request):
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('employee_list')
    else:
        form = EmployeeForm()
    return render(request, 'employee_form.html', {'form': form})

def employee_update(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    if request.method == 'POST':
        form = EmployeeForm(request.POST, instance=employee)
        if form.is_valid():
            form.save()
            return redirect('employee_list')
    else:
        form = EmployeeForm(instance=employee)
    return render(request, 'employee_form.html', {'form': form})

def employee_delete(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    if request.method == 'POST':
        employee.delete()
        return redirect('employee_list')
    return render(request, 'employee_confirm_delete.html', {'employee': employee})

# End of employee views----------------------------------------------------
# Start of Shift views----------------------------------------------------
def create_shift(request):
    if request.method == 'POST':
        shift_form = ShiftForm(request.POST)
        if shift_form.is_valid():
            # Save the shift
            shift = shift_form.save()

            # Assign the shift to the first employee (you can change this logic)
            employee_assignment = EmployeeAssignment.objects.create(shift=shift, employee=Employee.objects.first())

            return redirect('manage_rota')  # Redirect to manage rota page after creating shift and assignment
    else:
        shift_form = ShiftForm()

    return render(request, 'create_shift.html', {'shift_form': shift_form})

def assign_employee(request):
    if request.method == 'POST':
        form = EmployeeAssignmentForm(request.POST)
        if form.is_valid():
            form.save()  # Save the assigned shift to the database
            return redirect('manage_rota')  # Redirect to manage rota page
    else:
        form = EmployeeAssignmentForm()
    return render(request, 'assign_employee.html', {'form': form})
def rota(request):
    rota = EmployeeAssignment.objects.select_related('shift', 'employee').all()
    return render(request, 'home.html', {'rota': rota})
# End  of Shift views----------------------------------------------------

def manage_users_view(request):
    # Fetch all employees from the database
    employees = Employee.objects.all()
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            form.save()
            # Redirect to the same view function
            return redirect('manage_users') 
    else:
        form = EmployeeForm()
    
    return render(request, 'manage_users.html', {'form': form, 'employees': employees})

def manage_rota_view(request):
    # Fetch all employees, shifts, and rota data
    employees = Employee.objects.all()
    shifts = Shift.objects.all()
    rota = Rota.objects.all()  # Assuming Rota model contains the assignments

    # Define days of the week
    days_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

    # Handle form submission for adding a new shift
    if request.method == 'POST':
        form = ShiftForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('manage_rota')  # Redirect to manage rota page after adding shift
    else:
        form = ShiftForm()

    # Handle form submission for assigning an employee to a shift
    if request.method == 'POST':
        assignment_form = EmployeeAssignmentForm(request.POST)
        if assignment_form.is_valid():
            assignment_form.save()
            return redirect('success_page')  # Redirect to a success page after assigning employee to shift
    else:
        assignment_form = EmployeeAssignmentForm()

    # Render the template with the necessary context variables
    return render(request, 'manage_rota.html', {
        'shifts': shifts,
        'shift_form': form,
        'employees': employees,
        'assignment_form': assignment_form,
        'days_of_week': days_of_week,
        'rota': rota,  # Pass rota data to the template
    })

def manage_shifts_view(request):
    shifts = Shift.objects.all()
    rota = Rota.objects.all()  # Assuming Rota model contains the assignments

    # Define days of the week
    days_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

    # Handle form submission for adding a new shift
    if request.method == 'POST':
        form = ShiftForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('manage_shifts')  # Redirect to manage rota page after adding shift
    else:
        form = ShiftForm()

    # Render the template with the necessary context variables
    return render(request, 'manage_shifts.html', {
        'shifts': shifts,
        'shift_form': form,
        'days_of_week': days_of_week,
        'rota': rota,  # Pass rota data to the template
    })

def register_employee(request):

    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('manage_users')  # Redirect to same page
    else:
        form = EmployeeForm()
    return render(request, 'manage_users.html', {'form': form})

def test_add_to_schedule(request):
    if request.method == 'POST':
        form = EmployeeAssignmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('success_page')  # Redirect to a success page
    else:
        form = EmployeeAssignmentForm()
    return render(request, 'test_add_to_schedule.html', {'form': form})