# pylint: disable=too-many-ancestors, unused-argument
"""
Django REST Framework viewsets for Employee and Department CRUD APIs.
"""
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Department, Employee
from .serializers import DepartmentSerializer, EmployeeSerializer


class EmployeeViewSet(viewsets.ModelViewSet):
    """
    Provides CRUD for Employee along with department linkage,
    GET shows department details; POST/PUT accepts department IDs.

    Plus an extra endpoint:
      GET /api/employees/{pk}/departments/  → list departments of this employee
    """

    serializer_class = EmployeeSerializer

    def get_queryset(self):
        # Base queryset with prefetch for performance
        qs = Employee.objects.prefetch_related("departments").all()
        # Optional filter by department ID (supports ?departments__id__exact=<id>)
        if dept_id := self.request.query_params.get("departments__id__exact", None):
            qs = qs.filter(departments__id=dept_id)
        return qs

    @action(detail=True, methods=["get"])
    def departments(self, request, pk=None):
        """Return a list of departments this employee belongs to."""
        emp = self.get_object()
        qs = emp.departments.all()
        serializer = DepartmentSerializer(qs, many=True, context={"request": request})
        return Response(serializer.data)


class DepartmentViewSet(viewsets.ModelViewSet):
    """
    Provides CRUD for Department, plus an extra endpoint:
      GET /api/departments/{pk}/employees/  → list employees in this dept
    """

    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer

    @action(detail=True, methods=["get"])
    def employees(self, request, pk=None):
        """Return a list of employees belonging to this department."""
        dept = self.get_object()
        qs = dept.employees.all()
        serializer = EmployeeSerializer(qs, many=True, context={"request": request})
        return Response(serializer.data)
