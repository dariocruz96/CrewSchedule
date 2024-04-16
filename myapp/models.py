from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Employee(models.Model):
    firstName = models.CharField(max_length=50, verbose_name='First Name')
    lastName = models.CharField(max_length=50, verbose_name='Last Name')
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)  # Hashed password
    # Add other fields as needed
    class Meta:
        db_table = 'employee'

    def __str__(self):
        return f"{self.firstName} {self.lastName}"

class Shift(models.Model):

    DAY_CHOICES = [
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
        ('Sunday', 'Sunday'),
    ]
    start_time = models.TimeField()
    end_time = models.TimeField()
    date = models.DateField()

    class Meta:
        db_table = 'shift'

    def __str__(self):
        return f"{self.date} - {self.start_time} to {self.end_time}"
    
class Rota(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    shift = models.ForeignKey(Shift, on_delete=models.CASCADE)
    date_assigned = models.DateField(default=timezone.now)
    
    class Meta:
        db_table = 'rota'

class EmployeeShift(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    shift = models.ForeignKey(Shift, on_delete=models.CASCADE)
    is_assigned = models.BooleanField(default=False)

    class Meta:
        db_table = 'employee_shift'

class EmployeeAssignment(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    shift = models.ForeignKey(Shift, on_delete=models.CASCADE)
    date_assigned = models.DateField(default=timezone.now)

    class Meta:
        db_table = 'employee_assignment'