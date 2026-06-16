# ===== SCHOOL AI DASHBOARD — FUN & INTERACTIVE VERSION =====
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
    page_title="Eco-School AI Dashboard",
    page_icon="🏫",
    layout="wide"
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
        required_cols = ['walk', 'bike', 'car', 'bus', 'lights_left_on', 
                        'food_waste_lbs', 'recycling_lbs', 'paper_reams', 'trees_planted', 'total_students']
        missing_cols = [col for col in required_cols if col not in df.columns]
        if missing_cols:
            df = generate_demo_data()
        return df
    except:
        return generate_demo_data()

df = load_data()

# ===== AI FUNCTIONS =====
def detect_anomalies(df):
    anomalies = []
    latest = df.iloc[-1]
    if latest['lights_left_on'] > 5:
        anomalies.append(f"💡 Lights left on: {latest['lights_left_on']} classrooms. Wastes ${latest['lights_left_on'] * 10:.0f}/month.")
    waste_avg = df['food_waste_lbs'].mean()
    if latest['food_waste_lbs'] > waste_avg + df['food_waste_lbs'].std():
        anomalies.append(f"🍎 High food waste: {latest['food_waste_lbs']:.0f} lbs vs avg {waste_avg:.0f} lbs.")
    walk_avg = df['walk'].mean()
    if latest['walk'] < walk_avg - df['walk'].std():
        anomalies.append(f"🚶 Low walking: {latest['walk']:.0f} walkers vs avg {walk_avg:.0f}.")
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
# FUN STUFF: Emoji Reactions & Encouragement
# ============================================================
def get_encouragement(grade):
    if grade == 'A':
        return "🌟 Amazing! You're a sustainability superstar! 🎉"
    elif grade == 'B':
        return "💪 Great job! Keep pushing for that A! 🚀"
    elif grade == 'C':
        return "📈 Good start! There's room to grow. Let's go! 🌱"
    elif grade == 'D':
        return "😬 Oof! Time to take action! You've got this! 🔥"
    else:
        return "🚨 Urgent! Your school needs help! Start with small steps! 💚"

def get_mood_emoji(grade):
    if grade == 'A': return "😎"
    elif grade == 'B': return "🙂"
    elif grade == 'C': return "😐"
    elif grade == 'D': return "😰"
    else: return "😱"

# ============================================================
# CSS — FULL DARK MODE SUPPORT
# ============================================================
def get_css(dark_mode):
    if dark_mode:
        return """
        <style>
        .stApp { background: #0a0a1a; }
        .stMarkdown, .stText, label, .stMetric label { color: #f0f3f8 !important; }
        .stMetric div[data-testid="stMetricValue"] { color: #86efac !important; }
        .stMetric div[data-testid="stMetricDelta"] { color: #4ade80 !important; }
        .stButton > button { background: linear-gradient(135deg, #86efac, #4ade80); color: #0a0a1a; font-weight: bold; border-radius: 30px; transition: 0.3s; }
        .stButton > button:hover { transform: scale(1.05); box-shadow: 0 0 30px rgba(134,239,172,0.3); }
        .metric-card { background: #1a1a2e; border-radius: 20px; padding: 1.5rem; margin-bottom: 1rem; text-align: center; border: 1px solid #2d3748; box-shadow: 0 4px 20px rgba(0,0,0,0.3); transition: 0.3s; }
        .metric-card:hover { transform: translateY(-5px); box-shadow: 0 8px 40px rgba(134,239,172,0.1); }
        .anomaly-card { background: #2d1a1a; border-radius: 16px; padding: 1rem; margin-bottom: 0.5rem; border-left: 4px solid #ef4444; }
        .fun-fact { background: #1a2d2a; border-radius: 16px; padding: 1rem; border-left: 4px solid #86efac; margin: 1rem 0; }
        [data-testid="stSidebar"] { background: #0f0f1f; }
        [data-testid="stSidebar"] * { color: #f0f3f8 !important; }
        </style>
        """
    else:
        return """
        <style>
        .stApp { background: linear-gradient(135deg, #f0f4f8, #e2e8f0); }
        .stMarkdown, .stText, label, .stMetric label { color: #1a202c !important; }
        .stMetric div[data-testid="stMetricValue"] { color: #2e8b57 !important; }
        .stMetric div[data-testid="stMetricDelta"] { color: #38a169 !important; }
        .stButton > button { background: linear-gradient(135deg, #2e8b57, #38a169); color: white; font-weight: bold; border-radius: 30px; transition: 0.3s; }
        .stButton > button:hover { transform: scale(1.05); box-shadow: 0 0 30px rgba(46,139,87,0.3); }
        .metric-card { background: white; border-radius: 20px; padding: 1.5rem; margin-bottom: 1rem; text-align: center; box-shadow: 0 4px 20px rgba(0,0,0,0.06); transition: 0.3s; }
        .metric-card:hover { transform: translateY(-5px); box-shadow: 0 8px 40px rgba(46,139,87,0.1); }
        .anomaly-card { background: #fff5f0; border-radius: 16px; padding: 1rem; margin-bottom: 0.5rem; border-left: 4px solid #ef4444; }
        .fun-fact { background: #f0fdf4; border-radius: 16px; padding: 1rem; border-left: 4px solid #2e8b57; margin: 1rem 0; }
        [data-testid="stSidebar"] { background: #ffffff; }
        [data-testid="stSidebar"] * { color: #1a202c !important; }
        </style>
        """

# ===== APPLY CSS =====
st.markdown(get_css(st.session_state.dark_mode), unsafe_allow_html=True)

# ============================================================
# HEADER WITH DARK MODE TOGGLE
# ============================================================
col1, col2 = st.columns([4, 1])
with col1:
    st.markdown("""
    <div style="display: flex; align-items: center; gap: 12px;">
        <span style="font-size: 2.5rem;">🏫</span>
        <div>
            <h1 style="margin: 0; background: linear-gradient(135deg, #2e8b57, #86efac); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">Eco-School AI</h1>
            <p style="margin: 0; color: #a0aec0; font-size: 0.9rem;">Make your school green with AI ✨</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
with col2:
    new_mode = st.toggle("🌙 Dark", value=st.session_state.dark_mode)
    if new_mode != st.session_state.dark_mode:
        st.session_state.dark_mode = new_mode
        st.rerun()

# ============================================================
# SIDEBAR NAV
# ============================================================
pages = ["📊 Dashboard", "📥 Data Entry", "📈 Trends", "🤖 AI Predictions", "📋 Action Plan", "🌡️ Simulator"]
selected_page = st.sidebar.radio("🚀 Navigate", pages)
st.sidebar.markdown("---")
st.sidebar.caption("🏫 Made for USAII Hackathon 2026")

# ============================================================
# PAGE 1: DASHBOARD
# ============================================================
if selected_page == "📊 Dashboard":
    st.subheader("📊 AI-Powered Dashboard")
    st.caption("AI detects problems, predicts trends, and suggests actions — automatically!")
    
    latest = df.iloc[-1]
    grade, score, grade_color = calculate_grade(df)
    anomalies = detect_anomalies(df)
    walk_pct = (latest['walk'] + latest['bike']) / latest['total_students'] * 100
    total_waste = latest['food_waste_lbs'] + latest['recycling_lbs']
    waste_pct = (latest['recycling_lbs'] / total_waste * 100) if total_waste > 0 else 0
    
    # ===== FUN EMOJI =====
    st.markdown(f"""
    <div style="text-align: center; padding: 1rem; font-size: 1.2rem;">
        {get_mood_emoji(grade)} <strong>{get_encouragement(grade)}</strong>
    </div>
    """, unsafe_allow_html=True)
    
    # ===== METRICS =====
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div style="font-size: 3rem; font-weight: 800; color: {grade_color};">{grade}</div>
            <div>📊 Overall Grade</div>
            <div style="font-size: 0.8rem; opacity: 0.7;">Score: {score:.0f}/100</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div style="font-size: 2.5rem; font-weight: 800; color: #3b82f6;">{walk_pct:.0f}%</div>
            <div>🚶 Walk/Bike</div>
            <div style="font-size: 0.8rem; opacity: 0.7;">Goal: 50%</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        color = '#ef4444' if latest['lights_left_on'] > 4 else '#2e8b57'
        st.markdown(f"""
        <div class="metric-card">
            <div style="font-size: 2.5rem; font-weight: 800; color: {color};">{latest['lights_left_on']}</div>
            <div>💡 Lights Left On</div>
            <div style="font-size: 0.8rem; opacity: 0.7;">{'🔴 Too many' if latest['lights_left_on'] > 4 else '✅ Good'}</div>
        </div>
        """, unsafe_allow_html=True)
    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <div style="font-size: 2.5rem; font-weight: 800; color: #8b5cf6;">{waste_pct:.0f}%</div>
            <div>♻️ Waste Diverted</div>
            <div style="font-size: 0.8rem; opacity: 0.7;">Goal: 70%</div>
        </div>
        """, unsafe_allow_html=True)
    
    # ===== FUN FACT =====
    fun_facts = [
        "🌳 One tree absorbs 48 lbs of CO2 per year!",
        "🚶 Walking 1 mile instead of driving saves 1 lb of CO2!",
        "💡 Turning off 1 light saves $10/year!",
        "♻️ Recycling 1 ton of paper saves 17 trees!",
        "🍎 Food waste in landfills creates methane — 25x worse than CO2!"
    ]
    st.markdown(f"""
    <div class="fun-fact">
        💡 <strong>Did you know?</strong> {random.choice(fun_facts)}
    </div>
    """, unsafe_allow_html=True)
    
    # ===== ANOMALIES =====
    st.markdown("---")
    st.subheader("🚨 AI-Detected Anomalies")
    if anomalies:
        for anomaly in anomalies:
            st.markdown(f'<div class="anomaly-card">⚠️ {anomaly}</div>', unsafe_allow_html=True)
    else:
        st.success("✅ No anomalies detected! Your school is doing great! 🌟")

# ============================================================
# PAGE 2: DATA ENTRY
# ============================================================
elif selected_page == "📥 Data Entry":
    st.subheader("📥 Enter Today's Data")
    st.caption("Log your school's daily environmental data. Every entry helps AI learn! 📊")
    
    with st.form("data_entry_form"):
        col1, col2 = st.columns(2)
        with col1:
            walk = st.number_input("🚶 Students who walked today", min_value=0, value=150)
            bike = st.number_input("🚲 Students who biked today", min_value=0, value=48)
            car = st.number_input("🚗 Students dropped by car", min_value=0, value=48)
            bus = st.number_input("🚌 Students who took bus", min_value=0, value=188)
        with col2:
            lights_left = st.number_input("💡 Classrooms with lights left on", min_value=0, value=3)
            food_waste = st.number_input("🍎 Food waste (lbs)", min_value=0.0, value=20.0)
            recycling = st.number_input("♻️ Recycling collected (lbs)", min_value=0.0, value=28.0)
            paper = st.number_input("📄 Reams of paper used", min_value=0.0, value=7.0)
        total_students = walk + bike + car + bus
        st.caption(f"👥 Total Students: {total_students}")
        date = st.date_input("📅 Date", datetime.now())
        trees_planted = st.number_input("🌳 New trees planted today", min_value=0, value=0)
        
        submitted = st.form_submit_button("💾 Save Data 🌱", type="primary")
        if submitted:
            new_row = {
                'date': date, 'walk': walk, 'bike': bike, 'car': car, 'bus': bus,
                'lights_left_on': lights_left, 'food_waste_lbs': food_waste,
                'recycling_lbs': recycling, 'paper_reams': paper,
                'trees_planted': trees_planted, 'total_students': total_students
            }
            df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
            df.to_csv(DATA_FILE, index=False)
            st.success("✅ Data saved! 🌍 Keep up the great work!")
            st.balloons()

# ============================================================
# PAGE 3: TRENDS
# ============================================================
elif selected_page == "📈 Trends":
    st.subheader("📈 Trends Over Time")
    st.caption("Watch your school's environmental impact evolve! 📊")
    
    df_sorted = df.sort_values('date')
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### 🚶 Walk/Bike Trends")
        fig = px.line(df_sorted, x='date', y=['walk', 'bike'], title='Students Walking/Biking to School',
                      labels={'value': 'Students', 'variable': 'Mode'},
                      color_discrete_map={'walk': '#2e8b57', 'bike': '#3b82f6'})
        fig.update_layout(hovermode='x unified', height=350)
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        st.markdown("#### 🗑️ Waste Trends")
        waste_df = df_sorted.melt(id_vars=['date'], value_vars=['food_waste_lbs', 'recycling_lbs'],
                                  var_name='Type', value_name='Pounds')
        fig = px.bar(waste_df, x='date', y='Pounds', color='Type',
                     color_discrete_map={'food_waste_lbs': '#f59e0b', 'recycling_lbs': '#2e8b57'},
                     title='Daily Food Waste vs Recycling')
        fig.update_layout(barmode='group', height=350)
        st.plotly_chart(fig, use_container_width=True)
    
    col3, col4 = st.columns(2)
    with col3:
        st.markdown("#### 💡 Energy")
        fig = px.line(df_sorted, x='date', y='lights_left_on', title='Classrooms with Lights Left On')
        fig.update_traces(line_color='#ef4444')
        fig.update_layout(height=350)
        st.plotly_chart(fig, use_container_width=True)
    with col4:
        st.markdown("#### 🌳 Trees Planted")
        fig = px.line(df_sorted, x='date', y='trees_planted', title='Cumulative Trees Planted')
        fig.update_traces(line_color='#2e8b57')
        fig.update_layout(height=350)
        st.plotly_chart(fig, use_container_width=True)

# ============================================================
# PAGE 4: AI PREDICTIONS
# ============================================================
elif selected_page == "🤖 AI Predictions":
    st.subheader("🤖 AI Predictions — Next 14 Days")
    st.caption("Based on Linear Regression, here's what we expect if current trends continue.")
    
    if len(df) > 3:
        predictions = predict_trends(df)
        col1, col2, col3 = st.columns(3)
        with col1:
            walk_pred = predictions['walk']
            st.metric("🚶 Walkers", f"{walk_pred['current']:.0f} → {walk_pred['future_last']:.0f}",
                      delta=f"{walk_pred['future_last'] - walk_pred['current']:.0f}")
        with col2:
            waste_pred = predictions['food_waste_lbs']
            st.metric("🍎 Food Waste", f"{waste_pred['current']:.0f} → {waste_pred['future_last']:.0f}",
                      delta=f"{waste_pred['future_last'] - waste_pred['current']:.0f}")
        with col3:
            recycle_pred = predictions['recycling_lbs']
            st.metric("♻️ Recycling", f"{recycle_pred['current']:.0f} → {recycle_pred['future_last']:.0f}",
                      delta=f"{recycle_pred['future_last'] - recycle_pred['current']:.0f}")
        
        st.markdown("#### 📊 AI Prediction: Walkers Trend")
        df_sorted = df.sort_values('date')
        future_dates = [df_sorted['date'].iloc[-1] + timedelta(days=i+1) for i in range(14)]
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df_sorted['date'], y=df_sorted['walk'], mode='lines+markers', name='Actual', line=dict(color='#2e8b57')))
        fig.add_trace(go.Scatter(x=future_dates, y=predictions['walk']['future'], mode='lines', name='AI Predicted', line=dict(color='#3b82f6', dash='dash')))
        fig.update_layout(hovermode='x unified', height=400)
        st.plotly_chart(fig, use_container_width=True)
        
        if predictions['walk']['trend'] == 'up':
            st.success("📈 Walking is trending UP! Keep encouraging students! 🌟")
        else:
            st.warning("📉 Walking is trending DOWN. Time for a campaign! 🚀")
    else:
        st.warning("📊 Not enough data for predictions. Enter at least 4 days of data.")

# ============================================================
# PAGE 5: ACTION PLAN
# ============================================================
elif selected_page == "📋 Action Plan":
    st.subheader("📋 AI-Generated Action Plan")
    st.caption("Here are the highest-impact actions for your school.")
    
    latest = df.iloc[-1]
    walk_pct = (latest['walk'] + latest['bike']) / latest['total_students'] * 100
    waste_avg = df['food_waste_lbs'].mean()
    total_waste = latest['food_waste_lbs'] + latest['recycling_lbs']
    waste_pct = (latest['recycling_lbs'] / total_waste * 100) if total_waste > 0 else 0
    
    # Priority cards with fun styling
    priorities = [
        {
            "icon": "💡",
            "title": "Energy Efficiency",
            "color": "#ef4444",
            "problem": f"{latest['lights_left_on']} classrooms leave lights on daily.",
            "impact": f"Save ${latest['lights_left_on'] * 10:.0f}/month.",
            "action": "Assign an 'Energy Monitor' in each classroom."
        },
        {
            "icon": "🚶",
            "title": "Transportation",
            "color": "#f59e0b",
            "problem": f"Only {walk_pct:.0f}% walk/bike to school.",
            "impact": "Reduce 500 lbs CO2/week.",
            "action": "Launch a 'Walk & Roll Wednesday' program."
        },
        {
            "icon": "🍎",
            "title": "Food Waste",
            "color": "#8b5cf6",
            "problem": f"{latest['food_waste_lbs']:.0f} lbs food waste vs {waste_avg:.0f} lbs avg.",
            "impact": "Divert 5,000 lbs/year to hungry people.",
            "action": "Start a Share Table program."
        },
        {
            "icon": "♻️",
            "title": "Recycling",
            "color": "#3b82f6",
            "problem": f"{waste_pct:.0f}% waste diverted. Goal: 70%.",
            "impact": "Save 1 tree per 500 lbs recycled.",
            "action": "Add more recycling bins in hallways."
        }
    ]
    
    for p in priorities:
        st.markdown(f"""
        <div style="background: {'#1a1a2e' if st.session_state.dark_mode else '#f8faf8'}; border-radius: 16px; padding: 1rem; margin: 1rem 0; border-left: 4px solid {p['color']};">
            <h4>{p['icon']} {p['title']}</h4>
            <p><strong>Problem:</strong> {p['problem']}</p>
            <p><strong>Impact:</strong> {p['impact']}</p>
            <p><strong>AI Suggestion:</strong> {p['action']}</p>
        </div>
        """, unsafe_allow_html=True)

# ============================================================
# PAGE 6: SIMULATOR
# ============================================================
elif selected_page == "🌡️ Simulator":
    st.markdown('<div class="section-header">🌡️ What If Simulator</div>', unsafe_allow_html=True)
    st.caption("See the impact of your actions before you take them! 🚀")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### 🌳 Tree Planting Simulator")
        trees = st.slider("Number of trees to plant:", 0, 100, 20, step=5)
        temp_reduction = trees * 0.3
        co2_absorbed = trees * 48
        st.metric("🌡️ Temperature Reduction", f"-{temp_reduction:.1f}°F")
        st.caption(f"🌿 Also absorbs {co2_absorbed} lbs CO2 per year")
    
    with col2:
        st.markdown("#### 🚶 Walk to School Simulator")
        walk_pct = st.slider("Increase walk/bike by:", 0, 100, 20, step=5)
        cars_removed = int(54 * walk_pct / 100)
        co2_saved = cars_removed * 5
        st.metric("🚗 Fewer Solo Cars Daily", f"-{cars_removed}")
        st.caption(f"🌿 Saves {co2_saved} lbs CO2 per day")
    
    st.markdown("---")
    
    # Combined impact
    combined_score = (trees * 0.5 + walk_pct * 0.5)
    st.markdown("### 📊 Combined Impact")
    st.progress(min(100, combined_score) / 100)
    st.caption(f"🌱 Overall impact score: {min(100, combined_score):.0f}/100")
    
    if combined_score > 80:
        st.success("🌟 Amazing! Your school would be a sustainability leader!")
    elif combined_score > 50:
        st.info("💪 Good progress! Keep pushing for more!")
    else:
        st.warning("🌱 Start small! Every tree and every walker counts!")

# ============================================================
# FOOTER
# ============================================================
st.markdown("---")
st.caption("🏫 Eco-School AI · Made with ❤️ for USAII Hackathon 2026 · Data stored locally")