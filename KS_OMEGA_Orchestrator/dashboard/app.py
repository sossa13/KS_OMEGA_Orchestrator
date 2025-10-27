import streamlit as st, json, os, time, pandas as pd

st.set_page_config(page_title="KS-Ω Orchestrator v1.1", layout="wide")
st.title("KS-Ω Orchestrator — Dashboard v1.1")

log_path = "data/logs/app.log"
auto = st.sidebar.checkbox("Auto-refresh", value=True)
interval = st.sidebar.slider("Interval (s)", 1, 10, 3)

def load_logs():
    if not os.path.exists(log_path):
        return []
    with open(log_path, "r", encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]

placeholder = st.empty()
while True:
    logs = load_logs()
    rows = [{"time": l.get("time"), "event": l.get("event"), **(l.get("data") or {})} for l in logs]
    df = pd.DataFrame(rows)
    with placeholder.container():
        st.subheader("Derniers événements")
        st.dataframe(df.tail(200), use_container_width=True)
        st.subheader("Stats")
        if not df.empty:
            st.json({
                "events": df["event"].value_counts().to_dict(),
                "total": len(df)
            })
        else:
            st.write("Aucun log pour le moment.")
    if not auto: break
    time.sleep(interval)
