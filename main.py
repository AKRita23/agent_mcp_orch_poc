from langgraph.graph import StateGraph
from typing import TypedDict
from issuer import issue_token
from middleware import verify_token

class AgentState(TypedDict, total=False):
    planner_state: dict
    exec2_state: dict
    exec3_state: dict

def mcp_issuer(state: AgentState) -> AgentState:
    print("[MCP] Issuing scoped token")
    token = issue_token("agent-planner-001", ["call.summarizer"], "summarize")
    return {
        "planner_state": {
            "agent_id": "agent-planner-001",
            "intent": "summarize",
            "tool_call": "call.summarizer",
            "token": token
        }
    }

def mcp_middleware(state: AgentState) -> AgentState:
    for key in ["planner_state", "exec2_state", "exec3_state"]:
        if key in state:
            result = verify_token(state[key])
            if result:
                return {key: result}
            else:
                print(f"[MCP] Blocking flow due to threat detected for: {key}")
                return {}
    return {}

def executor(state: AgentState) -> AgentState:
    planner_state = state.get("planner_state")
    if planner_state:
        print(f"[Executor] Executing: {planner_state['tool_call']}")
    return state

def executor_identity_mismatch(state: AgentState) -> AgentState:
    print("[Executor 2] Trying to use token not issued to me")
    token = issue_token("agent-planner-001", ["call.summarizer"], "summarize")
    return {
        "exec2_state": {
            "agent_id": "agent-executor-002",
            "intent": "summarize",
            "tool_call": "call.summarizer",
            "token": token
        }
    }

def executor_tool_mismatch(state: AgentState) -> AgentState:
    print("[Executor 3] Trying to use wrong tool with valid token")
    token = issue_token("agent-executor-003", ["call.summarizer"], "summarize")
    return {
        "exec3_state": {
            "agent_id": "agent-executor-003",
            "intent": "summarize",
            "tool_call": "call.delete",
            "token": token
        }
    }

def done(state: AgentState) -> AgentState:
    print("[✓] Flow complete.")
    return state

builder = StateGraph(AgentState)
builder.add_node("mcp_issuer", mcp_issuer)
builder.add_node("mcp_middleware", mcp_middleware)
builder.add_node("executor", executor)
builder.add_node("executor_identity_mismatch", executor_identity_mismatch)
builder.add_node("executor_tool_mismatch", executor_tool_mismatch)
builder.add_node("done", done)

builder.set_entry_point("mcp_issuer")
builder.add_edge("mcp_issuer", "mcp_middleware")
builder.add_edge("mcp_middleware", "executor")
builder.add_edge("executor", "executor_identity_mismatch")
builder.add_edge("executor", "executor_tool_mismatch")
builder.add_edge("executor_identity_mismatch", "mcp_middleware")
builder.add_edge("executor_tool_mismatch", "mcp_middleware")
builder.add_edge("mcp_middleware", "done")
builder.set_finish_point("done")

graph = builder.compile()
graph.invoke({})
