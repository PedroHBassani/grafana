from fastapi import FastAPI
from starlette.responses import Response
from prometheus_client import Counter, Summary, Gauge, generate_latest, CONTENT_TYPE_LATEST
import time
import random
import psutil
import threading

app = FastAPI()

# Existing metrics
REQUEST_COUNT = Counter('app_requests_total', 'Total de requisições recebidas')
REQUEST_TIME = Summary('app_request_processing_seconds', 'Tempo de processamento das requisições')

# New CPU and memory metrics
CPU_PERCENT = Gauge('app_cpu_percent', 'Percentual de uso de CPU pela aplicação')
MEMORY_USAGE = Gauge('app_memory_bytes', 'Uso de memória pela aplicação em bytes')
MEMORY_PERCENT = Gauge('app_memory_percent', 'Percentual de uso de memória pela aplicação')

# System metrics
SYSTEM_CPU_PERCENT = Gauge('system_cpu_percent', 'Percentual de uso de CPU do sistema')
SYSTEM_MEMORY_PERCENT = Gauge('system_memory_percent', 'Percentual de uso de memória do sistema')

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
        
        time.sleep(1)  # Collect every second

@app.on_event("startup")
def start_metrics_collection():
    # Start metrics collection in a background thread
    thread = threading.Thread(target=collect_metrics, daemon=True)
    thread.start()

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