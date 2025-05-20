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
        cls.dept1 = Department.objects.create(name='HR')
        cls.dept2 = Department.objects.create(name='Finance')
        cls.list_url = reverse('department-list')

    def test_list_departments(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Expect two departments
        self.assertEqual(len(response.data), 2)
        names = {d['name'] for d in response.data}
        self.assertSetEqual(names, {'HR', 'Finance'})

    def test_retrieve_department(self):
        url = reverse('department-detail', args=[self.dept1.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.dept1.pk)
        self.assertEqual(response.data['name'], self.dept1.name)

    def test_create_department(self):
        payload = {'name': 'Legal'}
        response = self.client.post(self.list_url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Department.objects.filter(name='Legal').exists())

    def test_update_department(self):
        url = reverse('department-detail', args=[self.dept2.pk])
        payload = {'name': 'Operations'}
        response = self.client.put(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.dept2.refresh_from_db()
        self.assertEqual(self.dept2.name, 'Operations')

    def test_delete_department(self):
        url = reverse('department-detail', args=[self.dept2.pk])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Department.objects.filter(pk=self.dept2.pk).exists())


class EmployeeAPITestCase(APITestCase):
    """
    Tests for Employee CRUD and M2M batch update using APITestCase.
    """
    @classmethod
    def setUpTestData(cls):
        cls.dep1 = Department.objects.create(name='HR')
        cls.dep2 = Department.objects.create(name='Finance')
        cls.employee = Employee.objects.create(
            name='Alice', email='alice@example.com'
        )
        cls.employee.departments.set([cls.dep1.pk])
        cls.list_url = reverse('employee-list')

    def test_list_employees(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # One employee exists
        self.assertEqual(len(response.data), 1)
        emp = response.data[0]
        self.assertEqual(emp['id'], self.employee.pk)
        self.assertEqual(emp['name'], 'Alice')
        self.assertEqual(emp['email'], 'alice@example.com')
        # Check nested departments
        self.assertEqual(emp['departments'], [{'id': self.dep1.pk, 'name': 'HR'}])

    def test_create_employee(self):
        payload = {
            'name': 'Bob',
            'email': 'bob@example.com',
            'department_ids': [self.dep2.pk]
        }
        response = self.client.post(self.list_url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        bob = Employee.objects.get(email='bob@example.com')
        self.assertIn(self.dep2, bob.departments.all())

    def test_retrieve_employee(self):
        url = reverse('employee-detail', args=[self.employee.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.employee.pk)
        self.assertEqual(response.data['departments'], [{'id': self.dep1.pk, 'name': 'HR'}])

    def test_update_employee_departments_batch(self):
        url = reverse('employee-detail', args=[self.employee.pk])
        payload = {
            'name': 'Alice',
            'email': 'alice@example.com',
            'department_ids': [self.dep2.pk]
        }
        response = self.client.put(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.employee.refresh_from_db()
        # Only dep2 now
        dept_pks = list(self.employee.departments.values_list('pk', flat=True))
        self.assertListEqual(dept_pks, [self.dep2.pk])

    def test_delete_employee(self):
        url = reverse('employee-detail', args=[self.employee.pk])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Employee.objects.filter(pk=self.employee.pk).exists())
