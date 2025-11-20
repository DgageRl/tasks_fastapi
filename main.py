from fastapi import FastAPI
from contextlib import asynccontextmanager
from database import create_tables, delete_tables
from router import router as tasks_router

from prometheus_client import Counter, Histogram, generate_latest, REGISTRY
import time


@asynccontextmanager
async def lifespan(app: FastAPI):
   await delete_tables()
   print("База очищена")
   await create_tables()
   print("База готова к работе")
   yield
   print("Выключение")


# 1. Traffic: Счетчик HTTP запросов
REQUEST_COUNT = Counter(
   'http_requests_total',
   'Total HTTP Requests',
   ['method', 'endpoint', 'status_code']
)

# 2. Latency: Гистограмма длительности запросов
REQUEST_LATENCY = Histogram(
   'http_request_duration_seconds',
   'HTTP Request latency',
   ['method', 'endpoint']
)


# 3. Errors: Будем считать по кодам ответа (4xx, 5xx) из REQUEST_COUNT

@app.before_request
def before_request():
   request.start_time = time.time()


@app.after_request
def after_request(response):
   # Получаем время выполнения запроса
   latency = time.time() - request.start_time
   # Регистрируем метрики
   REQUEST_LATENCY.labels(
      method=request.method,
      endpoint=request.path
   ).observe(latency)

   REQUEST_COUNT.labels(
      method=request.method,
      endpoint=request.path,
      status_code=response.status_code
   ).inc()

   return response


@app.route('/metrics')
def metrics():
   # Prometheus будет забирать метрики по этому эндпоинту
   return generate_latest(REGISTRY)


# Ваши обычные эндпоинты API
@app.route('/api/v1/users')
def get_users():
   # ... ваша логика
   return {"users": []}


app = FastAPI(lifespan=lifespan)
app.include_router(tasks_router)





