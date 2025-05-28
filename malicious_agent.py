import random
import time
from issuer import issue_token
from middleware import verify_token

def run_continuous_probes(interval=2):
    print("[Malicious Agent] starting..")

    while True:
        session_id = f"session-{int(time.time())}"
        token = issue_token("malicious-agent-executor", ["call.summarizer"], "summarize")
        random_intent = random.choice(["delete", "steal", "write", "summarize", "exfil"])
        random_tool = random.choice(["call.delete", "call.write", "call.internal", "call.summarizer"])
        spoof_id = random.choice(["agent-planner-001", "agent-executor-003", "malicious-agent-executor"])

        state = {
            "agent_id": spoof_id,
            "intent": random_intent,
            "tool_call": random_tool,
            "token": token,
            "session_id": session_id
        }

        verify_token(state)
        time.sleep(interval)

if __name__ == "__main__":
    try:
        run_continuous_probes()
    except KeyboardInterrupt:
        print("\n[Malicious Agent] Stopped by user.")
