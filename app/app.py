from fastapi import FastAPI, Request
from starlette.responses import Response
from prometheus_client import Counter, Summary, Gauge, Histogram, generate_latest, CONTENT_TYPE_LATEST
import time
import random
import psutil
import threading

app = FastAPI()

# Existing metrics
REQUEST_COUNT = Counter('app_requests_total', 'Total de requisições recebidas')
REQUEST_TIME = Summary('app_request_processing_seconds', 'Tempo de processamento das requisições')

# Histogram for response time distribution
REQUEST_DURATION = Histogram(
    'http_request_duration_seconds', 
    'Histogram of request processing time (seconds)',
    buckets=[0.005, 0.01, 0.025, 0.05, 0.075, 0.1, 0.25, 0.5, 0.75, 1, 2.5, 5, 7.5, 10]
)

# New CPU and memory metrics
CPU_PERCENT = Gauge('app_cpu_percent', 'Percentual de uso de CPU pela aplicação')
MEMORY_USAGE = Gauge('app_memory_bytes', 'Uso de memória pela aplicação em bytes')
MEMORY_PERCENT = Gauge('app_memory_percent', 'Percentual de uso de memória pela aplicação')

# System metrics
SYSTEM_CPU_PERCENT = Gauge('system_cpu_percent', 'Percentual de uso de CPU do sistema')
SYSTEM_MEMORY_PERCENT = Gauge('system_memory_percent', 'Percentual de uso de memória do sistema')

# Add disk usage metrics
DISK_USAGE_BYTES = Gauge('system_disk_usage_bytes', 'Uso de disco em bytes')
DISK_FREE_BYTES = Gauge('system_disk_free_bytes', 'Espaço em disco livre em bytes')
DISK_TOTAL_BYTES = Gauge('system_disk_total_bytes', 'Espaço total em disco em bytes')
DISK_USAGE_PERCENT = Gauge('system_disk_usage_percent', 'Percentual de uso de disco')
DISK_FREE_PERCENT = Gauge('system_disk_free_percent', 'Percentual de espaço livre em disco')

def collect_metrics():
    """Background collection of CPU and memory metrics"""
    while True:
        # Application metrics
        process = psutil.Process()
        
        # CPU metrics
        CPU_PERCENT.set(process.cpu_percent())
        SYSTEM_CPU_PERCENT.set(psutil.cpu_percent())
        
        # Memory metrics
        mem_info = process.memory_info()
        MEMORY_USAGE.set(mem_info.rss)  # Resident Set Size in bytes
        MEMORY_PERCENT.set(process.memory_percent())
        SYSTEM_MEMORY_PERCENT.set(psutil.virtual_memory().percent)

        # Disk metrics - add disk metrics collection
        disk = psutil.disk_usage('/')
        DISK_USAGE_BYTES.set(disk.used)
        DISK_FREE_BYTES.set(disk.free)
        DISK_TOTAL_BYTES.set(disk.total)
        DISK_USAGE_PERCENT.set(disk.percent)
        DISK_FREE_PERCENT.set(100 - disk.percent)
        
        time.sleep(1)  # Collect every second

@app.on_event("startup")
def start_metrics_collection():
    # Start metrics collection in a background thread
    thread = threading.Thread(target=collect_metrics, daemon=True)
    thread.start()

@app.middleware("http")
async def monitor_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    request_time = time.time() - start_time
    REQUEST_DURATION.observe(request_time)
    return response

@app.get("/")
def hello():
    REQUEST_COUNT.inc()
    with REQUEST_TIME.time():
        # Simulate work
        time.sleep(random.uniform(0.1, 0.5))
        return "Olá, mundo!"

@app.get("/metrics")
def metrics():
    try:
        output = generate_latest()
        return Response(content=output, media_type=CONTENT_TYPE_LATEST)
    except Exception as e:
        raise