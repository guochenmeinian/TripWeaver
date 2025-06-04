# backend/main.py
from fastapi import FastAPI, Request
from TripWeaver.agent import root_agent

app = FastAPI()
agent = root_agent

@app.post("/message")
async def chat(request: Request):
    data = await request.json()
    user_message = data["message"]
    response = await agent.run(user_message)  # run 是 ADK 的核心函数
    return {"reply": response.output, "state": agent.state.dict()}


# uvicorn main:app --reload