# Secure Multi-Agent Orchestration: Detection Framework for Scope, Intent, and Replay Violations

This proof-of-concept demonstrates a lightweight detection layer for multi-agent AI systems that rely on Management Control Planes (MCPs) to coordinate planners, executors, and tool calls. The framework identifies and blocks three common security pitfalls in agent orchestration:
* Scope Overreach – An agent calling tools it wasn’t scoped to use
* Intent Drift – An agent executing a different action than what was originally assigned
* Replay Attacks – Reuse of previously valid tokens across agents or tasks

Built using LangGraph and AutoGen, the PoC simulates real-world orchestration and introduces a middleware layer (locally and in AWS Lambda) to verify every tool invocation using scoped JWTs and behavior validation. 

## Project Structure 

|-- main.py # Runs LangGraph base multi agent orchestration 
|-- middleware.py # verifies token scope, intent and replay violation 
|-- dashboard.py #Streamlit dashboard showing realtime detection logs 
|-- simulator.py #Malicious agent stimulating attack scenarios 
|-- autogen_sim.py #AutoGen orchestration layer with detection middleware 
|--utils/
    |--token_utils.py #JWT generation and decoding helper 
    |-- logger.py #Streming logger consumed by the dashboard 
|README.md 
