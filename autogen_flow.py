import random
import time
from issuer import issue_token
from middleware import verify_token
from autogen import UserProxyAgent, AssistantAgent


def simulate_autogen_convo():
    print("[AutoGen] Running simulated conversation...")
    token = issue_token("agent-autogen-001", ["call.summarizer", "call.query"], "summarize")

    # Simulated intent drift / misuse
    spoof_id = random.choice(["agent-planner-001", "agent-autogen-001"])
    tool_call = random.choice(["call.summarizer", "call.delete", "call.query"])
    intent = random.choice(["summarize", "delete", "query"])

    state = {
        "agent_id": spoof_id,
        "tool_call": tool_call,
        "intent": intent,
        "token": token,
        "session_id": f"autogen-session-{int(time.time())}",
        "framework": "autogen"
    }

    verify_token(state)