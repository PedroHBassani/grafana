from flask import Flask
from prometheus_client import Counter, Summary, generate_latest
import time
import random

app = Flask(__name__)

REQUEST_COUNT = Counter('app_requests_total', 'Total de requisições recebidas')
REQUEST_TIME = Summary('app_request_processing_seconds', 'Tempo de processamento das requisições')

@app.route("/")
@REQUEST_TIME.time()
def hello():
    REQUEST_COUNT.inc()
    time.sleep(random.uniform(0.1, 0.5))
    return "Olá, mundo!"

@app.route("/metrics")
def metrics():
    return generate_latest(), 200, {'Content-Type': 'text/plain'}