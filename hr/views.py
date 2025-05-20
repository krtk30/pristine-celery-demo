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
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        data = request.data.get("department_ids")
        if data is not None:
            self.override_update_to_force_discrete_add_remove_calls(data, instance)
        return super().update(request, *args, **kwargs)

    def override_update_to_force_discrete_add_remove_calls(self, data, instance):
        new_ids = set(map(int, data))
        old_ids = set(instance.departments.all().values_list("id", flat=True))

        to_add = new_ids - old_ids
        to_del = old_ids - new_ids

        if to_add:
            instance.departments.add(*to_add)   # triggers post_add
        if to_del:
            instance.departments.remove(*to_del)   # triggers post_remove


class DepartmentViewSet(viewsets.ModelViewSet):
    """
    Provides CRUD for Department.
    """
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
