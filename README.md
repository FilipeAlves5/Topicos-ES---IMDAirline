# Projeto IMDAirline (Baseline)

Este projeto implementa um sistema de microsserviços para compra de passagens aéreas, como parte da avaliação da disciplina de Tópicos Especiais em Engenharia de Software.

O sistema é composto por 4 microsserviços e um orquestrador, todos executados em containers Docker.

## Arquitetura

[cite_start]O sistema segue a arquitetura de microsserviços orquestrada, conforme o diagrama fornecido na especificação do projeto[cite: 45].

1.  [cite_start]**IMDTravel (Orquestrador)**: `porta 8000` - Expõe o endpoint `/buyTicket` [cite: 56] e coordena as chamadas aos outros serviços.
2.  [cite_start]**AirlinesHub**: `porta 8001` - Gerencia informações de voos (`/flight`) [cite: 62] [cite_start]e processa vendas (`/sell`)[cite: 71].
3.  [cite_start]**Exchange**: `porta 8002` - Fornece a taxa de câmbio Dólar para Real (`/convert`)[cite: 67].
4.  [cite_start]**Fidelity**: `porta 8003` - Gerencia o programa de bônus de fidelidade (`/bonus`)[cite: 76].

## Como Rodar o Sistema

O sistema é 100% containerizado. A única dependência é o **Docker Desktop**.

### 1. Pré-requisitos

-   [Docker Desktop](https://www.docker.com/products/docker-desktop/) instalado e em execução.

### 2. Execução

1.  Abra um terminal (PowerShell, CMD ou outro) na raiz do projeto.
2.  Execute o seguinte comando para construir as imagens e iniciar todos os serviços:
    ```bash
    docker-compose up --build
    ```
3.  Aguarde até que os logs indiquem que todos os 4 serviços (`imd_travel`, `airlines_hub`, `exchange`, `fidelity`) estão no ar e "rodando em http://0.0.0.0...".

### 3. Testando a Execução

O endpoint principal de orquestração está disponível no `IMDTravel`:

-   **URL do Navegador (Documentação da API)**: `http://localhost:8000/docs`

Você pode usar a interface do Swagger UI (na URL acima) para testar o endpoint `POST /buyTicket`.

1.  Clique em `POST /buyTicket`, depois em "Try it out".
2.  Preencha o corpo da requisição com dados válidos, por exemplo:

    ```json
    {
      "flight": "AA100",
      "day": "2025-01-15",
      "user": "meu_usuario_123"
    }
    ```
3.  Clique em "Execute" e verifique a resposta.

## Como Rodar os Testes de Código

O projeto utiliza `pytest` para testes unitários e de integração.

1.  (Opcional, se não for rodar via Docker) Crie um ambiente virtual Python e instale as dependências:
    ```bash
    python -m venv venv
    source venv/bin/activate  # ou .\\venv\\Scripts\\activate no Windows
    pip install -r requirements.txt
    ```

2.  Execute o `pytest` na raiz do projeto. Ele descobrirá e rodará automaticamente todos os testes:
    ```bash
    pytest
    ```