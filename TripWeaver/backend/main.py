# agent/backend/main.py

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from google.adk.runtime.agent_runtime import AgentRuntime
from google.adk.runtime.session_service import SessionService
from google.adk.events import Event, EventActions
from TripWeaver.agent import root_agent
import time

app = FastAPI()

# 跨域设置，允许 React 本地前端访问
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 初始化 ADK 运行时与会话服务
runtime = AgentRuntime(root_agent)
session_service = SessionService(runtime=runtime)

@app.post("/create_session")
async def create_session():
    session = await session_service.create_session()
    return {"session_id": session.session_id}

@app.get("/state/{session_id}")
async def get_state(session_id: str):
    session = await session_service.get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return session.state

@app.post("/update_state/{session_id}")
async def update_state(session_id: str, update: dict):
    session = await session_service.get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    await session_service.append_event(session, Event(
        invocation_id=session.active_invocation.invocation_id,
        author="system",
        actions=EventActions(state_delta=update),
        timestamp=time.time()
    ))
    return {"message": "State updated", "new_state": session.state}
