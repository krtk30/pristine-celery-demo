# HR Models

## Entity-Relationship Diagram

```plaintext
┌─────────────┐    M2M   ┌─────────────┐
│ Department  │◀────────▶│  Employee   │
│─────────────│          │─────────────│
│ id (PK)     │          │ id (PK)     │
│ name        │          │ name        │
└─────────────┘          │ email (UQ)  │
                         └─────────────┘
```
Field Descriptions

Department

	•	id: Auto-increment primary key
	•	name: CharField(max_length=100) – unique department name

Employee

	•	id: Auto-increment primary key
	•	name: CharField(max_length=100)
	•	email: EmailField(unique=True)
	•	departments: ManyToManyField(Department, related_name="employees")

---