# Secure Multi-Agent Orchestration: Detection Framework for Scope, Intent, and Replay Violations

This proof-of-concept demonstrates a lightweight detection layer for multi-agent AI systems that rely on Management Control Planes (MCPs) to coordinate planners, executors, and tool calls. The framework identifies and blocks three common security pitfalls in agent orchestration:
* Scope Overreach – An agent calling tools it wasn’t scoped to use
* Intent Drift – An agent executing a different action than what was originally assigned
* Replay Attacks – Reuse of previously valid tokens across agents or tasks

Built using LangGraph and AutoGen, the PoC simulates real-world orchestration and introduces a middleware layer (locally and in AWS Lambda) to verify every tool invocation using scoped JWTs and behavior validation. 

## Project Structure 
<code> 
├── main.py               # Runs LangGraph-based multi-agent orchestration
├── middleware.py         # Verifies token scope, intent, and replay violations
├── dashboard.py          # Streamlit dashboard showing real-time detection logs
├── malicious_agent.py    # malicious agent simulating attack scenarios
├── autogen_flow.py       # AutoGen orchestration with detection middleware
├── issuer.py             # JWT generation and decoding helpers
└── README.md
</code>

## Getting Started

* Clone the repository
  
<code>git clone https://github.com/YOUR_HANDLE/secure-multi-agent-poc.git
 cd secure-multi-agent-poc</code>

* Set up the virtual environment

<code>python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
pip install -r requirements.txt</code>

* Run the main LangGraph PoC

<code> python main.py </code> 

* Launch the real-time detection dashboard

<code> streamlit run dashboard.py</code> 

* Simulate malicious agents

<code> python simulator.py </code> 

* (Another Orch Layer) Run AutoGen PoC

<code> python autogen_sim.py</code> 

## How it works 

Each agent in the system receives a scoped token tied to its ID, permitted tool(s), and intended task. The middleware intercepts every tool call and validates:
* The agent’s identity and scope
* The tool being used
* Whether the intent matches the assigned task
* Whether the token has been reused

Violations are logged in real-time — visible on the dashboard.py.

