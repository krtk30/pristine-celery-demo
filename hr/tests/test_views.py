"""
Test suite for Department and Employee API endpoints.
"""

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from hr.models import Department, Employee


class DepartmentAPITestCase(APITestCase):
    """
    Tests for Department CRUD using Django REST Framework APITestCase.
    """

    @classmethod
    def setUpTestData(cls):
        """Set up initial Departments for tests."""
        cls.dept1 = Department.objects.create(name="HR")
        cls.dept2 = Department.objects.create(name="Finance")
        cls.list_url = reverse("department-list")

    def test_list_departments(self):
        """Ensure listing departments returns correct data and structure."""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Expect two departments
        self.assertEqual(len(response.data), 2)
        names = {d["name"] for d in response.data}
        self.assertSetEqual(names, {"HR", "Finance"})

    def test_retrieve_department(self):
        """Ensure retrieving an existing department returns 200 and correct data."""
        url = reverse("department-detail", args=[self.dept1.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], self.dept1.pk)
        self.assertEqual(response.data["name"], self.dept1.name)

    def test_retrieve_nonexistent_department(self):
        """Ensure retrieving a non-existent department returns 404."""
        url = reverse("department-detail", args=[999])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_department(self):
        """Ensure creating a department via POST returns 201 and the department is stored."""
        payload = {"name": "Legal"}
        response = self.client.post(self.list_url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Department.objects.filter(name="Legal").exists())

    def test_create_department_missing_name(self):
        """Ensure creating a department without a name returns 400 and error message."""
        response = self.client.post(self.list_url, {}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("name", response.data)

    def test_update_department(self):
        """Ensure updating an existing department returns 200 and updates the name."""
        url = reverse("department-detail", args=[self.dept2.pk])
        payload = {"name": "Operations"}
        response = self.client.put(url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.dept2.refresh_from_db()
        self.assertEqual(self.dept2.name, "Operations")

    def test_update_nonexistent_department(self):
        """Ensure updating a non-existent department returns 404."""
        url = reverse("department-detail", args=[999])
        payload = {"name": "X"}
        response = self.client.put(url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_department(self):
        """Ensure deleting an existing department returns 204 and removes the record."""
        url = reverse("department-detail", args=[self.dept2.pk])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Department.objects.filter(pk=self.dept2.pk).exists())

    def test_delete_nonexistent_department(self):
        """Ensure deleting a non-existent department returns 404."""
        url = reverse("department-detail", args=[999])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class EmployeeAPITestCase(APITestCase):
    """
    Tests for Employee CRUD and M2M batch update using APITestCase.
    """

    @classmethod
    def setUpTestData(cls):
        """Set up initial Employee and Departments for tests."""
        cls.dep1 = Department.objects.create(name="HR")
        cls.dep2 = Department.objects.create(name="Finance")
        cls.employee = Employee.objects.create(name="Alice", email="alice@example.com")
        cls.employee.departments.set([cls.dep1.pk])
        cls.list_url = reverse("employee-list")

    def test_list_employees(self):
        """Ensure listing employees returns correct data and structure."""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        emp = response.data[0]
        self.assertEqual(emp["id"], self.employee.pk)
        self.assertEqual(emp["name"], "Alice")
        self.assertEqual(emp["email"], "alice@example.com")
        self.assertEqual(emp["departments"], [{"id": self.dep1.pk, "name": "HR"}])

    def test_create_employee(self):
        """
        Ensure creating an employee with valid data returns 201 and
        associates departments correctly.
        """
        payload = {
            "name": "Bob",
            "email": "bob@example.com",
            "department_ids": [self.dep2.pk],
        }
        response = self.client.post(self.list_url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        bob = Employee.objects.get(email="bob@example.com")
        self.assertIn(self.dep2, bob.departments.all())

    def test_create_employee_missing_fields(self):
        """Ensure creating an employee without department_ids returns 400 and error message."""
        # Missing department_ids
        payload = {"name": "NoDeps", "email": "nodeps@example.com"}
        response = self.client.post(self.list_url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("department_ids", response.data)

    def test_create_employee_invalid_email(self):
        """Ensure creating an employee with an invalid email returns 400."""
        payload = {"name": "X", "email": "invalid", "department_ids": [self.dep1.pk]}
        response = self.client.post(self.list_url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("email", response.data)

    def test_create_employee_duplicate_email(self):
        """Ensure creating an employee with an existing email returns 400."""
        payload = {
            "name": "AliceDup",
            "email": "alice@example.com",
            "department_ids": [self.dep1.pk],
        }
        response = self.client.post(self.list_url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("email", response.data)

    def test_retrieve_employee(self):
        """Ensure retrieving an existing employee returns correct data."""
        url = reverse("employee-detail", args=[self.employee.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], self.employee.pk)
        self.assertEqual(
            response.data["departments"], [{"id": self.dep1.pk, "name": "HR"}]
        )

    def test_retrieve_nonexistent_employee(self):
        """Ensure retrieving a non-existent employee returns 404."""
        url = reverse("employee-detail", args=[999])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_employee_departments_batch(self):
        """Ensure batch update of employee departments works correctly."""
        url = reverse("employee-detail", args=[self.employee.pk])
        payload = {
            "name": "Alice",
            "email": "alice@example.com",
            "department_ids": [self.dep2.pk],
        }
        response = self.client.put(url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.employee.refresh_from_db()
        dept_pks = list(self.employee.departments.values_list("pk", flat=True))
        self.assertListEqual(dept_pks, [self.dep2.pk])

    def test_update_employee_invalid_department_ids(self):
        """Ensure updating with invalid department IDs returns 400."""
        url = reverse("employee-detail", args=[self.employee.pk])
        payload = {
            "name": "Alice",
            "email": "alice@example.com",
            "department_ids": [999],
        }
        response = self.client.put(url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("department_ids", response.data)

    def test_partial_update_employee(self):
        """Ensure partial update of departments via PATCH works correctly."""
        url = reverse("employee-detail", args=[self.employee.pk])
        payload = {"department_ids": [self.dep2.pk]}
        response = self.client.patch(url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.employee.refresh_from_db()
        self.assertListEqual(
            list(self.employee.departments.values_list("pk", flat=True)), [self.dep2.pk]
        )

    def test_delete_employee(self):
        """Ensure deleting an employee via the API returns 204 and removes the record."""
        url = reverse("employee-detail", args=[self.employee.pk])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Employee.objects.filter(pk=self.employee.pk).exists())

    def test_filter_employees_by_department(self):
        """Ensure filtering by department returns only matching employees."""
        # Create second employee in dep2
        emp2 = Employee.objects.create(name="Carl", email="carl@example.com")
        emp2.departments.set([self.dep2.pk])
        url = f"{self.list_url}" f"?departments__id__exact={self.dep2.pk}"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        ids = {e["id"] for e in response.data}
        self.assertSetEqual(ids, {emp2.pk})
