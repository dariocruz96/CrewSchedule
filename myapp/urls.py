"""
URL configuration for CrewSchedule project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from . import views
urlpatterns = [
    path('', views.home_view, name='home'),
    path('login/', views.login_view, name='login'),
    path('manage-users/', views.manage_users_view, name='manage_users'),
    path('manage-shifts/create-shift-modal/', views.create_shift_modal, name='create_shift_modal'),
    path('manage-shifts/edit-shift/<int:pk>/', views.edit_shift_modal, name='edit_shift_modal'),
    path('manage-shifts/delete-shift/<int:pk>', views.delete_shift_modal, name='delete_shift_modal'),
    path('shifts/', views.shift_list, name='shift_list'),
    path('manage-rota/', views.manage_rota_view, name='manage_rota'),
    path('manage-shifts/', views.manage_shifts_view, name='manage_shifts'),
    path('manage-shifts/<int:pk>/edit/', views.shift_update, name='shift_update'),
    path('employees/', views.employee_list, name='employee_list'),
    path('employee/<int:pk>/', views.employee_detail, name='employee_detail'),
    path('employee/new/', views.employee_create, name='employee_create'),
    path('employee/<int:pk>/edit/', views.employee_update, name='employee_update'),
    path('employee/<int:pk>/delete/', views.employee_delete, name='employee_delete'),
    path('assign-employee/<int:shift_id>/', views.assign_employee, name='assign_employee'),
    path('success_page', views.manage_rota_view, name='success_page'),
    path('test-add-to-schedule/', views.test_add_to_schedule, name='test_add_to_schedule'),
    path('api/employee/', views.EmployeeView.as_view(), name='employee-list'),
    path('api/rota/', views.RotaView.as_view(), name='rota'),
    path('api/update-shifts/', views.UpdateShifts.as_view(), name='update-shifts'),
    path('api/shifts/<int:pk>/', views.Shifts.as_view(), name='shift-detail'),
    path('api/shifts/', views.Shifts.as_view(), name='shifts'),
    path('api/shifts-assigned/', views.EmployeeAssignment.as_view(), name='shifts-assigned'),
    path("manage-rota/update_shift/", views.update_shift, name="update_shift"),
]