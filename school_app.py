# ===== ECO-SCHOOL AI — PROFESSIONAL VERSION =====
# Run: python -m streamlit run school_app.py
# USAII Hackathon 2026 Submission

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import random
import os
from sklearn.linear_model import LinearRegression
import warnings
warnings.filterwarnings('ignore')

# ===== PAGE CONFIG =====
st.set_page_config(
    page_title="Eco-School AI",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="collapsed"
)

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
        'walk': np.random.randint(100, 160, 30),
        'bike': np.random.randint(30, 55, 30),
        'car': np.random.randint(40, 70, 30),
        'bus': np.random.randint(170, 200, 30),
        'lights_left_on': np.random.randint(2, 8, 30),
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

# ============================================================
# AI FUNCTIONS
# ============================================================
def detect_anomalies(df):
    anomalies = []
    latest = df.iloc[-1]
    if latest['lights_left_on'] > 5:
        anomalies.append(f"💡 {latest['lights_left_on']} classrooms left lights on")
    waste_avg = df['food_waste_lbs'].mean()
    if latest['food_waste_lbs'] > waste_avg + df['food_waste_lbs'].std():
        anomalies.append(f"🍎 {latest['food_waste_lbs']:.0f} lbs food waste (avg: {waste_avg:.0f})")
    walk_avg = df['walk'].mean()
    if latest['walk'] < walk_avg - df['walk'].std():
        anomalies.append(f"🚶 {latest['walk']:.0f} walkers (avg: {walk_avg:.0f})")
    return anomalies

def predict_trends(df, days=14):
    df_sorted = df.sort_values('date')
    predictions = {}
    metrics = ['walk', 'food_waste_lbs', 'recycling_lbs']
    for metric in metrics:
        days_num = np.array(range(len(df_sorted))).reshape(-1, 1)
        model = LinearRegression()
        model.fit(days_num, df_sorted[metric].values)
        future = model.predict(np.array(range(len(df_sorted), len(df_sorted)+days)).reshape(-1, 1))
        predictions[metric] = {
            'current': df_sorted[metric].iloc[-1],
            'future': future,
            'future_last': future[-1],
            'trend': 'up' if future[-1] > df_sorted[metric].iloc[-1] else 'down'
        }
    return predictions

def calculate_grade(df):
    latest = df.iloc[-1]
    walk_pct = (latest['walk'] + latest['bike']) / latest['total_students'] * 100
    total_waste = latest['food_waste_lbs'] + latest['recycling_lbs']
    waste_pct = (latest['recycling_lbs'] / total_waste * 100) if total_waste > 0 else 0
    energy_score = max(0, 100 - (latest['lights_left_on'] * 10))
    overall = (walk_pct * 0.3 + waste_pct * 0.2 + energy_score * 0.3 + min(100, latest['trees_planted'] * 2))
    if overall > 80: return 'A', overall, '#2e8b57'
    if overall > 60: return 'B', overall, '#3b82f6'
    if overall > 40: return 'C', overall, '#f59e0b'
    if overall > 20: return 'D', overall, '#ef4444'
    return 'F', overall, '#dc2626'

# ============================================================
# PROFESSIONAL CSS
# ============================================================
def get_css(dark_mode):
    if dark_mode:
        return """
        <style>
        /* Reset */
        .stApp { background: #0a0a12; }
        .stApp header { background: rgba(10,10,18,0.8); backdrop-filter: blur(10px); }
        
        /* Typography */
        h1, h2, h3, h4, .stMarkdown, .stText, label, .stMetric label {
            color: #f0f3f8 !important;
            font-family: 'Inter', -apple-system, sans-serif;
        }
        
        /* Metric Cards */
        .metric-card {
            background: rgba(255,255,255,0.04);
            border: 1px solid rgba(255,255,255,0.06);
            border-radius: 16px;
            padding: 1.5rem;
            text-align: center;
            transition: all 0.3s ease;
            backdrop-filter: blur(10px);
        }
        .metric-card:hover {
            background: rgba(255,255,255,0.08);
            transform: translateY(-2px);
        }
        .metric-card .value {
            font-size: 2.5rem;
            font-weight: 700;
            letter-spacing: -0.02em;
        }
        .metric-card .label {
            font-size: 0.85rem;
            opacity: 0.7;
            margin-top: 0.25rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }
        .metric-card .sub {
            font-size: 0.7rem;
            opacity: 0.5;
            margin-top: 0.5rem;
        }
        
        /* Feature Cards (like F-Secure) */
        .feature-card {
            background: rgba(255,255,255,0.03);
            border: 1px solid rgba(255,255,255,0.06);
            border-radius: 16px;
            padding: 1.5rem;
            transition: all 0.3s ease;
            height: 100%;
        }
        .feature-card:hover {
            background: rgba(255,255,255,0.06);
            transform: translateY(-4px);
        }
        .feature-card .icon { font-size: 2rem; margin-bottom: 0.5rem; }
        .feature-card .title { font-weight: 600; font-size: 1.1rem; margin-bottom: 0.25rem; }
        .feature-card .desc { opacity: 0.6; font-size: 0.9rem; }
        
        /* Buttons */
        .stButton > button {
            background: linear-gradient(135deg, #2e8b57, #3cb371) !important;
            color: white !important;
            border: none !important;
            border-radius: 30px !important;
            padding: 0.6rem 1.8rem !important;
            font-weight: 600 !important;
            transition: all 0.3s ease !important;
        }
        .stButton > button:hover {
            transform: scale(1.02);
            box-shadow: 0 8px 30px rgba(46,139,87,0.3);
        }
        
        /* Anomaly cards */
        .anomaly-card {
            background: rgba(239,68,68,0.1);
            border: 1px solid rgba(239,68,68,0.2);
            border-radius: 12px;
            padding: 0.75rem 1rem;
            margin: 0.25rem 0;
        }
        
        /* Sidebar */
        [data-testid="stSidebar"] {
            background: rgba(10,10,18,0.95);
            border-right: 1px solid rgba(255,255,255,0.05);
        }
        [data-testid="stSidebar"] * { color: #f0f3f8 !important; }
        
        /* Toggle */
        .stToggle { color: #f0f3f8 !important; }
        </style>
        """
    else:
        return """
        <style>
        /* Reset */
        .stApp { background: #f8fafc; }
        .stApp header { background: rgba(255,255,255,0.8); backdrop-filter: blur(10px); }
        
        /* Typography */
        h1, h2, h3, h4, .stMarkdown, .stText, label, .stMetric label {
            color: #0a0a12 !important;
            font-family: 'Inter', -apple-system, sans-serif;
        }
        
        /* Metric Cards */
        .metric-card {
            background: white;
            border: 1px solid rgba(0,0,0,0.04);
            border-radius: 16px;
            padding: 1.5rem;
            text-align: center;
            transition: all 0.3s ease;
            box-shadow: 0 1px 3px rgba(0,0,0,0.02);
        }
        .metric-card:hover {
            box-shadow: 0 8px 30px rgba(0,0,0,0.06);
            transform: translateY(-2px);
        }
        .metric-card .value {
            font-size: 2.5rem;
            font-weight: 700;
            letter-spacing: -0.02em;
        }
        .metric-card .label {
            font-size: 0.85rem;
            opacity: 0.6;
            margin-top: 0.25rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }
        .metric-card .sub {
            font-size: 0.7rem;
            opacity: 0.4;
            margin-top: 0.5rem;
        }
        
        /* Feature Cards */
        .feature-card {
            background: white;
            border: 1px solid rgba(0,0,0,0.04);
            border-radius: 16px;
            padding: 1.5rem;
            transition: all 0.3s ease;
            height: 100%;
            box-shadow: 0 1px 3px rgba(0,0,0,0.02);
        }
        .feature-card:hover {
            box-shadow: 0 8px 30px rgba(0,0,0,0.06);
            transform: translateY(-4px);
        }
        .feature-card .icon { font-size: 2rem; margin-bottom: 0.5rem; }
        .feature-card .title { font-weight: 600; font-size: 1.1rem; margin-bottom: 0.25rem; }
        .feature-card .desc { opacity: 0.6; font-size: 0.9rem; }
        
        /* Buttons */
        .stButton > button {
            background: linear-gradient(135deg, #2e8b57, #3cb371) !important;
            color: white !important;
            border: none !important;
            border-radius: 30px !important;
            padding: 0.6rem 1.8rem !important;
            font-weight: 600 !important;
            transition: all 0.3s ease !important;
        }
        .stButton > button:hover {
            transform: scale(1.02);
            box-shadow: 0 8px 30px rgba(46,139,87,0.2);
        }
        
        /* Anomaly cards */
        .anomaly-card {
            background: rgba(239,68,68,0.05);
            border: 1px solid rgba(239,68,68,0.1);
            border-radius: 12px;
            padding: 0.75rem 1rem;
            margin: 0.25rem 0;
        }
        
        /* Sidebar */
        [data-testid="stSidebar"] {
            background: white;
            border-right: 1px solid rgba(0,0,0,0.04);
        }
        [data-testid="stSidebar"] * { color: #0a0a12 !important; }
        </style>
        """

st.markdown(get_css(st.session_state.dark_mode), unsafe_allow_html=True)

# ============================================================
# HEADER
# ============================================================
col1, col2, col3 = st.columns([1, 3, 1])
with col2:
    st.markdown("""
    <div style="text-align: center; padding: 0.5rem 0 1rem 0;">
        <div style="font-size: 2.8rem; font-weight: 700; letter-spacing: -0.03em; background: linear-gradient(135deg, #2e8b57, #86efac); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
            Eco-School AI
        </div>
        <div style="opacity: 0.6; font-size: 1rem; margin-top: -0.25rem;">
            Intelligence for a greener campus
        </div>
    </div>
    """, unsafe_allow_html=True)

# ============================================================
# SIDEBAR
# ============================================================
with st.sidebar:
    st.markdown("### 🌱 Navigation")
    pages = ["📊 Dashboard", "📥 Data Entry", "📈 Trends", "🤖 AI Predictions", "📋 Action Plan", "🌡️ Simulator"]
    selected_page = st.radio("", pages, label_visibility="collapsed")
    
    st.markdown("---")
    
    # Dark mode toggle
    new_mode = st.toggle("🌙 Dark Mode", value=st.session_state.dark_mode)
    if new_mode != st.session_state.dark_mode:
        st.session_state.dark_mode = new_mode
        st.rerun()
    
    st.markdown("---")
    st.caption("Made for USAII Hackathon 2026")

# ============================================================
# PAGE: DASHBOARD
# ============================================================
if selected_page == "📊 Dashboard":
    latest = df.iloc[-1]
    grade, score, grade_color = calculate_grade(df)
    anomalies = detect_anomalies(df)
    walk_pct = (latest['walk'] + latest['bike']) / latest['total_students'] * 100
    total_waste = latest['food_waste_lbs'] + latest['recycling_lbs']
    waste_pct = (latest['recycling_lbs'] / total_waste * 100) if total_waste > 0 else 0
    
    # Metrics Row
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="value" style="color: {grade_color};">{grade}</div>
            <div class="label">Overall Grade</div>
            <div class="sub">{score:.0f}/100</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="value" style="color: #3b82f6;">{walk_pct:.0f}%</div>
            <div class="label">🚶 Walk/Bike</div>
            <div class="sub">Goal: 50%</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        color = '#ef4444' if latest['lights_left_on'] > 4 else '#2e8b57'
        st.markdown(f"""
        <div class="metric-card">
            <div class="value" style="color: {color};">{latest['lights_left_on']}</div>
            <div class="label">💡 Lights On</div>
            <div class="sub">{'🔴 High' if latest['lights_left_on'] > 4 else '✅ Good'}</div>
        </div>
        """, unsafe_allow_html=True)
    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <div class="value" style="color: #8b5cf6;">{waste_pct:.0f}%</div>
            <div class="label">♻️ Waste Diverted</div>
            <div class="sub">Goal: 70%</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Feature Cards (like F-Secure)
    st.markdown("---")
    st.markdown("### 🌿 Your School's Environmental Profile")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        <div class="feature-card">
            <div class="icon">🌳</div>
            <div class="title">Tree Canopy</div>
            <div class="desc">""" + f"{latest['trees_planted']} trees planted on campus" + """</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="feature-card">
            <div class="icon">🚮</div>
            <div class="title">Waste Management</div>
            <div class="desc">""" + f"{waste_pct:.0f}% diverted from landfill" + """</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div class="feature-card">
            <div class="icon">⚡</div>
            <div class="title">Energy Efficiency</div>
            <div class="desc">""" + f"{latest['lights_left_on']} classrooms with lights on" + """</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Anomalies
    if anomalies:
        st.markdown("---")
        st.markdown("### ⚠️ AI-Detected Issues")
        for a in anomalies:
            st.markdown(f'<div class="anomaly-card">🚨 {a}</div>', unsafe_allow_html=True)
    
    # Fun insight
    st.markdown("---")
    st.markdown("### 💡 Quick Insight")
    if grade == 'A':
        st.success("🌟 Your school is a sustainability leader! Keep inspiring others.")
    elif grade == 'B':
        st.info("💪 Great progress! A few small changes could make you a leader.")
    elif grade == 'C':
        st.warning("📈 Good foundation. Focus on energy and waste for biggest impact.")
    else:
        st.error("🚀 Start with one action: assign Energy Monitors in every classroom.")

# ============================================================
# PAGE: DATA ENTRY
# ============================================================
elif selected_page == "📥 Data Entry":
    st.markdown("### 📥 Log Today's Data")
    st.caption("Enter your school's daily environmental metrics.")
    
    with st.form("data_form"):
        col1, col2 = st.columns(2)
        with col1:
            walk = st.number_input("🚶 Walkers", min_value=0, value=150)
            bike = st.number_input("🚲 Bikers", min_value=0, value=48)
            car = st.number_input("🚗 Car dropoffs", min_value=0, value=48)
        with col2:
            lights = st.number_input("💡 Lights left on", min_value=0, value=3)
            food = st.number_input("🍎 Food waste (lbs)", min_value=0.0, value=20.0)
            recycle = st.number_input("♻️ Recycling (lbs)", min_value=0.0, value=28.0)
        
        date = st.date_input("Date", datetime.now())
        trees = st.number_input("🌳 New trees planted", min_value=0, value=0)
        
        submitted = st.form_submit_button("💾 Save Data")
        if submitted:
            new_row = {
                'date': date, 'walk': walk, 'bike': bike, 'car': car,
                'bus': 188, 'lights_left_on': lights, 'food_waste_lbs': food,
                'recycling_lbs': recycle, 'paper_reams': 7,
                'trees_planted': trees, 'total_students': walk + bike + car + 188
            }
            df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
            df.to_csv(DATA_FILE, index=False)
            st.success("✅ Data saved successfully!")
            st.balloons()

# ============================================================
# PAGE: TRENDS
# ============================================================
elif selected_page == "📈 Trends":
    st.markdown("### 📈 Trends Over Time")
    st.caption("Visualize your school's environmental journey.")
    
    df_sorted = df.sort_values('date')
    
    col1, col2 = st.columns(2)
    with col1:
        fig = px.line(df_sorted, x='date', y=['walk', 'bike'], 
                      title='Active Transportation',
                      color_discrete_map={'walk': '#2e8b57', 'bike': '#3b82f6'})
        fig.update_layout(hovermode='x unified', height=350)
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        fig = px.line(df_sorted, x='date', y=['food_waste_lbs', 'recycling_lbs'],
                      title='Waste Management',
                      color_discrete_map={'food_waste_lbs': '#f59e0b', 'recycling_lbs': '#2e8b57'})
        fig.update_layout(hovermode='x unified', height=350)
        st.plotly_chart(fig, use_container_width=True)
    
    col3, col4 = st.columns(2)
    with col3:
        fig = px.line(df_sorted, x='date', y='lights_left_on', title='Energy Waste')
        fig.update_traces(line_color='#ef4444')
        fig.update_layout(height=350)
        st.plotly_chart(fig, use_container_width=True)
    with col4:
        fig = px.line(df_sorted, x='date', y='trees_planted', title='Trees Planted')
        fig.update_traces(line_color='#2e8b57')
        fig.update_layout(height=350)
        st.plotly_chart(fig, use_container_width=True)

# ============================================================
# PAGE: AI PREDICTIONS
# ============================================================
elif selected_page == "🤖 AI Predictions":
    st.markdown("### 🤖 AI Predictions")
    st.caption("14-day forecast based on your school's data.")
    
    if len(df) > 3:
        preds = predict_trends(df)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            w = preds['walk']
            st.metric("🚶 Walkers", f"{w['current']:.0f} → {w['future_last']:.0f}",
                      delta=f"{w['future_last'] - w['current']:.0f}")
        with col2:
            w = preds['food_waste_lbs']
            st.metric("🍎 Food Waste", f"{w['current']:.0f} → {w['future_last']:.0f}",
                      delta=f"{w['future_last'] - w['current']:.0f}")
        with col3:
            w = preds['recycling_lbs']
            st.metric("♻️ Recycling", f"{w['current']:.0f} → {w['future_last']:.0f}",
                      delta=f"{w['future_last'] - w['current']:.0f}")
        
        # Prediction chart
        df_sorted = df.sort_values('date')
        future_dates = [df_sorted['date'].iloc[-1] + timedelta(days=i+1) for i in range(14)]
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df_sorted['date'], y=df_sorted['walk'], 
                                 mode='lines+markers', name='Actual', line=dict(color='#2e8b57')))
        fig.add_trace(go.Scatter(x=future_dates, y=preds['walk']['future'], 
                                 mode='lines', name='AI Predicted', line=dict(color='#3b82f6', dash='dash')))
        fig.update_layout(hovermode='x unified', height=400)
        st.plotly_chart(fig, use_container_width=True)
        
        if preds['walk']['trend'] == 'up':
            st.success("📈 Walking is trending up! Keep encouraging students.")
        else:
            st.warning("📉 Walking is trending down. Time for a campaign.")
    else:
        st.warning("📊 Enter at least 4 days of data for predictions.")

# ============================================================
# PAGE: ACTION PLAN
# ============================================================
elif selected_page == "📋 Action Plan":
    st.markdown("### 📋 AI-Generated Action Plan")
    st.caption("Prioritized actions for your school.")
    
    latest = df.iloc[-1]
    walk_pct = (latest['walk'] + latest['bike']) / latest['total_students'] * 100
    waste_avg = df['food_waste_lbs'].mean()
    total_waste = latest['food_waste_lbs'] + latest['recycling_lbs']
    waste_pct = (latest['recycling_lbs'] / total_waste * 100) if total_waste > 0 else 0
    
    # Priority cards
    priorities = [
        {
            "icon": "💡", "title": "Energy Efficiency",
            "problem": f"{latest['lights_left_on']} classrooms leave lights on.",
            "impact": f"Save ${latest['lights_left_on'] * 10:.0f}/month.",
            "action": "Assign Energy Monitors in each classroom."
        },
        {
            "icon": "🚶", "title": "Transportation",
            "problem": f"Only {walk_pct:.0f}% walk/bike.",
            "impact": "Reduce 500 lbs CO2/week.",
            "action": "Launch 'Walk & Roll Wednesday'."
        },
        {
            "icon": "🍎", "title": "Food Waste",
            "problem": f"{latest['food_waste_lbs']:.0f} lbs food waste daily.",
            "impact": "Divert 5,000 lbs/year to hungry people.",
            "action": "Start a Share Table program."
        }
    ]
    
    for p in priorities:
        st.markdown(f"""
        <div style="background: {'rgba(255,255,255,0.03)' if st.session_state.dark_mode else '#f8faf8'}; 
                    border-radius: 12px; padding: 1rem; margin: 0.75rem 0; 
                    border-left: 4px solid #2e8b57;">
            <h4>{p['icon']} {p['title']}</h4>
            <p style="margin: 0.25rem 0; opacity: 0.7;">{p['problem']}</p>
            <p style="margin: 0.25rem 0;"><strong>Impact:</strong> {p['impact']}</p>
            <p style="margin: 0.25rem 0;"><strong>Action:</strong> {p['action']}</p>
        </div>
        """, unsafe_allow_html=True)

# ============================================================
# PAGE: SIMULATOR
# ============================================================
elif selected_page == "🌡️ Simulator":
    st.markdown("### 🌡️ What If Simulator")
    st.caption("See the impact of your actions before you take them.")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### 🌳 Plant Trees")
        trees = st.slider("Number of trees:", 0, 100, 20, step=5)
        st.metric("🌡️ Temperature Reduction", f"-{trees * 0.3:.1f}°F")
        st.caption(f"🌿 Absorbs {trees * 48} lbs CO2/year")
    
    with col2:
        st.markdown("#### 🚶 Increase Walking")
        pct = st.slider("Increase walk/bike by:", 0, 100, 20, step=5)
        cars = int(54 * pct / 100)
        st.metric("🚗 Fewer Cars Daily", f"-{cars}")
        st.caption(f"🌿 Saves {cars * 5} lbs CO2/day")
    
    st.markdown("---")
    score = (trees * 0.5 + pct * 0.5) / 100
    st.progress(min(1.0, score))
    st.caption(f"🌱 Overall impact: {min(100, trees + pct):.0f}/100")

# ============================================================
# FOOTER
# ============================================================
st.markdown("---")
st.caption("🌱 Eco-School AI · Made with ❤️ for USAII Hackathon 2026")