"""
Serializers module for the HR app, defining Department and Employee serializers.
"""

from rest_framework import serializers

from .models import Department, Employee


class DepartmentSerializer(serializers.ModelSerializer):
    """
    Serializes Department instances.
        This serializer handles the serialization of Department objects.
    """

    class Meta:
        model = Department
        fields = ["id", "name"]


class EmployeeSerializer(serializers.ModelSerializer):
    """
    Serializes Employee instances.
        This serializer handles the serialization of Employee objects, including
        nested serialization of related departments and a custom message field.

        GET → departments with id+name
            POST/PUT → department_ids with just the IDs
    """

    departments = DepartmentSerializer(many=True, read_only=True)
    department_ids = serializers.PrimaryKeyRelatedField(
        queryset=Department.objects.all(),
        many=True,
        write_only=True,
        source="departments",
    )
    message = serializers.SerializerMethodField()

    class Meta:
        model = Employee
        fields = ["id", "name", "email", "departments", "department_ids", "message"]

    def get_message(self, obj):
        """
        Generates a message indicating the number of associated departments.
            Args:
                obj: The Employee instance.
            Returns:
                A string message.
        """
        return f"{obj.name} is associated with {obj.departments.count()} department(s)."
