"""
AirlinesHub Microservice
Responsável por gerenciar informações de voos e processar vendas.
"""

from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
import uuid
import json
from datetime import datetime

app = FastAPI(title="AirlinesHub", version="1.0.0")

# Simulação de banco de dados de voos
FLIGHTS_DATABASE = {
    "AA100": {
        "2025-01-15": {"flight": "AA100", "day": "2025-01-15", "value": 450.00},
        "2025-01-20": {"flight": "AA100", "day": "2025-01-20", "value": 480.00},
    },
    "UA200": {
        "2025-01-15": {"flight": "UA200", "day": "2025-01-15", "value": 520.00},
        "2025-01-22": {"flight": "UA200", "day": "2025-01-22", "value": 550.00},
    },
    "DL300": {
        "2025-02-10": {"flight": "DL300", "day": "2025-02-10", "value": 380.00},
        "2025-02-15": {"flight": "DL300", "day": "2025-02-15", "value": 400.00},
    },
}

# Simulação de transações vendidas
TRANSACTIONS = {}


class FlightResponse(BaseModel):
    flight: str
    day: str
    value: float


class SellRequest(BaseModel):
    flight: str
    day: str


class SellResponse(BaseModel):
    transaction_id: str


@app.get("/flight", response_model=FlightResponse)
async def get_flight(flight: str, day: str):
    """
    Endpoint GET /flight
    Retorna informações sobre um voo específico em uma data determinada.
    
    Parâmetros:
    - flight: Número do voo (ex: AA100)
    - day: Data do voo (ex: 2025-01-15)
    
    Resposta:
    - flight: Número do voo
    - day: Data do voo
    - value: Valor em dólar
    """
    if flight in FLIGHTS_DATABASE and day in FLIGHTS_DATABASE[flight]:
        return FLIGHTS_DATABASE[flight][day]
    else:
        # Retorna um voo simulado com valores padrão se não encontrado
        return FlightResponse(
            flight=flight,
            day=day,
            value=500.00  # Valor padrão
        )


@app.post("/sell", response_model=SellResponse)
async def sell_flight(request: SellRequest):
    """
    Endpoint POST /sell
    Processa a venda de um voo e retorna um ID de transação único.
    
    Parâmetros:
    - flight: Número do voo
    - day: Data do voo
    
    Resposta:
    - transaction_id: ID único da transação gerado automaticamente
    """
    transaction_id = str(uuid.uuid4())
    
    # Armazena a transação
    TRANSACTIONS[transaction_id] = {
        "flight": request.flight,
        "day": request.day,
        "timestamp": datetime.now().isoformat()
    }
    
    return SellResponse(transaction_id=transaction_id)


@app.get("/health")
async def health_check():
    """Verifica se o serviço está saudável."""
    return {"status": "healthy", "service": "AirlinesHub"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
