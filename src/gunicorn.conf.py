from os import cpu_count, environ

bind = f"0.0.0.0:{environ.get('APP_PORT', '8000')}"
worker_class = "uvicorn.workers.UnicornWorker"
max_requests = 1000

number_cpu = cpu_count()
if number_cpu:
    number_workers = number_cpu // 2 + 1
else:
    number_workers = 1

workers = int(environ.get("APP_WORKERS", number_workers))
