import time
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="IoT Smart Irrigation Management", layout="wide"
)

# Custom Dark Theme Styling
st.markdown(
    """
    <style>
    .stApp { background-color: #0e131f; color: #ffffff; }
    .alert-box { background-color: #5c1d24; color: #ff9999; padding: 10px; border-radius: 5px; border: 1px solid #ff4d4d; font-weight: bold; }
    .safe-box { background-color: #1b3b2b; color: #79efaf; padding: 10px; border-radius: 5px; border: 1px solid #2ecc71; font-weight: bold; }
    </style>
""",
    unsafe_allow_html=True,
)

st.sidebar.title("Demo Controls")
pause_sim = st.sidebar.checkbox("Pause simulation")

st.sidebar.markdown("### Trigger a fault in a zone:")
zone1_fault = st.sidebar.selectbox(
    "Zone 1 (Wheat)", ["none", "pump_failure", "pipe_leakage", "dry_spell"]
)
zone2_fault = st.sidebar.selectbox(
    "Zone 2 (Sugarcane)", ["none", "pump_failure", "pipe_leakage", "dry_spell"]
)
zone3_fault = st.sidebar.selectbox(
    "Zone 3 (Cotton)", ["none", "pump_failure", "pipe_leakage", "dry_spell"]
)

st.title("IoT-Based Smart Irrigation Management & Water Stress Prediction")
st.markdown(
    "Simulated IoT sensors: soil moisture, temperature, and relative humidity,"
    " with automated pump actuation."
)
st.markdown("---")

if "val_w" not in st.session_state:
  st.session_state.val_w = {
      "moisture": 58.4,
      "temp": 23.5,
      "humidity": 62.0,
      "history": [],
  }
  st.session_state.val_s = {
      "moisture": 72.1,
      "temp": 27.8,
      "humidity": 74.5,
      "history": [],
  }
  st.session_state.val_c = {
      "moisture": 44.2,
      "temp": 31.0,
      "humidity": 48.3,
      "history": [],
  }


def update_zone_state(state, fault):
  if fault == "pump_failure":
    state["moisture"] = max(10.0, state["moisture"] - 1.5)
  elif fault == "pipe_leakage":
    state["moisture"] = min(100.0, state["moisture"] + 1.8)
  elif fault == "dry_spell":
    state["moisture"] = max(5.0, state["moisture"] - 2.5)
  else:
    state["moisture"] += 0.1 if state["moisture"] < 50 else -0.1

  state["history"].append({
      "moisture": state["moisture"],
      "temp": state["temp"],
      "humidity": state["humidity"],
  })
  if len(state["history"]) > 30:
    state["history"].pop(0)


if not pause_sim:
  update_zone_state(st.session_state.val_w, zone1_fault)
  update_zone_state(st.session_state.val_s, zone2_fault)
  update_zone_state(st.session_state.val_c, zone3_fault)

col1, col2, col3 = st.columns(3)


def render_zone_panel(title, state, fault):
  st.markdown(f"### {title}")
  m1, m2, m3 = st.columns(3)
  m1.metric("Moisture (%)", f"{state['moisture']:.2f}")
  m2.metric("Temp (°C)", f"{state['temp']:.2f}")
  m3.metric("Humidity (%)", f"{state['humidity']:.2f}")

  is_risk = fault != "none" or state["moisture"] < 35 or state["moisture"] > 80
  risk_label = "HIGH" if is_risk else "LOW"

  if is_risk:
    st.markdown(
        f"**Water Stress Risk:** <span style='color:red;'>🔴 {risk_label}</span>",
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="alert-box">ALERT: Water stress detected! Pump active.'
        "</div>",
        unsafe_allow_html=True,
    )
  else:
    st.markdown(
        f"**Water Stress Risk:** <span style='color:green;'>🟢"
        f" {risk_label}</span>",
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="safe-box">STATUS: Optimal hydration levels.</div>',
        unsafe_allow_html=True,
    )

  if len(state["history"]) > 0:
    st.line_chart(
        pd.DataFrame(state["history"])[["moisture", "temp", "humidity"]],
        height=180,
        use_container_width=True,
    )


with col1:
  render_zone_panel("Zone 1: Wheat", st.session_state.val_w, zone1_fault)
with col2:
  render_zone_panel("Zone 2: Sugarcane", st.session_state.val_s, zone2_fault)
with col3:
  render_zone_panel("Zone 3: Cotton", st.session_state.val_c, zone3_fault)

if not pause_sim:
  time.sleep(1)
  st.rerun()