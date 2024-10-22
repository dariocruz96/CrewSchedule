from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from .forms import EmployeeForm, ShiftForm, EmployeeAssignmentForm
from .models import Employee, EmployeeAssignment, Shift, Rota
from .serializers import EmployeeSerializer, RotaSerializer, ShiftSerializer, EmployeeAssignmentSerializer
from datetime import datetime, timedelta
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response

def get_week_start_end_dates(selected_date):
    # Calculate the start date of the week (Monday)
    start_of_week = selected_date - timedelta(days=selected_date.weekday())

    # Calculate the end date of the week (Sunday)
    end_of_week = start_of_week + timedelta(days=6)

    return start_of_week, end_of_week

def get_monday(date):
    # Calculate the number of days from Monday (0: Monday, 1: Tuesday, ..., 6: Sunday)
    days_from_monday = date.weekday()
    # Subtract the number of days from the current date to get the nearest past Monday
    monday = date - timedelta(days=days_from_monday)
    return monday

def get_week_dates(start_date):
    # Initialize a list to store the dates of the week
    week_dates = []
    # Loop through 7 days to get the dates from start_date to start_date + 6 days
    for i in range(7):
        monday = get_monday(start_date)
        date = monday + timedelta(days=i)
        week_dates.append(date.strftime("%d/%m"))
        print(week_dates)
    return week_dates


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
def create_shift_modal(request):
    if request.method == "POST":
        form = ShiftForm(request.POST)
        if form.is_valid():
            form.save()
            response_headers = {'HX-Trigger': 'shiftChanged'}
            print("Response Headers:", response_headers)
            return HttpResponse(status=204, headers={'HX-Trigger': 'shiftChanged'})
    else:
        form = ShiftForm()
    return render(request, 'shift_form.html', {'form': form})

def edit_shift_modal(request, pk):
    shift = get_object_or_404(Shift, pk=pk)
    
    if request.method == 'POST':
        form = ShiftForm(request.POST, instance=shift)
        if form.is_valid():
            form.save()
            # Return a successful response with HTMX trigger to update the UI
            return HttpResponse(status=204, headers={'HX-Trigger': 'shiftChanged'})
    elif request.method == 'DELETE':
        shift.delete()
        # Return a successful response with HTMX trigger to update the UI
        return HttpResponse(status=204, headers={'HX-Trigger': 'shiftChanged'})
    else:
        form = ShiftForm(instance=shift)
    
    return render(request, 'shift_form.html', {'form': form})

def delete_shift_modal(request, pk):
    shift = get_object_or_404(Shift, pk=pk)
    if request.method == 'DELETE':
        shift.delete()
        # Return a successful response with HTMX trigger to update the UI
        return HttpResponse(status=204, headers={'HX-Trigger': 'shiftChanged'})
    else:
        return HttpResponse(status=405)  # Method Not Allowed if not a DELETE request
    
def shift_list(request):
    return render(request, 'shift_list.html', {
        'shifts': Shift.objects.all(),
    })

def rota_populate(request):
    # Get the start of the week from the URL parameter, if provided
    start_of_week_str = request.GET.get('start_of_week')
    if start_of_week_str:
        # Parse the start_of_week string into a datetime object
        start_of_week = datetime.strptime(start_of_week_str, '%Y/%m/%d')
    else:
        # If start_of_week parameter is not provided, default to the nearest past Monday
        today = datetime.now().date()
        start_of_week = today - timedelta(days=today.weekday())
        

    # Calculate the end date of the week (Sunday)
    end_of_week = start_of_week + timedelta(days=6)
    # Generate the list of dates for the week
    week_calendar_days = [(start_of_week + timedelta(days=i)).strftime("%B %d, %Y") for i in range(7)]
    
    return render(request, 'rota_modal_populate.html', {
        'rota': Rota.objects.all(),
        'week_calendar_days' : week_calendar_days,
    })

def create_shift(request):
    if request.method == 'POST':
        shift_form = ShiftForm(request.POST)
        if shift_form.is_valid():
            # Save the shift
            shift = shift_form.save()

            # Assign the shift to the first employee (you can change this logic)
            employee_assignment = EmployeeAssignment.objects.create(shift=shift, employee=Employee.objects.first())

            return HttpResponse(status=204, headers={'HX-Trigger': 'shiftChanged'})
    else:
        shift_form = ShiftForm()
    return render(request, 'shift_form.html', {'shift_form': shift_form})

def shift_update(request, pk):
    shift = get_object_or_404(Shift, pk=pk)
    if request.method == 'POST':
        form = ShiftForm(request.POST, instance=shift)
        if form.is_valid():
            form.save()
            return redirect('manage_rota')
    else:
        form = ShiftForm(instance=shift)
    return render(request, 'shift_form.html', {'form': form})
    
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

    # Get the start of the week from the URL parameter, if provided
    start_of_week_str = request.GET.get('start_of_week')
    if start_of_week_str:
        # Parse the start_of_week string into a datetime object
        start_of_week = datetime.strptime(start_of_week_str, '%Y/%m/%d')
    else:
        # If start_of_week parameter is not provided, default to the nearest past Monday
        today = datetime.now().date()
        start_of_week = today - timedelta(days=today.weekday())
        

    # Calculate the end date of the week (Sunday)
    end_of_week = start_of_week + timedelta(days=6)
    # Generate the list of dates for the week
    week_calendar_days = [(start_of_week + timedelta(days=i)).strftime("%B %d, %Y") for i in range(7)]
    if request.method == 'POST':
        form = ShiftForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse(status=204, headers={'HX-Trigger': 'rotaChanged'})
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
        'start_of_week': start_of_week,
        'end_of_week': end_of_week,
        'week_calendar_days': week_calendar_days,
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

@require_POST
def update_shift(request):
    if request.method == "POST" and request.headers.get("HTTP_X_REQUESTED_WITH") == "XMLHttpRequest":
        start_time = request.POST.get("startTime")
        end_time = request.POST.get("endTime")
        shift_id = request.POST.get("shiftId")

        try:
            shift = Shift.objects.get(id=shift_id)
            shift.start_time = start_time
            shift.end_time = end_time
            shift.save()
            return JsonResponse({"success": True})
        except Shift.DoesNotExist:
            return JsonResponse({"success": False, "error": "Shift not found."})

    return JsonResponse({"success": False, "error": "Invalid request."})

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

# Start of API calls views----------------------------------------------------
class EmployeeView(APIView):
    def get(self, request):
        queryset = Employee.objects.all()
        serializer = EmployeeSerializer(queryset, many=True)
        return Response(serializer.data)

class EmployeeAssignment(APIView) :
    def get(self, request):
        queryset = Employee.objects.all()
        serializer = EmployeeAssignmentSerializer(queryset, many=True)
        return Response(serializer.data)
    
class RotaView(APIView):
    def get(self, request):
        queryset = Rota.objects.all()
        serializer = RotaSerializer(queryset, many=True)
        return Response(serializer.data)
    
class Shifts(APIView):
    def get(self, request, pk=None):  # Add pk as a parameter
        if pk is not None:
            # Retrieve a specific shift by ID
            shift = get_object_or_404(Shift, pk=pk)
            serializer = ShiftSerializer(shift)
            return Response(serializer.data)
        else:
            # Retrieve all shifts if no ID is provided
            queryset = Shift.objects.all()
            serializer = ShiftSerializer(queryset, many=True)
            return Response(serializer.data)
        
    def put(self, request, pk):
        shift = get_object_or_404(Shift, pk=pk)
        serializer = ShiftSerializer(shift, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            # Print serializer errors to inspect validation issues
            print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UpdateShifts(APIView):
    def post(self, request):
        # Assuming the request data contains the updated shifts
        updated_shifts = request.data.get('shifts', [])
        
        # Example: Updating shifts in the database
        for updated_shift in updated_shifts:
            shift_id = updated_shift.get('id')
            start_time = updated_shift.get('start_time')
            end_time = updated_shift.get('end_time')

            # Retrieve the Shift object from the database
            try:
                shift = Shift.objects.get(id=shift_id)
            except Shift.DoesNotExist:
                return Response({'error': f'Shift with id {shift_id} does not exist'})
            
            # Update the shift times
            shift.start_time = start_time
            shift.end_time = end_time
            shift.save()
        
        return Response({'message': 'Shifts updated successfully'}, status=status.HTTP_200_OK)
    
    class ShiftDetail(APIView):
        def get(self, request, pk):
            # Retrieve the Shift object from the database
            shift = get_object_or_404(Shift, pk=pk)

            # Serialize the Shift object to JSON using ShiftSerializer
            serializer = ShiftSerializer(shift)

            # Return the serialized data as a response
            return Response(serializer.data)

# End of API calls views----------------------------------------------------
