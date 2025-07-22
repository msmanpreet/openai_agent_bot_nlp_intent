from fastapi import FastAPI
from pydantic import BaseModel
from agent.intent_router import route_intent

app = FastAPI()

class ChatRequest(BaseModel):
    message: str
    session_id: str

@app.post("/chat")
async def chat(req: ChatRequest):
    response = await route_intent(req.message, req.session_id)
    return {"response": response}