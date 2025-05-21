# pylint: disable=too-many-ancestors
"""
Django REST Framework viewsets for Employee and Department CRUD APIs.
"""
from rest_framework import viewsets

from .models import Department, Employee
from .serializers import DepartmentSerializer, EmployeeSerializer


class EmployeeViewSet(viewsets.ModelViewSet):
    """
    Provides CRUD for Employee along with department linkage.
    GET shows department details; POST/PUT accepts department IDs.
    """

    serializer_class = EmployeeSerializer

    def get_queryset(self):
        # Base queryset with prefetch for performance
        qs = Employee.objects.prefetch_related("departments").all()
        # Optional filter by department ID (supports ?departments__id__exact=<id>)
        if dept_id := self.request.query_params.get("departments__id__exact", None):
            qs = qs.filter(departments__id=dept_id)
        return qs


class DepartmentViewSet(viewsets.ModelViewSet):
    """
    Provides CRUD for Department.
    """

    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
