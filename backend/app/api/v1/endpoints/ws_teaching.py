"""
Real-Time Teaching WebSocket Endpoint
Provides live bidirectional streaming between the learner and the cognitive AI teaching engine.
Streams lesson step transitions, live transcript tokens, visual trigger events, and checkpoint dispatch.
"""

from fastapi import APIRouter, WebSocket, WebSocketDisconnect
import asyncio
import json
from typing import Dict, List

router = APIRouter()

class TeachingConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, List[WebSocket]] = {}

    async def connect(self, session_id: str, websocket: WebSocket):
        await websocket.accept()
        if session_id not in self.active_connections:
            self.active_connections[session_id] = []
        self.active_connections[session_id].append(websocket)

    def disconnect(self, session_id: str, websocket: WebSocket):
        if session_id in self.active_connections:
            if websocket in self.active_connections[session_id]:
                self.active_connections[session_id].remove(websocket)
            if not self.active_connections[session_id]:
                del self.active_connections[session_id]

    async def send_event(self, session_id: str, event: Dict):
        if session_id in self.active_connections:
            for connection in self.active_connections[session_id]:
                try:
                    await connection.send_text(json.dumps(event))
                except Exception:
                    pass

manager = TeachingConnectionManager()

@router.websocket("/ws/lesson/{session_id}")
async def lesson_websocket_endpoint(websocket: WebSocket, session_id: str):
    """
    Live WebSocket channel for real-time pedagogical streaming.
    """
    await manager.connect(session_id, websocket)
    try:
        # Send initial calibration handshake
        await websocket.send_text(json.dumps({
            "type": "SESSION_INIT",
            "session_id": session_id,
            "status": "connected",
            "teacher": "Dr. Aris",
            "pipeline": {
                "visual_ready": True,
                "audio_ready": True,
                "avatar_ready": True
            }
        }))

        while True:
            raw_data = await websocket.receive_text()
            message = json.loads(raw_data)
            msg_type = message.get("type")

            if msg_type == "PING":
                await websocket.send_text(json.dumps({"type": "PONG"}))

            elif msg_type == "START_STREAM":
                concept = message.get("concept", "Resistance")
                # Stream pedagogical tokens
                tokens = [
                    "Think ", "of ", "resistance ", "as ", "the ", "narrowing ",
                    "of ", "a ", "water ", "pipe. ",
                    "When ", "the ", "pipe ", "constricts, ",
                    "fewer ", "gallons ", "can ", "flow ", "per ", "minute."
                ]
                for tok in tokens:
                    await asyncio.sleep(0.08)
                    await websocket.send_text(json.dumps({
                        "type": "STREAM_TOKEN",
                        "token": tok,
                        "concept": concept
                    }))

                # Send visual synchronization event
                await websocket.send_text(json.dumps({
                    "type": "VISUAL_UPDATE",
                    "visual_type": "water_pipe",
                    "pipe_width": "Narrow",
                    "description": "Hydraulic constriction demonstration"
                }))

            elif msg_type == "CHECKPOINT_SUBMIT":
                choice = message.get("choice", "B")
                is_correct = (choice.upper() == "B")
                await websocket.send_text(json.dumps({
                    "type": "CHECKPOINT_EVALUATION",
                    "is_correct": is_correct,
                    "mastery_delta": 10 if is_correct else -6,
                    "next_state": "ADVANCE" if is_correct else "REMEDIATE"
                }))

    except WebSocketDisconnect:
        manager.disconnect(session_id, websocket)
    except Exception:
        manager.disconnect(session_id, websocket)
