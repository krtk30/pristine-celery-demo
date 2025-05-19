# 🧩 Pristine Celery Demo

A production-ready Django 5.0.8 project using **Celery**, **Redis**, and **Poetry**, showcasing:

- Task queueing and execution via Redis
- Retry logic with `acks_late=True`
- Monitoring via Flower
- Chained task pipelines for real-world workflows
- Structured logging with task lifecycle visibility

---

## 🏗 Project Structure
```
pristine-celery-demo/
├── celery_demo/         # Django app with Celery tasks
├── pristine/            # Django settings and celery app
├── manage.py
├── pyproject.toml       # Poetry config
└── README.md
```


## ⚙️ Setup Instructions

### 1. Clone the Repo

```bash
git clone https://github.com/<your-username>/pristine-celery-demo.git
cd pristine-celery-demo
```

### 2. Install Dependencies via Poetry

```bash
poetry install
```

### 3. Setup Redis (Docker)

```bash
docker run -d -p 6379:6379 redis
```
## 🚀 Run the Application

### 1. Start Django Server
```bash
poetry run python manage.py migrate
poetry run python manage.py runserver
```

### 2. Start Celery Worker
```bash
poetry run celery -A pristine worker --loglevel=info
```
You'll see logs like:
```angular2html
[2025-05-19 12:34:56] [INFO] [celery_demo] [a1b2c3d4] Task slow_add triggered with args: x=3, y=5
[2025-05-19 12:34:58] [WARNING] [celery_demo] [a1b2c3d4] Task failed: Simulated failure, retrying...
[2025-05-19 12:35:04] [INFO] [celery_demo] [a1b2c3d4] Task completed successfully: 3 + 5 = 8
```
When you run:
```bash
celery -A pristine worker --loglevel=info
```
Celery spawns worker processes (or threads) that:
#### 1. Connect to the Redis broker
#### 2. Poll for messages from the task queue
#### 3. Deserialize the job payload
#### 4. Load the task by name from registered apps
#### 5. Run the task in memory
#### 6. Capture output and exceptions

### 3. Start Flower Dashboard
```bash
poetry run celery -A pristine flower --port=5555 --basic_auth=<username>:<password>
```
Access it at: http://localhost:5555

You’ll see:

	•	Active tasks
	•	Queued tasks
	•	Retries
	•	Worker logs


## 🧪 Task Execution
    •	Task runs in a worker subprocess/thread.
	•	If it succeeds → result is stored in Redis result backend.
	•	If it fails → retried (if configured) or marked as failed.
### Single task
```bash
poetry run python manage.py shell
>>> from celery_demo.tasks import slow_add
>>> result = slow_add.delay(3, 7)
>>> result.get(propagate=False)
```
In the worker logs

```bash
[2025-05-19 16:20:17,284: INFO/MainProcess] Events of group {task} enabled by remote.
[2025-05-19 16:20:51,296: INFO/MainProcess] Task celery_demo.tasks.slow_add[4e70b858-16c1-487b-9777-fbd756514e6b] received
[2025-05-19 16:20:51,298] [INFO] [celery_demo] [4e70b858-16c1-487b-9777-fbd756514e6b] Task slow_add triggered with args: x=3, y=7
[2025-05-19 16:20:51,298: INFO/ForkPoolWorker-8] [4e70b858-16c1-487b-9777-fbd756514e6b] Task slow_add triggered with args: x=3, y=7
[2025-05-19 16:20:53,301] [INFO] [celery_demo] [4e70b858-16c1-487b-9777-fbd756514e6b] Task completed successfully: 3 + 7 = 10
[2025-05-19 16:20:53,301: INFO/ForkPoolWorker-8] [4e70b858-16c1-487b-9777-fbd756514e6b] Task completed successfully: 3 + 7 = 10
[2025-05-19 16:20:53,313: INFO/ForkPoolWorker-8] Task celery_demo.tasks.slow_add[4e70b858-16c1-487b-9777-fbd756514e6b] succeeded in 2.0159977909643203s: 10

```
### Chained task
A chained Celery task is used when you have a series of dependent tasks where each task’s output becomes the input for the next, forming a workflow or pipeline.

```bash
poetry run python manage.py shell
```

```python
from celery import chain
from celery_demo.tasks import slow_add, multiply, subtract

chain_result = chain(slow_add.s(2, 3), multiply.s(), subtract.s())()
print("Task ID:", chain_result.id)
```