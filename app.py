import streamlit as st
import pandas as pd
import plotly.express as px
from pymongo import MongoClient
import random
from datetime import datetime

# ---------- PAGE CONFIG ----------
st.set_page_config(page_title="Traffic Dashboard", layout="wide")

# ---------- MONGODB CONNECTION ----------
uri = "mongodb+srv://delluser:<password>@cluster0.hh7ijb9.mongodb.net/?appName=Cluster0"
client = MongoClient(uri)

db = client["traffic_db"]
collection = db["traffic_data"]

# ---------- LOAD DATA ----------
data = list(collection.find({}, {"_id": 0}))
df = pd.DataFrame(data)

if df.empty:
    st.warning("No data found in database")
    st.stop()

# Convert time column
df["time"] = pd.to_datetime(df["time"], format="%H:%M")

# ---------- HEADER ----------
col1, col2 = st.columns([3, 1])

with col1:
    st.title("🚦 Traffic Analytics Dashboard")

with col2:
    st.markdown("### 🚗 Live Data")

# ---------- SIDEBAR ----------
st.sidebar.markdown("## 🚦 Traffic System")
st.sidebar.markdown("Smart ITS Dashboard")

location = st.sidebar.selectbox(
    "Select Location",
    df["location"].unique()
)

# Time slider
min_time = df["time"].min().to_pydatetime()
max_time = df["time"].max().to_pydatetime()

time_range = st.sidebar.slider(
    "Select Time Range",
    min_value=min_time,
    max_value=max_time,
    value=(min_time, max_time),
    format="HH:mm"
)

# ---------- LIVE DATA BUTTON ----------
if st.sidebar.button("Add Random Traffic Data"):
    new_data = {
        "time": datetime.now().strftime("%H:%M"),
        "location": random.choice(["A", "B", "C"]),
        "vehicle_count": random.randint(50, 250),
        "avg_speed": random.randint(20, 60),
        "emissions": random.randint(100, 400)
    }
    collection.insert_one(new_data)
    st.sidebar.success("New data added!")

# ---------- REFRESH ----------
if st.button("🔄 Refresh Data"):
    st.rerun()

# ---------- FILTER DATA ----------
filtered = df[
    (df["location"] == location) &
    (df["time"] >= pd.to_datetime(time_range[0])) &
    (df["time"] <= pd.to_datetime(time_range[1]))
]

if filtered.empty:
    st.warning("No data available for selected filters")
    st.stop()

# ---------- KPI SECTION ----------
st.markdown("### Key Metrics")

kpi1, kpi2, kpi3 = st.columns(3)

kpi1.metric("Total Vehicles", int(filtered["vehicle_count"].sum()))
kpi2.metric("Average Speed", f"{filtered['avg_speed'].mean():.2f}")
kpi3.metric("Total Emissions", int(filtered["emissions"].sum()))

st.markdown("---")

# ---------- SMART INSIGHTS ----------
st.markdown("### Smart Insights")
st.info("Insights are based on selected filters and real-time data simulation")

# Peak traffic
peak_row = filtered.loc[filtered["vehicle_count"].idxmax()]
peak_time = peak_row["time"].strftime("%H:%M")
peak_value = peak_row["vehicle_count"]

# Low traffic
low_row = filtered.loc[filtered["vehicle_count"].idxmin()]
low_time = low_row["time"].strftime("%H:%M")

# Avg traffic
avg_traffic = filtered["vehicle_count"].mean()

# Congestion level
if avg_traffic > 180:
    congestion = "High"
    congestion_color = "🔴"
elif avg_traffic > 120:
    congestion = "Moderate"
    congestion_color = "🟠"
else:
    congestion = "Low"
    congestion_color = "🟢"

# Trend
first = filtered.iloc[0]["vehicle_count"]
last = filtered.iloc[-1]["vehicle_count"]

if last > first:
    trend = "Increasing 📈"
elif last < first:
    trend = "Decreasing 📉"
else:
    trend = "Stable ➖"

# Display insights
ins1, ins2, ins3, ins4 = st.columns(4)

ins1.metric("Peak Traffic", f"{peak_time}", f"{peak_value} vehicles")
ins2.metric("Congestion Level", f"{congestion_color} {congestion}")
ins3.metric("Best Time to Travel", low_time)
ins4.metric("Traffic Trend", trend)

st.markdown("---")

# ---------- CHARTS ----------
filtered["time_str"] = filtered["time"].dt.strftime("%H:%M")

chart1, chart2 = st.columns(2)

with chart1:
    st.markdown("#### Traffic Density Over Time")
    fig1 = px.line(
        filtered,
        x="time_str",
        y="vehicle_count",
        markers=True
    )
    fig1.update_layout(
        xaxis_title="Time",
        yaxis_title="Vehicle Count",
        template="plotly_white"
    )
    st.plotly_chart(fig1, use_container_width=True)

with chart2:
    st.markdown("#### Emissions Over Time")
    fig2 = px.bar(
        filtered,
        x="time_str",
        y="emissions"
    )
    fig2.update_layout(
        xaxis_title="Time",
        yaxis_title="Emissions",
        template="plotly_white"
    )
    st.plotly_chart(fig2, use_container_width=True)

st.markdown("---")

# ---------- LOCATION COMPARISON ----------
st.markdown("### Location Comparison")

fig3 = px.bar(
    df,
    x="location",
    y="vehicle_count",
    color="location",
    barmode="group"
)

fig3.update_layout(
    xaxis_title="Location",
    yaxis_title="Vehicle Count",
    template="plotly_white"
)

st.plotly_chart(fig3, use_container_width=True)

# ---------- FOOTER ----------
st.markdown("---")
st.caption("Built using Streamlit | Intelligent Transportation Systems Project")
