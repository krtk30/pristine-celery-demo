# HR App API Endpoints

```markdown

Base path: `/api/`

| Method | Path                           | Body                                          | Description                             |
|--------|--------------------------------|-----------------------------------------------|-----------------------------------------|
| GET    | `/employees/`                  | —                                             | List all employees                      |
| POST   | `/employees/`                  | `{ name, email, department_ids: [1,2,…] }`    | Create new employee                     |
| GET    | `/employees/{id}/`             | —                                             | Retrieve employee details               |
| PUT    | `/employees/{id}/`             | `{ name, email, department_ids: […] }`        | Replace employee & M2M                  |
| PATCH  | `/employees/{id}/`             | Partial fields + `department_ids`             | Update employee or M2M membership       |
| DELETE | `/employees/{id}/`             | —                                             | Delete employee                         |
| GET    | `/departments/`                | —                                             | List all departments                    |
| POST   | `/departments/`                | `{ name }`                                    | Create new department                   |
| GET    | `/departments/{id}/`           | —                                             | Retrieve department                     |
| PUT    | `/departments/{id}/`           | `{ name }`                                    | Rename department                       |
| DELETE | `/departments/{id}/`           | —                                             | Delete department                       |
| GET    | `/departments/{id}/employees/` | —                                             | List all employees in the specified department |
| GET    | `/employees/{id}/departments/` | —                                             | List all departments for the specified employee |

```

### Example

```bash
curl -X PUT http://localhost:8000/api/employees/1/ \
  -H "Content-Type: application/json" \
  -d '{"name":"Karthik","email":"krtk@example.com","department_ids":[2,4]}'

# List employees in department 1
curl http://localhost:8000/api/departments/1/employees/

# List departments for employee 1
curl http://localhost:8000/api/employees/1/departments/
```