from django.shortcuts import render, redirect, get_object_or_404
from .forms import EmployeeForm
from .models import Employee

def home_view(request):
    return render(request, 'home.html')

def login_view(request):
    return render(request, 'login.html')

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
    # Logic for managing rota goes here
    return render(request, 'manage_rota.html')

def register_employee(request):

    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('manage_users.html')  # Redirect to same page
    else:
        form = EmployeeForm()
    return render(request, 'manage_users.html', {'form': form})