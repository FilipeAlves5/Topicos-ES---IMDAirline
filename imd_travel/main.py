"""
IMDTravel Microservice
Serviço orquestrador responsável por coordenar a compra de passagens aéreas.
Realiza chamadas aos microsserviços: AirlinesHub, Exchange e Fidelity.
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import httpx
import logging
from typing import Optional

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="IMDTravel", version="1.0.0")

# URLs dos microsserviços (usando nomes de serviço do Docker Compose)
AIRLINES_HUB_URL = "http://localhost:8001"
EXCHANGE_URL = "http://localhost:8002"
FIDELITY_URL = "http://localhost:8003"


class BuyTicketRequest(BaseModel):
    flight: str
    day: str
    user: str


class BuyTicketResponse(BaseModel):
    success: bool
    message: str
    transaction_id: Optional[str] = None
    value_in_dollars: Optional[float] = None
    value_in_reais: Optional[float] = None
    bonus_credited: Optional[int] = None


@app.post("/buyTicket", response_model=BuyTicketResponse)
async def buy_ticket(request: BuyTicketRequest):
    """
    Endpoint POST /buyTicket
    Orquestra o fluxo completo de compra de uma passagem aérea.
    
    Parâmetros:
    - flight: Número do voo
    - day: Data do voo
    - user: ID do usuário
    
    Fluxo:
    1. Consulta informações do voo (AirlinesHub)
    2. Obtém taxa de câmbio (Exchange)
    3. Realiza a venda do voo (AirlinesHub)
    4. Credita bônus de fidelidade (Fidelity)
    
    Resposta:
    - success: Indica se a compra foi bem-sucedida
    - message: Mensagem descritiva
    - transaction_id: ID único da transação
    - value_in_dollars: Valor da passagem em dólares
    - value_in_reais: Valor da passagem em reais
    - bonus_credited: Bônus creditado
    """
    
    try:
        async with httpx.AsyncClient() as client:
            
            # Request 1: Consultar informações do voo
            logger.info(f"[Request 1] Consultando voo {request.flight} em {request.day}")
            flight_response = await client.get(
                f"{AIRLINES_HUB_URL}/flight",
                params={"flight": request.flight, "day": request.day},
                timeout=10.0
            )
            flight_response.raise_for_status()
            flight_data = flight_response.json()
            value_in_dollars = flight_data.get("value", 0.0)
            logger.info(f"[Request 1] Voo encontrado: ${value_in_dollars}")
            
            # Request 2: Obter taxa de câmbio
            logger.info("[Request 2] Consultando taxa de câmbio")
            exchange_response = await client.get(
                f"{EXCHANGE_URL}/convert",
                timeout=10.0
            )
            exchange_response.raise_for_status()
            exchange_data = exchange_response.json()
            exchange_rate = exchange_data.get("exchange_rate", 5.5)
            logger.info(f"[Request 2] Taxa de câmbio: {exchange_rate}")
            
            # Cálculos
            value_in_reais = value_in_dollars * exchange_rate
            bonus_to_credit = round(value_in_dollars)  # Valor inteiro mais próximo
            
            logger.info(f"Cálculos: ${value_in_dollars} * {exchange_rate} = R${value_in_reais:.2f}")
            logger.info(f"Bônus a creditar: {bonus_to_credit} pontos")
            
            # Request 3: Vender o voo
            logger.info(f"[Request 3] Processando venda do voo {request.flight}")
            sell_response = await client.post(
                f"{AIRLINES_HUB_URL}/sell",
                json={"flight": request.flight, "day": request.day},
                timeout=10.0
            )
            sell_response.raise_for_status()
            sell_data = sell_response.json()
            transaction_id = sell_data.get("transaction_id")
            logger.info(f"[Request 3] Venda realizada com ID: {transaction_id}")
            
            # Request 4: Creditar bônus de fidelidade
            logger.info(f"[Request 4] Creditando {bonus_to_credit} pontos para usuário {request.user}")
            bonus_response = await client.post(
                f"{FIDELITY_URL}/bonus",
                json={"user": request.user, "bonus": bonus_to_credit},
                timeout=10.0
            )
            bonus_response.raise_for_status()
            bonus_data = bonus_response.json()
            logger.info(f"[Request 4] Bônus creditado com sucesso")
            
            # Resposta de sucesso
            return BuyTicketResponse(
                success=True,
                message=f"Compra realizada com sucesso! Transação: {transaction_id}",
                transaction_id=transaction_id,
                value_in_dollars=value_in_dollars,
                value_in_reais=round(value_in_reais, 2),
                bonus_credited=bonus_to_credit
            )
            
    except httpx.HTTPError as e:
        logger.error(f"Erro HTTP ao chamar microsserviço: {str(e)}")
        raise HTTPException(
            status_code=502,
            detail=f"Erro ao comunicar com microsserviço: {str(e)}"
        )
    except Exception as e:
        logger.error(f"Erro inesperado: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Erro interno ao processar compra: {str(e)}"
        )


@app.get("/health")
async def health_check():
    """Verifica se o serviço está saudável."""
    return {"status": "healthy", "service": "IMDTravel"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
