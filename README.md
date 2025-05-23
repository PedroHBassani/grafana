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
│   └── requirements.txt  # Dependências Python - App
├── test/
│   └── load_test.py      # Script de teste de carga
│   └── requirements.txt  # Dependências Python - Test
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
   - Vá para Conexões (engrenagem) > Data Sources > Add new data source
   - Selecione "Prometheus"
   - URL: `http://prometheus:9090` - A url funcionará por estar dentro do mesmo container.
   - Clique em "Save & Test"

4. Importe um dashboard:
   - Vá para Dashboards > New > Import
   - Faça upload do arquivo JSON ou cole o conteúdo JSON

## Parando os Serviços

Para parar todos os contêineres:
```bash
docker-compose down
```

Para parar e remover todos os dados (volumes):
```bash
docker-compose down -v
```

## Usando a Ferramenta de Teste de Carga

O script `load_test.py` pode gerar carga artificial na sua API para testar o monitoramento.

### Uso Básico:

#### Teste com 1000 requisições a 10 requisições por segundo
```bash
py ./test/load_test.py --url http://localhost:8000 --requests 1000 --rate 10
```

#### Execute um teste por 5 minutos (300 segundos)
```bash
py ./test/load_test.py --url http://localhost:8000 --duration 300 --rate 10
```

#### Execute com 5 requisições simultâneas a 20 requisições/segundo
```bash
py ./test/load_test.py --url http://localhost:8000 --duration 60 --rate 20 --concurrent 5
```

### Parâmetros:

- `--url`: O endpoint da API a ser testado (padrão: http://localhost:8000)
- `--requests`: Número total de requisições a serem enviadas
- `--duration`: Quanto tempo executar o teste em segundos
- `--rate`: Taxa de requisições por segundo (padrão: 10)
- `--concurrent`: Número de requisições simultâneas (padrão: 1)

Nota: Você deve especificar `--requests` ou `--duration`.

## Melhores Práticas

Sempre obtenha a versão mais recente do dashboard antes de fazer alterações para evitar conflitos.