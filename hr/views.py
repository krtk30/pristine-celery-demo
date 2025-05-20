from rest_framework import viewsets
from .models import Employee, Department
from .serializers import EmployeeSerializer, DepartmentSerializer


class EmployeeViewSet(viewsets.ModelViewSet):
    """
    Provides CRUD for Employee along with department linkage.
    GET shows department details; POST/PUT accepts department IDs.
    """
    queryset = Employee.objects.prefetch_related("departments").all()
    serializer_class = EmployeeSerializer
    

class DepartmentViewSet(viewsets.ModelViewSet):
    """
    Provides CRUD for Department.
    """
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
