# HR App Setup

## 1. Ensure Dependencies

```bash
poetry install
```
---
## 2. Migrate & Seed

```bash
poetry run python manage.py migrate
# Create some departments
poetry run python manage.py shell
>>> from hr.models import Department
>>> for name in ["Finance","HR","Ops"]: Department.objects.create(name=name)
>>> exit()
```
---
## 3. Prepare Log Directory
```bash
mkdir -p logs
chmod 755 logs
cd logs
touch hr.log
```
---
## 4. Run Services
### 1. Django Server
```bash
poetry run python manage.py runserver
```
### 2. Celery Worker
```bash
poetry run celery -A pristine worker --loglevel=info
```
### 3. Flower
```bash
poetry run celery -A pristine flower --port=5555
```
---