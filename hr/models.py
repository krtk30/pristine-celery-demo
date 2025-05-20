from django.db import models

class Department(models.Model):
    """
    Represents a department in the organization.
        Departments have a unique name, which is indexed for efficient lookups.
    """
    name = models.CharField(max_length=100, unique=True, db_index=True)

    def __str__(self):
        return self.name


class Employee(models.Model):
    """
    Represents an employee in the organization.
        Employees have a name, a unique email (indexed for lookups), and can belong to multiple departments.
    """
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True, db_index=True)
    departments = models.ManyToManyField(Department, related_name='employees')

    def __str__(self):
        return self.name