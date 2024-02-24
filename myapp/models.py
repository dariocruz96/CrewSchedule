from django.db import models

class Employee(models.Model):
    firstName = models.CharField(max_length=50)
    lastName = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)  # Hashed password
    # Add other fields as needed
    class Meta:
        db_table = 'employee'
