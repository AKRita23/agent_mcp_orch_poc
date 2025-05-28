import jwt
import time
import json
import os

MCP_SECRET = "supersecure"
USED_JTIS = set()
THREAT_LOG = []
LOG_FILE = "threat_log.json"

THREAT_SCORES = {
    "scope_violation": 5,
    "intent_drift": 4,
    "replay": 3,
    "spoofing": 6
}

def log_threat(agent_id, category, state):
    event = {
        "timestamp": time.time(),
        "agent_id": agent_id,
        "tool_call": state.get("tool_call"),
        "intent": state.get("intent"),
        "category": category,
        "score": THREAT_SCORES[category]
    }
    THREAT_LOG.append(event)
    with open(LOG_FILE, "w") as f:
        json.dump(THREAT_LOG, f, indent=2)
    print(f"[ALERT] {category.upper()} - {event}")
    return None

def verify_token(state):
    token = state.get("token")
    try:
        decoded = jwt.decode(token, MCP_SECRET, algorithms=["HS256"])
    except Exception as e:
        print("[MCP] Invalid token:", e)
        return None

    if decoded["jti"] in USED_JTIS:
        return log_threat(decoded["sub"], "replay", state)
    USED_JTIS.add(decoded["jti"])

    if state["agent_id"] != decoded["sub"]:
        return log_threat(state["agent_id"], "spoofing", state)

    if state["tool_call"] not in decoded["scope"]:
        return log_threat(decoded["sub"], "scope_violation", state)

    if state["intent"] != decoded["intent"]:
        return log_threat(decoded["sub"], "intent_drift", state)

    print(f"[MCP] Agent {decoded['sub']} verified.")
    return state
