"""
Test suite for Department and Employee admin customizations.
"""

# pylint: disable=missing-function-docstring, too-few-public-methods

# pylint: disable=invalid-name

from django.contrib.admin.sites import AdminSite
from django.test import RequestFactory, TestCase
from django.utils.html import escape

from hr.admin import DepartmentAdmin, EmployeeAdmin, EmployeeInline
from hr.models import Department, Employee


class MockRequest:
    """Simple mock request with GET params."""

    def __init__(self, GET=None):
        self.GET = GET or {}


class AdminMixin:
    """Provide a fresh AdminSite and request factory for tests."""

    def setUp(self):
        self.site = AdminSite()
        self.factory = RequestFactory()


class DepartmentAdminTests(AdminMixin, TestCase):
    """Test DepartmentAdmin configuration and helper methods."""

    def setUp(self):
        super().setUp()
        # Register admin
        self.admin = DepartmentAdmin(Department, self.site)
        # Create sample data
        self.dep = Department.objects.create(name="Engineering")
        self.emp1 = Employee.objects.create(name="Alice", email="alice@example.com")
        self.emp2 = Employee.objects.create(name="Bob", email="bob@example.com")
        self.dep.employees.set([self.emp1.pk, self.emp2.pk])

    def test_list_display(self):
        """Ensure list_display matches expected fields."""
        self.assertEqual(
            self.admin.list_display,
            ("id", "name", "employee_count", "view_employees_link"),
        )

    def test_search_fields(self):
        """Ensure search_fields contains only 'name'."""
        self.assertEqual(self.admin.search_fields, ("name",))

    def test_list_filter(self):
        """Ensure list_filter includes 'employees'."""
        self.assertEqual(self.admin.list_filter, ("employees",))

    def test_inlines(self):
        """Ensure EmployeeInline is present in inlines."""
        self.assertIn(EmployeeInline, self.admin.inlines)

    def test_readonly_fields(self):
        """Ensure readonly_fields include employee_count and view_employees_link."""
        self.assertIn("employee_count", self.admin.readonly_fields)
        self.assertIn("view_employees_link", self.admin.readonly_fields)

    def test_employee_count(self):
        """Ensure employee_count returns correct number of employees."""
        count = self.admin.employee_count(self.dep)
        self.assertEqual(count, 2)

    def test_view_employees_link(self):
        """Ensure view_employees_link returns correct HTML link."""
        html = self.admin.view_employees_link(self.dep)
        url = f"../employee/?departments__id__exact={self.dep.id}"
        self.assertIn(escape(url), html)
        self.assertIn("View 2 Employees", html)


class EmployeeAdminTests(AdminMixin, TestCase):
    """Test EmployeeAdmin configuration and helper methods."""

    def setUp(self):
        super().setUp()
        self.admin = EmployeeAdmin(Employee, self.site)
        self.dep = Department.objects.create(name="HR")
        self.emp = Employee.objects.create(name="Charlie", email="charlie@example.com")
        self.emp.departments.set([self.dep.pk])

    def test_list_display(self):
        """Ensure list_display matches expected fields."""
        self.assertEqual(
            self.admin.list_display, ("id", "name", "email", "department_list")
        )

    def test_search_fields(self):
        """Ensure search_fields contains name and email."""
        self.assertEqual(self.admin.search_fields, ("name", "email"))

    def test_list_filter(self):
        """Ensure list_filter includes departments."""
        self.assertEqual(self.admin.list_filter, ("departments",))

    def test_filter_horizontal(self):
        """Ensure filter_horizontal includes departments."""
        self.assertEqual(self.admin.filter_horizontal, ("departments",))

    def test_department_list(self):
        """Ensure department_list returns comma-separated department names."""
        result = self.admin.department_list(self.emp)
        self.assertEqual(result, self.dep.name)
