"""
Django admin customization for the HR app, defining admin interfaces for Department and Employee.
"""

from django.contrib import admin
from django.utils.html import format_html

from .models import Department, Employee


class EmployeeInline(admin.TabularInline):
    """Inline through model for Employee-Department relationships."""

    model = Employee.departments.through
    extra = 0
    verbose_name = "Employee"
    verbose_name_plural = "Employees"


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    """
    Advanced admin for Department:
    - List display with employee count
    - Search and filter
    - Inline employees
    """

    list_display = ("id", "name", "employee_count", "view_employees_link")
    search_fields = ("name",)
    list_filter = ("employees",)
    inlines = [EmployeeInline]
    readonly_fields = ("employee_count", "view_employees_link")

    def get_queryset(self, request):
        """Return departments with related employees prefetched for performance."""
        qs = super().get_queryset(request)
        return qs.prefetch_related("employees")

    def employee_count(self, obj):
        """Return the number of employees in this department."""
        return obj.employees.count()

    employee_count.short_description = "Number of Employees"  # type: ignore[attr-defined]

    def view_employees_link(self, obj):
        """Render a link to view all employees in this department."""
        count = obj.employees.count()
        url = f"../employee/?departments__id__exact={obj.id}"
        return format_html('<a href="{}">{}</a>', url, f"View {count} Employees")

    view_employees_link.short_description = "Employees"  # type: ignore[attr-defined]


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    """
    Advanced admin for Employee:
    - List display with departments
    - Search by name/email
    - Filter by departments
    - ManyToMany field horizontal filter
    - Custom actions
    """

    list_display = ("id", "name", "email", "department_list")
    search_fields = ("name", "email")
    list_filter = ("departments",)
    filter_horizontal = ("departments",)

    def get_queryset(self, request):
        """Return employees with related departments prefetched for performance."""
        qs = super().get_queryset(request)
        return qs.prefetch_related("departments")

    def department_list(self, obj):
        """Return comma-separated department names for this employee."""
        names = [d.name for d in obj.departments.all()]
        return ", ".join(names)

    department_list.short_description = "Departments"  # type: ignore[attr-defined]
