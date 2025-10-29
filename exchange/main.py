"""
Exchange Microservice
Responsável por fornecer a taxa de câmbio (Dólar para Real).
"""

from fastapi import FastAPI
import random

app = FastAPI(title="Exchange", version="1.0.0")


@app.get("/convert")
async def convert_currency():
    """
    Endpoint GET /convert
    Retorna a taxa de conversão de Dólar para Real.
    
    A taxa é gerada aleatoriamente entre 5.0 e 6.0 (1 dólar = entre 5 e 6 reais).
    
    Resposta:
    - Número real positivo representando a taxa de câmbio
    """
    # Gera uma taxa de câmbio aleatória entre 5.0 e 6.0
    exchange_rate = round(random.uniform(5.0, 6.0), 2)
    return {"exchange_rate": exchange_rate}


@app.get("/health")
async def health_check():
    """Verifica se o serviço está saudável."""
    return {"status": "healthy", "service": "Exchange"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)
