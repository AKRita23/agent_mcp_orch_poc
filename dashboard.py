import streamlit as st
import json
import os
import time
import pandas as pd

LOG_FILE = "threat_log.json"

st.set_page_config(page_title="MCP Threat Dashboard", layout="wide")
st.title("Real-Time MCP Threat Detection")

placeholder_table = st.empty()
placeholder_chart = st.empty()

def format_event(event):
    return {
        "Timestamp": time.strftime('%H:%M:%S', time.localtime(event["timestamp"])),
        "Agent ID": event["agent_id"],
        "Tool": event["tool_call"],
        "Intent": event["intent"],
        "Category": event["category"].upper(),
        "Score": event["score"],
        "Framework": event.get("framework", "unknown")
    }

while True:
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE) as f:
            raw = json.load(f)
    else:
        raw = []

    if raw:
        # Framework filter dropdown
        frameworks = sorted(set(e.get("framework", "unknown") for e in raw))
        selected = st.selectbox("🔍 Filter by framework", ["All"] + frameworks)

        if selected != "All":
            filtered = [e for e in raw if e.get("framework") == selected]
        else:
            filtered = raw

        # Display formatted table
        formatted = [format_event(e) for e in filtered]
        placeholder_table.table(formatted[::-1])  # Show latest first

        # Generate and display bar chart
        df = pd.DataFrame(filtered)
        if not df.empty:
            category_counts = df.groupby(["framework", "category"]).size().unstack().fillna(0)
            st.markdown("### 📊 Threats by Framework & Category")
            placeholder_chart.bar_chart(category_counts)
        else:
            placeholder_chart.info("No data for selected framework.")
    else:
        placeholder_table.info("Waiting for threats...")
        placeholder_chart.empty()

    time.sleep(1)
