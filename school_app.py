# ===== SCHOOL AI DASHBOARD — EFFORT-REDUCING VERSION =====
# Run: python -m streamlit run school_app.py
# USAII Hackathon 2026 Submission

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import random
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import IsolationForest
import warnings
warnings.filterwarnings('ignore')

st.set_page_config(page_title="Eco-School AI", page_icon="🏫", layout="wide")

# ===== DARK MODE =====
if 'dark_mode' not in st.session_state:
    st.session_state.dark_mode = False

# ===== DATA FILE =====
DATA_FILE = "school_data.csv"

# ===== GENERATE DEMO DATA =====
def generate_demo_data():
    dates = pd.date_range(end=datetime.now(), periods=30)
    data = pd.DataFrame({
        'date': dates,
        'walkers': np.random.randint(100, 160, 30),
        'bikers': np.random.randint(30, 55, 30),
        'car_dropoffs': np.random.randint(40, 70, 30),
        'bus_riders': np.random.randint(170, 200, 30),
        'energy_kwh': np.random.randint(800, 1200, 30),
        'food_waste_lbs': np.random.randint(15, 35, 30),
        'recycling_lbs': np.random.randint(15, 35, 30),
        'paper_reams': np.random.randint(5, 15, 30),
        'trees_planted': np.cumsum(np.random.randint(0, 2, 30)),
        'total_students': 450
    })
    data.to_csv(DATA_FILE, index=False)
    return data

def load_data():
    try:
        df = pd.read_csv(DATA_FILE)
        df['date'] = pd.to_datetime(df['date'])
        return df
    except:
        return generate_demo_data()

df = load_data()

# ===== AI FUNCTIONS =====

def detect_anomalies(df):
    """AI detects unusual patterns without human intervention"""
    anomalies = []
    
    # 1. Energy anomaly (lights left on)
    energy_mean = df['energy_kwh'].mean()
    energy_std = df['energy_kwh'].std()
    last_energy = df['energy_kwh'].iloc[-1]
    if last_energy > energy_mean + energy_std:
        anomalies.append(f"💡 **High energy usage detected:** {last_energy:.0f} kWh today (avg: {energy_mean:.0f} kWh). Lights may be left on.")
    
    # 2. Food waste anomaly
    waste_mean = df['food_waste_lbs'].mean()
    waste_std = df['food_waste_lbs'].std()
    last_waste = df['food_waste_lbs'].iloc[-1]
    if last_waste > waste_mean + waste_std:
        anomalies.append(f"🍎 **High food waste detected:** {last_waste:.0f} lbs today (avg: {waste_mean:.0f} lbs). Check cafeteria.")
    
    # 3. Walkers anomaly
    walk_mean = df['walkers'].mean()
    walk_std = df['walkers'].std()
    last_walk = df['walkers'].iloc[-1]
    if last_walk < walk_mean - walk_std:
        anomalies.append(f"🚶 **Low walking detected:** {last_walk:.0f} walkers today (avg: {walk_mean:.0f}). Weather or event?")
    
    # 4. Car dropoff anomaly
    car_mean = df['car_dropoffs'].mean()
    car_std = df['car_dropoffs'].std()
    last_car = df['car_dropoffs'].iloc[-1]
    if last_car > car_mean + car_std:
        anomalies.append(f"🚗 **High car dropoffs detected:** {last_car:.0f} cars today (avg: {car_mean:.0f}). Encourage walking!")
    
    return anomalies

def predict_future(df, days=14):
    """AI predicts future trends"""
    df_sorted = df.sort_values('date')
    predictions = {}
    
    for metric in ['walkers', 'energy_kwh', 'food_waste_lbs']:
        days_num = np.array(range(len(df_sorted))).reshape(-1, 1)
        model = LinearRegression()
        model.fit(days_num, df_sorted[metric].values)
        future = model.predict(np.array(range(len(df_sorted), len(df_sorted)+days)).reshape(-1, 1))
        predictions[metric] = {
            'current': df_sorted[metric].iloc[-1],
            'future': future,
            'trend': 'up' if future[-1] > df_sorted[metric].iloc[-1] else 'down'
        }
    return predictions

def generate_recommendations(df):
    """AI generates personalized recommendations"""
    recs = []
    latest = df.iloc[-1]
    
    walk_pct = (latest['walkers'] + latest['bikers']) / latest['total_students'] * 100
    if walk_pct < 40:
        recs.append(f"🚶 **Walk more:** Only {walk_pct:.0f}% walk/bike. Increase to 50%.")
    
    energy_avg = df['energy_kwh'].mean()
    if latest['energy_kwh'] > energy_avg:
        recs.append(f"💡 **Save energy:** Energy usage {latest['energy_kwh']:.0f} kWh vs {energy_avg:.0f} kWh avg. Turn off lights.")
    
    waste_avg = df['food_waste_lbs'].mean()
    if latest['food_waste_lbs'] > waste_avg:
        recs.append(f"🍎 **Reduce waste:** Food waste {latest['food_waste_lbs']:.0f} lbs vs {waste_avg:.0f} lbs avg. Share Table needed.")
    
    return recs

def calculate_grade(df):
    """AI calculates overall grade"""
    latest = df.iloc[-1]
    walk_pct = (latest['walkers'] + latest['bikers']) / latest['total_students'] * 100
    waste_pct = latest['recycling_lbs'] / (latest['food_waste_lbs'] + latest['recycling_lbs']) * 100
    energy_score = max(0, 100 - (latest['energy_kwh'] / 10))
    overall = (walk_pct * 0.3 + waste_pct * 0.2 + energy_score * 0.3 + min(100, latest['trees_planted'] * 2))
    
    if overall > 80: return 'A', overall, '#2e8b57'
    if overall > 60: return 'B', overall, '#3b82f6'
    if overall > 40: return 'C', overall, '#f59e0b'
    if overall > 20: return 'D', overall, '#ef4444'
    return 'F', overall, '#dc2626'

# ===== CSS =====
if st.session_state.dark_mode:
    st.markdown("""
    <style>
    .stApp { background: #1a1a2e; }
    .stMarkdown, .stText, label { color: #f0f3f8 !important; }
    .metric-card { background: #16213e; border-radius: 16px; padding: 1.2rem; margin-bottom: 1rem; text-align: center; border: 1px solid #2d3748; }
    .anomaly-card { background: #2d1a1a; border-radius: 16px; padding: 1rem; margin-bottom: 0.5rem; border-left: 4px solid #ef4444; }
    </style>
    """, unsafe_allow_html=True)

# ===== HEADER =====
col1, col2 = st.columns([4, 1])
with col1:
    st.markdown("# 🏫 Eco-School AI")
    st.caption("AI-powered environmental intelligence — zero manual data collection")
with col2:
    new_mode = st.toggle("🌙 Dark Mode", value=st.session_state.dark_mode)
    if new_mode != st.session_state.dark_mode:
        st.session_state.dark_mode = new_mode
        st.rerun()

# ===== SIDEBAR =====
pages = ["📊 Dashboard", "📤 Upload Data", "🤖 AI Predictions", "📋 Action Plan"]
selected_page = st.sidebar.radio("Navigate", pages)
st.sidebar.markdown("---")
st.sidebar.caption("🏫 Made for USAII Hackathon 2026")

# ============================================================
# PAGE 1: DASHBOARD (AI-Driven)
# ============================================================
if selected_page == "📊 Dashboard":
    st.subheader("📊 AI-Powered Dashboard")
    st.caption("AI automatically detects problems, predicts trends, and suggests actions.")
    
    latest = df.iloc[-1]
    grade, score, grade_color = calculate_grade(df)
    anomalies = detect_anomalies(df)
    predictions = predict_future(df)
    
    # ===== METRICS =====
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"""
        <div class="metric-card" style="border-left: 4px solid #2e8b57;">
            <div style="font-size: 2rem; font-weight: 800; color: #2e8b57;">{grade}</div>
            <div>📊 Overall Grade</div>
            <div style="font-size: 0.7rem;">Score: {score:.0f}/100</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        walk_pct = (latest['walkers'] + latest['bikers']) / latest['total_students'] * 100
        st.markdown(f"""
        <div class="metric-card" style="border-left: 4px solid #3b82f6;">
            <div style="font-size: 2rem; font-weight: 800; color: #3b82f6;">{walk_pct:.0f}%</div>
            <div>🚶 Walk/Bike</div>
            <div style="font-size: 0.7rem;">Goal: 50%</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        energy_avg = df['energy_kwh'].mean()
        energy_diff = ((latest['energy_kwh'] - energy_avg) / energy_avg * 100)
        st.markdown(f"""
        <div class="metric-card" style="border-left: 4px solid {'#ef4444' if energy_diff > 10 else '#2e8b57'};">
            <div style="font-size: 2rem; font-weight: 800; color: {'#ef4444' if energy_diff > 10 else '#2e8b57'};">{energy_diff:.0f}%</div>
            <div>💡 Energy vs Avg</div>
            <div style="font-size: 0.7rem;">{'🔴 High' if energy_diff > 10 else '✅ Normal'}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        waste_pct = latest['recycling_lbs'] / (latest['food_waste_lbs'] + latest['recycling_lbs']) * 100
        st.markdown(f"""
        <div class="metric-card" style="border-left: 4px solid #8b5cf6;">
            <div style="font-size: 2rem; font-weight: 800; color: #8b5cf6;">{waste_pct:.0f}%</div>
            <div>♻️ Waste Diverted</div>
            <div style="font-size: 0.7rem;">Goal: 70%</div>
        </div>
        """, unsafe_allow_html=True)
    
    # ===== AI ANOMALIES =====
    st.markdown("---")
    st.subheader("🚨 AI-Detected Anomalies")
    
    if anomalies:
        for anomaly in anomalies:
            st.markdown(f'<div class="anomaly-card">{anomaly}</div>', unsafe_allow_html=True)
    else:
        st.success("✅ No anomalies detected. Your school is performing well!")
    
    # ===== AI PREDICTIONS =====
    st.markdown("---")
    st.subheader("🔮 AI Predictions (Next 14 Days)")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        walk_pred = predictions['walkers']
        st.metric("🚶 Walkers", f"{walk_pred['current']:.0f} → {walk_pred['future'][-1]:.0f}",
                  delta=f"{walk_pred['future'][-1] - walk_pred['current']:.0f}")
    with col2:
        energy_pred = predictions['energy_kwh']
        st.metric("💡 Energy (kWh)", f"{energy_pred['current']:.0f} → {energy_pred['future'][-1]:.0f}",
                  delta=f"{energy_pred['future'][-1] - energy_pred['current']:.0f}")
    with col3:
        waste_pred = predictions['food_waste_lbs']
        st.metric("🍎 Food Waste (lbs)", f"{waste_pred['current']:.0f} → {waste_pred['future'][-1]:.0f}",
                  delta=f"{waste_pred['future'][-1] - waste_pred['current']:.0f}")
    
    # ===== GUILT TRIGGER =====
    st.markdown("---")
    if grade in ['D', 'F']:
        st.error("⚠️ **Your school is failing on environmental metrics. The AI has detected multiple issues.**")
    elif grade == 'C':
        st.warning("⚠️ **Your school is average. There's significant room for improvement.**")
    elif grade == 'B':
        st.info("📊 **Your school is doing well but not perfect. Keep pushing.**")
    else:
        st.success("🎉 **Your school is a leader in environmental sustainability!**")

# ============================================================
# PAGE 2: UPLOAD DATA (One-time effort)
# ============================================================
elif selected_page == "📤 Upload Data":
    st.subheader("📤 Upload School Data (One-Time Setup)")
    st.caption("Upload a CSV file with your school's data. The AI will handle the rest.")
    
    st.markdown("""
    ### 📋 Required CSV Format
    | date | walkers | bikers | car_dropoffs | bus_riders | energy_kwh | food_waste_lbs | recycling_lbs | paper_reams | trees_planted | total_students |
    |------|---------|--------|--------------|------------|------------|----------------|---------------|-------------|---------------|----------------|
    | 2026-06-01 | 145 | 47 | 50 | 188 | 950 | 22 | 28 | 8 | 2 | 450 |
    | 2026-06-02 | 150 | 48 | 48 | 190 | 920 | 20 | 30 | 7 | 2 | 450 |
    """)
    
    uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])
    
    if uploaded_file is not None:
        try:
            df_new = pd.read_csv(uploaded_file)
            df_new['date'] = pd.to_datetime(df_new['date'])
            df_new.to_csv(DATA_FILE, index=False)
            st.success("✅ Data uploaded successfully! AI is now analyzing your data.")
            st.dataframe(df_new.head())
        except Exception as e:
            st.error(f"Error: {e}. Please check the format.")
    
    # Demo data button (zero effort)
    if st.button("🔄 Use Demo Data (No effort needed)"):
        df = generate_demo_data()
        st.success("✅ Demo data loaded! Your dashboard is ready.")
        st.rerun()

# ============================================================
# PAGE 3: AI PREDICTIONS
# ============================================================
elif selected_page == "🤖 AI Predictions":
    st.subheader("🤖 AI Trend Analysis")
    st.caption("AI analyzes historical data and predicts future trends.")
    
    df_sorted = df.sort_values('date')
    predictions = predict_future(df)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 🚶 Walkers Trend")
        future_dates = [df_sorted['date'].iloc[-1] + timedelta(days=i+1) for i in range(14)]
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df_sorted['date'], y=df_sorted['walkers'], mode='lines+markers', name='Actual', line=dict(color='#2e8b57')))
        fig.add_trace(go.Scatter(x=future_dates, y=predictions['walkers']['future'], mode='lines', name='AI Predicted', line=dict(color='#3b82f6', dash='dash')))
        fig.update_layout(hovermode='x unified', height=350)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("#### 💡 Energy Usage Trend")
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df_sorted['date'], y=df_sorted['energy_kwh'], mode='lines+markers', name='Actual', line=dict(color='#f59e0b')))
        fig.add_trace(go.Scatter(x=future_dates, y=predictions['energy_kwh']['future'], mode='lines', name='AI Predicted', line=dict(color='#ef4444', dash='dash')))
        fig.update_layout(hovermode='x unified', height=350)
        st.plotly_chart(fig, use_container_width=True)
    
    col3, col4 = st.columns(2)
    
    with col3:
        st.markdown("#### 🍎 Food Waste Trend")
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df_sorted['date'], y=df_sorted['food_waste_lbs'], mode='lines+markers', name='Actual', line=dict(color='#8b5cf6')))
        fig.add_trace(go.Scatter(x=future_dates, y=predictions['food_waste_lbs']['future'], mode='lines', name='AI Predicted', line=dict(color='#ec4899', dash='dash')))
        fig.update_layout(hovermode='x unified', height=350)
        st.plotly_chart(fig, use_container_width=True)
    
    with col4:
        st.markdown("#### 📊 AI Insights")
        st.info("💡 **AI Insight:** " + 
                ("Walking is trending UP. Keep encouraging students!" if predictions['walkers']['trend'] == 'up' else "Walking is trending DOWN. Time for a campaign!"))
        
        if predictions['energy_kwh']['trend'] == 'down':
            st.success("🎉 Energy usage is decreasing! Great job!")
        else:
            st.warning("⚠️ Energy usage is increasing. Check for lights left on.")

# ============================================================
# PAGE 4: ACTION PLAN
# ============================================================
elif selected_page == "📋 Action Plan":
    st.subheader("📋 AI-Generated Action Plan")
    st.caption("Based on your data, here are the highest-impact actions.")
    
    latest = df.iloc[-1]
    walk_pct = (latest['walkers'] + latest['bikers']) / latest['total_students'] * 100
    energy_avg = df['energy_kwh'].mean()
    waste_avg = df['food_waste_lbs'].mean()
    
    st.markdown("### 🔴 PRIORITY 1: Energy Efficiency")
    if latest['energy_kwh'] > energy_avg:
        st.markdown(f"**Problem:** Energy usage is {latest['energy_kwh']:.0f} kWh vs {energy_avg:.0f} kWh avg.")
        st.markdown("**Impact:** Save $200/month by reducing usage.")
        st.markdown("**AI Suggestion:** Install smart plugs or assign energy monitors.")
    else:
        st.success("✅ Energy usage is below average. Keep it up!")
    
    st.markdown("### 🟠 PRIORITY 2: Transportation")
    if walk_pct < 40:
        st.markdown(f"**Problem:** Only {walk_pct:.0f}% walk/bike to school.")
        st.markdown("**Impact:** Reduce 500 lbs CO2/week by increasing to 50%.")
        st.markdown("**AI Suggestion:** Launch a 'Walk & Roll Wednesday' program.")
    else:
        st.success("✅ Walking rate is good. Aim for 50%!")
    
    st.markdown("### 🟡 PRIORITY 3: Food Waste")
    if latest['food_waste_lbs'] > waste_avg:
        st.markdown(f"**Problem:** {latest['food_waste_lbs']:.0f} lbs food waste vs {waste_avg:.0f} lbs avg.")
        st.markdown("**Impact:** Divert 5,000 lbs/year to hungry people.")
        st.markdown("**AI Suggestion:** Start a Share Table program.")
    else:
        st.success("✅ Food waste is below average. Great work!")
    
    st.markdown("---")
    st.markdown("### 📊 Estimated Total Impact")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("🌡️ Temperature Reduction", "2-3°F")
    with col2:
        st.metric("💰 Cost Savings", "$500/year")
    with col3:
        st.metric("🌿 CO2 Reduced", "2,000 lbs/year")

# ===== FOOTER =====
st.markdown("---")
st.caption("🏫 Eco-School AI · Made for USAII Hackathon 2026 · Data is stored locally")