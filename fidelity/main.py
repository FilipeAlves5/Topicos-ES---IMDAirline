from fastapi import FastAPI
from pydantic import BaseModel
from typing import Dict

app = FastAPI(title="Fidelity", version="1.0.0")

USERS_DATABASE: Dict[str, float] = {}


class BonusRequest(BaseModel):
    user: str
    bonus: int


class BonusResponse(BaseModel):
    status: str
    message: str


@app.post("/bonus", response_model=BonusResponse)
async def add_bonus(request: BonusRequest):
    try:
        if request.user not in USERS_DATABASE:
            USERS_DATABASE[request.user] = 0.0
        
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
    balance = USERS_DATABASE.get(user_id, 0.0)
    return {"user": user_id, "bonus_balance": balance}


@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "Fidelity"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8003)
