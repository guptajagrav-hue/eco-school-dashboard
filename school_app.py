# ===== SCHOOL AI DASHBOARD — ECO SCHOOL DASHBOARD =====
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
        anomalies.append(f"💡 **Lights left on:** {latest['lights_left_on']} classrooms. Wastes ${latest['lights_left_on'] * 10:.0f}/month.")
    waste_avg = df['food_waste_lbs'].mean()
    if latest['food_waste_lbs'] > waste_avg + df['food_waste_lbs'].std():
        anomalies.append(f"🍎 **High food waste:** {latest['food_waste_lbs']:.0f} lbs vs avg {waste_avg:.0f} lbs.")
    walk_avg = df['walk'].mean()
    if latest['walk'] < walk_avg - df['walk'].std():
        anomalies.append(f"🚶 **Low walking:** {latest['walk']:.0f} walkers vs avg {walk_avg:.0f}.")
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
    st.caption("AI-powered environmental intelligence — minimal effort required")
with col2:
    new_mode = st.toggle("🌙 Dark Mode", value=st.session_state.dark_mode)
    if new_mode != st.session_state.dark_mode:
        st.session_state.dark_mode = new_mode
        st.rerun()

# ===== SIDEBAR NAV =====
pages = ["📊 Dashboard", "📥 Data Entry", "📈 Trends", "🤖 AI Predictions", "📋 Action Plan", "🌡️ Simulator"]
selected_page = st.sidebar.radio("Navigate", pages)
st.sidebar.markdown("---")
st.sidebar.caption("🏫 Made for USAII Hackathon 2026")

# ============================================================
# PAGE 1: DASHBOARD
# ============================================================
if selected_page == "📊 Dashboard":
    st.subheader("📊 AI-Powered Dashboard")
    st.caption("AI automatically detects problems, predicts trends, and suggests actions.")
    
    latest = df.iloc[-1]
    grade, score, grade_color = calculate_grade(df)
    anomalies = detect_anomalies(df)
    walk_pct = (latest['walk'] + latest['bike']) / latest['total_students'] * 100
    total_waste = latest['food_waste_lbs'] + latest['recycling_lbs']
    waste_pct = (latest['recycling_lbs'] / total_waste * 100) if total_waste > 0 else 0
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"""
        <div class="metric-card" style="border-left: 4px solid {grade_color};">
            <div style="font-size: 2rem; font-weight: 800; color: {grade_color};">{grade}</div>
            <div>📊 Overall Grade</div>
            <div style="font-size: 0.7rem;">Score: {score:.0f}/100</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="metric-card" style="border-left: 4px solid #3b82f6;">
            <div style="font-size: 2rem; font-weight: 800; color: #3b82f6;">{walk_pct:.0f}%</div>
            <div>🚶 Walk/Bike</div>
            <div style="font-size: 0.7rem;">Goal: 50%</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
        <div class="metric-card" style="border-left: 4px solid {'#ef4444' if latest['lights_left_on'] > 4 else '#2e8b57'};">
            <div style="font-size: 2rem; font-weight: 800; color: {'#ef4444' if latest['lights_left_on'] > 4 else '#2e8b57'};">{latest['lights_left_on']}</div>
            <div>💡 Lights Left On</div>
            <div style="font-size: 0.7rem;">{'🔴 Too many' if latest['lights_left_on'] > 4 else '✅ Good'}</div>
        </div>
        """, unsafe_allow_html=True)
    with col4:
        st.markdown(f"""
        <div class="metric-card" style="border-left: 4px solid #8b5cf6;">
            <div style="font-size: 2rem; font-weight: 800; color: #8b5cf6;">{waste_pct:.0f}%</div>
            <div>♻️ Waste Diverted</div>
            <div style="font-size: 0.7rem;">Goal: 70%</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.subheader("🚨 AI-Detected Anomalies")
    if anomalies:
        for anomaly in anomalies:
            st.markdown(f'<div class="anomaly-card">{anomaly}</div>', unsafe_allow_html=True)
    else:
        st.success("✅ No anomalies detected. Your school is performing well!")
    
    st.markdown("---")
    if grade in ['D', 'F']:
        st.error("⚠️ **Your school is failing on environmental metrics.**")
    elif grade == 'C':
        st.warning("⚠️ **Your school is average. Significant room for improvement.**")
    elif grade == 'B':
        st.info("📊 **Your school is doing well but not perfect. Keep pushing.**")
    else:
        st.success("🎉 **Your school is a leader in environmental sustainability!**")

# ============================================================
# PAGE 2: DATA ENTRY
# ============================================================
elif selected_page == "📥 Data Entry":
    st.subheader("📥 Enter Today's Data")
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
        date = st.date_input("Date", datetime.now())
        trees_planted = st.number_input("🌳 New trees planted today", min_value=0, value=0)
        submitted = st.form_submit_button("💾 Save Data", type="primary")
        if submitted:
            new_row = {
                'date': date, 'walk': walk, 'bike': bike, 'car': car, 'bus': bus,
                'lights_left_on': lights_left, 'food_waste_lbs': food_waste,
                'recycling_lbs': recycling, 'paper_reams': paper,
                'trees_planted': trees_planted, 'total_students': total_students
            }
            df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
            df.to_csv(DATA_FILE, index=False)
            st.success("✅ Data saved!")
            st.balloons()

# ============================================================
# PAGE 3: TRENDS
# ============================================================
elif selected_page == "📈 Trends":
    st.subheader("📈 Trends Over Time")
    df_sorted = df.sort_values('date')
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### 🚶 Walk/Bike Trends")
        fig = px.line(df_sorted, x='date', y=['walk', 'bike'], title='Students Walking/Biking to School',
                      labels={'value': 'Students', 'variable': 'Mode'},
                      color_discrete_map={'walk': '#2e8b57', 'bike': '#3b82f6'})
        fig.update_layout(hovermode='x unified')
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        st.markdown("#### 🗑️ Waste Trends")
        waste_df = df_sorted.melt(id_vars=['date'], value_vars=['food_waste_lbs', 'recycling_lbs'],
                                  var_name='Type', value_name='Pounds')
        fig = px.bar(waste_df, x='date', y='Pounds', color='Type',
                     color_discrete_map={'food_waste_lbs': '#f59e0b', 'recycling_lbs': '#2e8b57'})
        fig.update_layout(barmode='group')
        st.plotly_chart(fig, use_container_width=True)
    col3, col4 = st.columns(2)
    with col3:
        st.markdown("#### 💡 Energy")
        fig = px.line(df_sorted, x='date', y='lights_left_on', title='Classrooms with Lights Left On')
        fig.update_traces(line_color='#ef4444')
        st.plotly_chart(fig, use_container_width=True)
    with col4:
        st.markdown("#### 🌳 Trees Planted")
        fig = px.line(df_sorted, x='date', y='trees_planted', title='Cumulative Trees Planted')
        fig.update_traces(line_color='#2e8b57')
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
        fig.update_layout(hovermode='x unified')
        st.plotly_chart(fig, use_container_width=True)
        
        st.info("🤖 **AI Insight:** " + ("Walking is trending UP! Keep encouraging students." if predictions['walk']['trend'] == 'up' else "Walking is trending DOWN. Time for a campaign!"))
    else:
        st.warning("Not enough data for predictions. Enter at least 4 days of data.")

# ============================================================
# PAGE 5: ACTION PLAN
# ============================================================
elif selected_page == "📋 Action Plan":
    st.subheader("📋 AI-Generated Action Plan")
    st.caption("Based on your data, here are the highest-impact actions.")
    
    latest = df.iloc[-1]
    walk_pct = (latest['walk'] + latest['bike']) / latest['total_students'] * 100
    waste_avg = df['food_waste_lbs'].mean()
    total_waste = latest['food_waste_lbs'] + latest['recycling_lbs']
    waste_pct = (latest['recycling_lbs'] / total_waste * 100) if total_waste > 0 else 0
    
    st.markdown("### 🔴 PRIORITY 1: Energy Efficiency")
    if latest['lights_left_on'] > 3:
        st.markdown(f"**Problem:** {latest['lights_left_on']} classrooms leave lights on daily.")
        st.markdown(f"**Impact:** Save ${latest['lights_left_on'] * 10:.0f}/month.")
        st.markdown("**AI Suggestion:** Assign an 'Energy Monitor' in each classroom.")
    else:
        st.success("✅ Lights are being turned off. Keep it up!")
    
    st.markdown("### 🟠 PRIORITY 2: Transportation")
    if walk_pct < 40:
        st.markdown(f"**Problem:** Only {walk_pct:.0f}% walk/bike to school.")
        st.markdown("**Impact:** Reduce 500 lbs CO2/week.")
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
    
    st.markdown("### 🟢 PRIORITY 4: Recycling")
    if waste_pct < 60:
        st.markdown(f"**Problem:** {waste_pct:.0f}% waste diverted. Goal: 70%.")
        st.markdown("**AI Suggestion:** Add more recycling bins in hallways.")
    else:
        st.success("✅ Recycling rate is good. Aim for 70%!")

# ============================================================
# PAGE 6: SIMULATOR (WITH AI TREND PREDICTION)
# ============================================================
elif selected_page == "🌡️ Simulator":
    st.markdown('<div class="section-header">🌡️ What If Simulator</div>', unsafe_allow_html=True)
    
    # Two main simulators
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### 🌳 Tree Planting Simulator")
        trees = st.slider("Number of trees to plant:", 0, 100, 20, step=5)
        temp_reduction = trees * 0.3
        co2_absorbed = trees * 48
        st.metric("Temperature Reduction", f"-{temp_reduction:.1f}°F")
        st.caption(f"🌿 Also absorbs {co2_absorbed} lbs CO2 per year")
    
    with col2:
        st.markdown("#### 🚶 Walk to School Simulator")
        walk_pct = st.slider("Increase walk/bike by:", 0, 100, 20, step=5)
        cars_removed = int(54 * walk_pct / 100)
        co2_saved = cars_removed * 5
        st.metric("Fewer Solo Cars Daily", f"-{cars_removed}")
        st.caption(f"🌿 Saves {co2_saved} lbs CO2 per day")
    
    st.markdown("---")
    
    # ===== AI TREND PREDICTION GRAPH =====
    st.markdown("### 🤖 AI Trend Prediction")
    st.caption("Based on your logged data, AI predicts future walking trends")
    
    if os.path.exists(DATA_FILE):
        history = pd.read_csv(DATA_FILE)
        if len(history) > 3:
            from sklearn.linear_model import LinearRegression
            
            # Prepare data
            history['date_num'] = range(len(history))
            walks = history['walk'].values
            
            # Train model
            model = LinearRegression()
            model.fit(history[['date_num']], walks)
            
            # Predict next 30 days
            future_days = np.array(range(len(history), len(history) + 30)).reshape(-1, 1)
            future_walks = model.predict(future_days)
            
            # Display prediction metrics
            col_pred1, col_pred2 = st.columns(2)
            with col_pred1:
                current_walkers = int(history['walk'].iloc[-1])
                predicted_walkers = int(future_walks[-1])
                change = predicted_walkers - current_walkers
                st.metric("📊 Current Walkers", current_walkers)
                st.metric("🤖 Predicted in 30 Days", predicted_walkers, delta=f"{change:+d}")
            
            with col_pred2:
                if future_walks[-1] > history['walk'].iloc[-1]:
                    st.success("📈 Trending upward! Keep encouraging walking to school.")
                else:
                    st.warning("📉 Trending downward. Time for a new walking campaign!")
            
            # Create the prediction chart
            pred_days = list(range(len(history) + 30))
            pred_walks = list(walks) + list(future_walks)
            
            fig_pred = go.Figure()
            
            # Actual data (past)
            fig_pred.add_trace(go.Scatter(
                x=list(range(len(history))), 
                y=walks, 
                mode='lines+markers', 
                name='Actual Data',
                line=dict(color='#2e8b57', width=3),
                marker=dict(size=8, color='#2e8b57')
            ))
            
            # AI Prediction (future)
            fig_pred.add_trace(go.Scatter(
                x=list(range(len(history), len(history) + 30)), 
                y=future_walks, 
                mode='lines', 
                name='AI Prediction',
                line=dict(color='#f59e0b', width=3, dash='dash')
            ))
            
            # Add a vertical line at prediction start
            fig_pred.add_vline(
                x=len(history) - 0.5,
                line_dash="dot",
                line_color="gray",
                annotation_text="Today →",
                annotation_position="top right"
            )
            
            fig_pred.update_layout(
                title='AI Predicted Walking Trend (Next 30 Days)',
                xaxis_title='Days',
                yaxis_title='Students Walking to School',
                hovermode='x unified',
                height=450,
                legend=dict(x=0.5, y=-0.15, orientation='h')
            )
            
            st.plotly_chart(fig_pred, use_container_width=True)
            
            # Add insight
            st.info("💡 **AI Insight:** This prediction uses linear regression on your historical walking data. Add more data points for better accuracy!")
        else:
            st.info("📊 Not enough data yet. Add at least 4 days of data in the Data Entry page to see AI predictions!")
    else:
        st.info("📊 Start logging daily data in the Data Entry page to enable AI predictions!")

# ============================================================
# FOOTER
# ============================================================
st.markdown("---")
st.caption("🏫 Eco-School AI · Made for USAII Hackathon 2026 · Data stored locally")