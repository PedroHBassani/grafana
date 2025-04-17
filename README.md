# Monitoramento com FastAPI, Prometheus e Grafana

Este projeto demonstra como configurar um sistema de monitoramento usando FastAPI, Prometheus e Grafana em contêineres Docker.

## Pré-requisitos

- [Docker](https://www.docker.com/products/docker-desktop) instalado
- [Docker Compose](https://docs.docker.com/compose/install/) instalado

## Estrutura do Projeto

```
grafana/
├── app/
│   ├── app.py            # Aplicação FastAPI
│   ├── Dockerfile        # Dockerfile para a aplicação
│   └── requirements.txt  # Dependências Python
├── docker-compose.yml    # Configuração dos serviços
├── prometheus.yml        # Configuração do Prometheus
└── README.md             # Este arquivo
```

## Como Executar

1. Clone o repositório ou extraia os arquivos para sua máquina local.

2. Navegue até o diretório do projeto:
   ```bash
   cd grafana
   ```
3. Reconstrua os contêineres:
    ```bash
    docker-compose build
    ```

3. Inicie os contêineres com Docker Compose:
   ```bash
   docker-compose up -d
   ```

4. Verifique se os contêineres estão em execução:
   ```bash
   docker-compose ps
   ```

## Acessando os Serviços

- **FastAPI**: [http://localhost:8000](http://localhost:8000)
  - Endpoint de métricas: [http://localhost:8000/metrics](http://localhost:8000/metrics)

- **Prometheus**: [http://localhost:9090](http://localhost:9090)
  - Use a interface web para consultar métricas

- **Grafana**: [http://localhost:3000](http://localhost:3000)
  - Usuário: `admin`
  - Senha: `admin`

## Configuração do Grafana

1. Acesse o Grafana em [http://localhost:3000](http://localhost:3000)
2. Faça login com as credenciais padrão (admin/admin)
3. Configure uma fonte de dados Prometheus:
   - Vá para Configuração (engrenagem) > Data Sources > Add data source
   - Selecione "Prometheus"
   - URL: `http://prometheus:9090` - A url funcionará por estar dentro do mesmo container.
   - Clique em "Save & Test"

4. Importe um dashboard:
   - Vá para Create (ícone +) > Import
   - Use o ID 10427 para um dashboard FastAPI ou faça upload do JSON do dashboard fornecido

## Parando os Serviços

Para parar todos os contêineres:
```bash
docker-compose down
```

Para parar e remover todos os dados (volumes):
```bash
docker-compose down -v
```

## Resolução de Problemas

Se encontrar problemas ao executar o projeto:

1. Verifique os logs dos contêineres:
   ```bash
   docker-compose logs
   ```

2. Para ver logs de um serviço específico:
   ```bash
   docker-compose logs app
   docker-compose logs prometheus
   docker-compose logs grafana
   ```

3. Certifique-se de que todas as portas necessárias (8000, 9090, 3000) estão disponíveis no seu sistema.

# Grafana Monitoring System

This repository contains a Grafana monitoring dashboard configuration and scripts for monitoring a Python FastAPI application with Prometheus.

## Components

- `grafana.json`: Grafana dashboard configuration
- `app/`: Python FastAPI application with Prometheus metrics
- `load_test.py`: Script to generate load on the API for testing

## Dashboard Import Instructions

When importing the dashboard into Grafana:

1. Go to Dashboards > Import
2. Upload the JSON file or paste the JSON content
3. Select the Prometheus data source
4. Click Import

## Using the Load Testing Tool

The `load_test.py` script can generate artificial load on your API to test monitoring.

### Basic Usage:

```bash
# Test with 1000 requests at 10 requests per second
python ./test/load_test.py --url http://localhost:8000 --requests 1000 --rate 10

# Run a test for 5 minutes (300 seconds)
python ./test/load_test.py --url http://localhost:8000 --duration 300 --rate 10

# Run with 5 concurrent requests at 20 requests/second
python ./test/load_test.py --url http://localhost:8000 --duration 60 --rate 20 --concurrent 5
```

### Parameters:

- `--url`: The API endpoint to test (default: http://localhost:8000)
- `--requests`: Total number of requests to send
- `--duration`: How long to run the test in seconds
- `--rate`: Request rate per second (default: 10)
- `--concurrent`: Number of concurrent requests (default: 1)

Note: You must specify either `--requests` or `--duration`.

## Handling "Dashboard Changed" Errors

If you encounter a "Failed to save dashboard - The dashboard has been changed by someone else" error:

1. **Option 1**: Use the "overwrite" feature
   - In the dashboard JSON, ensure the "overwrite" property is set to true
   - This allows the dashboard to override existing versions with the same UID

2. **Option 2**: Update the version number
   - Increment the "version" field in the JSON
   - This tells Grafana this is a newer version of the dashboard

3. **Option 3**: Use a new UID
   - Change the "uid" field to a new unique identifier
   - This will create a new dashboard instead of updating the existing one

## Best Practice

Always pull the latest version of the dashboard before making changes to avoid conflicts.