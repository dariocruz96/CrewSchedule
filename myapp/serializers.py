from rest_framework import serializers
from .models import Employee, Shift, Rota, EmployeeShift, EmployeeAssignment

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = '__all__'

class ShiftSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shift
        fields = '__all__'

class RotaSerializer(serializers.ModelSerializer):
    employee = EmployeeSerializer()  # Use EmployeeSerializer for nested employee data
    shift = ShiftSerializer()
    class Meta:
        model = Rota
        fields = ['id', 'date_assigned', 'employee', 'shift']

class EmployeeShiftSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeShift
        fields = '__all__'

class EmployeeAssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeAssignment
        fields = '__all__'
