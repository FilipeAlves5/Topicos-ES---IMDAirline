"""
Fidelity Microservice
Responsável por gerenciar o programa de fidelidade e bônus dos usuários.
"""

from fastapi import FastAPI
from pydantic import BaseModel
from typing import Dict

app = FastAPI(title="Fidelity", version="1.0.0")

# Simulação de banco de dados de usuários e seus bônus
USERS_DATABASE: Dict[str, float] = {}


class BonusRequest(BaseModel):
    user: str
    bonus: int


class BonusResponse(BaseModel):
    status: str
    message: str


@app.post("/bonus", response_model=BonusResponse)
async def add_bonus(request: BonusRequest):
    """
    Endpoint POST /bonus
    Credita um valor de bônus na conta de fidelidade do usuário.
    
    Parâmetros:
    - user: ID do usuário
    - bonus: Valor inteiro do bônus a ser creditado
    
    Resposta:
    - status: "success" ou "error"
    - message: Mensagem descritiva
    """
    try:
        # Inicializa o usuário se não existir
        if request.user not in USERS_DATABASE:
            USERS_DATABASE[request.user] = 0.0
        
        # Adiciona o bônus à conta do usuário
        USERS_DATABASE[request.user] += request.bonus
        
        return BonusResponse(
            status="success",
            message=f"Bônus de {request.bonus} creditado para o usuário {request.user}. Saldo total: {USERS_DATABASE[request.user]}"
        )
    except Exception as e:
        return BonusResponse(
            status="error",
            message=f"Erro ao creditar bônus: {str(e)}"
        )


@app.get("/user/{user_id}")
async def get_user_bonus(user_id: str):
    """
    Endpoint GET /user/{user_id}
    Retorna o saldo de bônus de um usuário.
    
    Parâmetro:
    - user_id: ID do usuário
    
    Resposta:
    - user: ID do usuário
    - bonus_balance: Saldo total de bônus
    """
    balance = USERS_DATABASE.get(user_id, 0.0)
    return {"user": user_id, "bonus_balance": balance}


@app.get("/health")
async def health_check():
    """Verifica se o serviço está saudável."""
    return {"status": "healthy", "service": "Fidelity"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8003)
