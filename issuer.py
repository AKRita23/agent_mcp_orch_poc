import jwt
import datetime
import uuid

MCP_SECRET = "supersecure"

def issue_token(agent_id, scope, intent):
    payload = {
        "sub": agent_id,
        "scope": scope,
        "intent": intent,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=10),
        "iat": datetime.datetime.utcnow(),
        "jti": str(uuid.uuid4())
    }
    return jwt.encode(payload, MCP_SECRET, algorithm="HS256")
