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

# ===== INITIALIZE DATA =====
def init_data():
    data = pd.DataFrame({
        'date': pd.date_range(end=datetime.now(), periods=7),
        'walkers': [120, 125, 130, 135, 140, 145, 150],
        'bikers': [40, 42, 44, 45, 46, 47, 48],
        'car_dropoffs': [60, 58, 55, 54, 52, 50, 48],
        'bus_riders': [180, 182, 178, 180, 185, 190, 188],
        'lights_left_on': [6, 5, 5, 4, 4, 3, 3],
        'food_waste_lbs': [28, 26, 25, 24, 22, 21, 20],
        'paper_reams': [12, 11, 10, 9, 8, 8, 7],
        'recycling_lbs': [16, 18, 20, 22, 24, 26, 28],
        'trees_planted': [0, 0, 1, 1, 2, 2, 3],
        'total_students': [400, 407, 408, 413, 420, 432, 435]
    })
    data.to_csv(DATA_FILE, index=False)
    return data

def load_data():
    try:
        return pd.read_csv(DATA_FILE)
    except:
        return init_data()

def save_data(df):
    df.to_csv(DATA_FILE, index=False)

# ===== LOAD DATA =====
df = load_data()
df['date'] = pd.to_datetime(df['date'])

# ===== CALCULATE METRICS =====
def calculate_metrics(df):
    latest = df.iloc[-1]
    active_transport = latest['walkers'] + latest['bikers']
    total = latest['total_students']
    walk_bike_pct = (active_transport / total * 100) if total > 0 else 0
    
    total_waste = latest['food_waste_lbs'] + latest['recycling_lbs']
    diversion_pct = (latest['recycling_lbs'] / total_waste * 100) if total_waste > 0 else 0
    
    energy_score = max(0, 100 - (latest['lights_left_on'] * 10))
    
    overall = (walk_bike_pct * 0.3 + diversion_pct * 0.25 + energy_score * 0.25 + (latest['trees_planted'] * 2))
    return walk_bike_pct, diversion_pct, energy_score, overall

# ===== AI PREDICTION =====
def predict_trends(df, days=14):
    df_sorted = df.sort_values('date')
    days_num = np.array(range(len(df_sorted))).reshape(-1, 1)
    future_days = np.array(range(len(df_sorted), len(df_sorted) + days)).reshape(-1, 1)
    
    predictions = {}
    metrics = ['walkers', 'bikers', 'car_dropoffs', 'food_waste_lbs', 'recycling_lbs']
    
    for metric in metrics:
        model = LinearRegression()
        model.fit(days_num, df_sorted[metric].values)
        future_values = model.predict(future_days)
        predictions[metric] = {
            'current': df_sorted[metric].iloc[-1],
            'future': future_values,
            'future_avg': future_values.mean(),
            'future_last': future_values[-1],
            'trend': 'up' if future_values[-1] > df_sorted[metric].iloc[-1] else 'down'
        }
    return predictions

# ===== COLOR SCHEME =====
colors = {
    'green': '#2e8b57',
    'blue': '#3b82f6',
    'red': '#ef4444',
    'orange': '#f59e0b',
    'purple': '#8b5cf6',
    'teal': '#14b8a6'
}

# ===== CSS =====
if st.session_state.dark_mode:
    st.markdown("""
    <style>
    .stApp { background: #1a1a2e; }
    .stMarkdown, .stText, label { color: #f0f3f8 !important; }
    .metric-card { background: #16213e; border-radius: 16px; padding: 1.2rem; margin-bottom: 1rem; text-align: center; border: 1px solid #2d3748; }
    </style>
    """, unsafe_allow_html=True)

# ===== HEADER =====
col1, col2 = st.columns([4, 1])
with col1:
    st.markdown("# 🏫 Eco-School AI Dashboard")
    st.caption("Track, predict, and improve your school's environmental impact")
with col2:
    new_mode = st.toggle("🌙 Dark Mode", value=st.session_state.dark_mode)
    if new_mode != st.session_state.dark_mode:
        st.session_state.dark_mode = new_mode
        st.rerun()

# ===== SIDEBAR NAV =====
pages = ["📊 Dashboard", "📥 Data Entry", "📈 Trends", "🤖 AI Predictions", "🏆 Leaderboard", "📋 Action Plan", "🌡️ Simulator"]

selected_page = st.sidebar.radio("Navigate", pages)
st.sidebar.markdown("---")
st.sidebar.caption("🏫 Made for USAII Hackathon 2026")

# ============================================================
# PAGE 1: DASHBOARD
# ============================================================
if selected_page == "📊 Dashboard":
    st.subheader("📊 School Overview")
    
    walk_bike_pct, diversion_pct, energy_score, overall = calculate_metrics(df)
    latest = df.iloc[-1]
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"""
        <div class="metric-card" style="border-left: 4px solid {colors['green']};">
            <div style="font-size: 2rem; font-weight: 800; color: {colors['green']};">{walk_bike_pct:.0f}%</div>
            <div>🚶 Walk/Bike to School</div>
            <div style="font-size: 0.7rem; color: {'#a0aec0' if st.session_state.dark_mode else '#718096'};">Goal: 50%</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card" style="border-left: 4px solid {colors['blue']};">
            <div style="font-size: 2rem; font-weight: 800; color: {colors['blue']};">{diversion_pct:.0f}%</div>
            <div>♻️ Waste Diverted</div>
            <div style="font-size: 0.7rem; color: {'#a0aec0' if st.session_state.dark_mode else '#718096'};">Goal: 70%</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card" style="border-left: 4px solid {colors['orange']};">
            <div style="font-size: 2rem; font-weight: 800; color: {colors['orange']};">{energy_score:.0f}</div>
            <div>💡 Energy Efficiency</div>
            <div style="font-size: 0.7rem; color: {'#a0aec0' if st.session_state.dark_mode else '#718096'};">{latest['lights_left_on']} classrooms left lights on</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        grade = 'A' if overall > 80 else 'B' if overall > 60 else 'C' if overall > 40 else 'D' if overall > 20 else 'F'
        grade_color = colors['green'] if grade == 'A' else colors['blue'] if grade == 'B' else colors['orange'] if grade == 'C' else colors['red']
        st.markdown(f"""
        <div class="metric-card" style="border-left: 4px solid {grade_color};">
            <div style="font-size: 2rem; font-weight: 800; color: {grade_color};">{grade}</div>
            <div>📊 Overall Grade</div>
            <div style="font-size: 0.7rem; color: {'#a0aec0' if st.session_state.dark_mode else '#718096'};">Score: {overall:.0f}/100</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    if walk_bike_pct < 40:
        st.error(f"🚨 **ALERT:** Less than 40% of students walk or bike to school! That's {latest['car_dropoffs']} cars dropping off every morning. Encourage walking!")
    
    if latest['food_waste_lbs'] > 25:
        st.error(f"🚨 **ALERT:** {latest['food_waste_lbs']} lbs of food wasted daily! That's enough to feed {int(latest['food_waste_lbs'] * 3)} people. Start a Share Table!")
    
    if latest['lights_left_on'] > 4:
        st.error(f"🚨 **ALERT:** {latest['lights_left_on']} classrooms left lights on! That's wasting ${latest['lights_left_on'] * 10:.0f}/month on electricity.")
    
    if walk_bike_pct >= 40 and latest['food_waste_lbs'] <= 25 and latest['lights_left_on'] <= 4:
        st.success("🎉 Your school is doing great! Keep it up and aim for 50% walk/bike, 70% waste diversion, and 0 lights left on!")

# ============================================================
# PAGE 2: DATA ENTRY
# ============================================================
elif selected_page == "📥 Data Entry":
    st.subheader("📥 Enter Today's Data")
    
    with st.form("data_entry_form"):
        col1, col2 = st.columns(2)
        with col1:
            walkers = st.number_input("🚶 Students who walked today", min_value=0, value=150)
            bikers = st.number_input("🚲 Students who biked today", min_value=0, value=48)
            car_dropoffs = st.number_input("🚗 Students dropped by car", min_value=0, value=48)
            bus_riders = st.number_input("🚌 Students who took bus", min_value=0, value=188)
        
        with col2:
            lights_left = st.number_input("💡 Classrooms with lights left on", min_value=0, value=3)
            food_waste = st.number_input("🍎 Food waste (lbs)", min_value=0.0, value=20.0)
            recycling = st.number_input("♻️ Recycling collected (lbs)", min_value=0.0, value=28.0)
            paper = st.number_input("📄 Reams of paper used", min_value=0.0, value=7.0)
        
        total_students = walkers + bikers + car_dropoffs + bus_riders
        st.caption(f"👥 Total Students: {total_students}")
        
        date = st.date_input("Date", datetime.now())
        trees_planted = st.number_input("🌳 New trees planted today", min_value=0, value=0)
        
        submitted = st.form_submit_button("💾 Save Data", type="primary")
        
        if submitted:
            new_row = {
                'date': date,
                'walkers': walkers,
                'bikers': bikers,
                'car_dropoffs': car_dropoffs,
                'bus_riders': bus_riders,
                'lights_left_on': lights_left,
                'food_waste_lbs': food_waste,
                'paper_reams': paper,
                'recycling_lbs': recycling,
                'trees_planted': trees_planted,
                'total_students': total_students
            }
            df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
            save_data(df)
            st.success("✅ Data saved!")

# ============================================================
# PAGE 3: TRENDS
# ============================================================
elif selected_page == "📈 Trends":
    st.subheader("📈 Trends Over Time")
    
    df_sorted = df.sort_values('date')
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 🚶 Walk/Bike Trends")
        fig = px.line(df_sorted, x='date', y=['walkers', 'bikers'], 
                      title='Students Walking/Biking to School',
                      labels={'value': 'Students', 'variable': 'Mode'},
                      color_discrete_map={'walkers': colors['green'], 'bikers': colors['blue']})
        fig.update_layout(hovermode='x unified')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("#### 🗑️ Waste Trends")
        waste_df = df_sorted.melt(id_vars=['date'], value_vars=['food_waste_lbs', 'recycling_lbs'],
                                  var_name='Type', value_name='Pounds')
        fig = px.bar(waste_df, x='date', y='Pounds', color='Type',
                     title='Daily Food Waste vs Recycling',
                     color_discrete_map={'food_waste_lbs': colors['orange'], 'recycling_lbs': colors['green']})
        fig.update_layout(barmode='group')
        st.plotly_chart(fig, use_container_width=True)
    
    col3, col4 = st.columns(2)
    
    with col3:
        st.markdown("#### 💡 Energy")
        fig = px.line(df_sorted, x='date', y='lights_left_on',
                      title='Classrooms with Lights Left On',
                      labels={'lights_left_on': 'Classrooms'})
        fig.update_traces(line_color=colors['red'])
        st.plotly_chart(fig, use_container_width=True)
    
    with col4:
        st.markdown("#### 🌳 Trees Planted")
        fig = px.line(df_sorted, x='date', y='trees_planted',
                      title='Cumulative Trees Planted',
                      labels={'trees_planted': 'Trees'})
        fig.update_traces(line_color=colors['green'])
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
            walk_trend = predictions['walkers']
            st.metric(
                "🚶 Walkers", 
                f"{walk_trend['current']:.0f} → {walk_trend['future_last']:.0f}",
                delta=f"{walk_trend['future_last'] - walk_trend['current']:.0f}",
                delta_color="normal"
            )
        
        with col2:
            waste_trend = predictions['food_waste_lbs']
            st.metric(
                "🍎 Food Waste (lbs)",
                f"{waste_trend['current']:.0f} → {waste_trend['future_last']:.0f}",
                delta=f"{waste_trend['future_last'] - waste_trend['current']:.0f}",
                delta_color="inverse"
            )
        
        with col3:
            recycle_trend = predictions['recycling_lbs']
            st.metric(
                "♻️ Recycling (lbs)",
                f"{recycle_trend['current']:.0f} → {recycle_trend['future_last']:.0f}",
                delta=f"{recycle_trend['future_last'] - recycle_trend['current']:.0f}",
                delta_color="normal"
            )
        
        st.markdown("#### 📊 AI Prediction: Walkers Trend")
        df_sorted = df.sort_values('date')
        future_dates = [df_sorted['date'].iloc[-1] + timedelta(days=i+1) for i in range(14)]
        future_walkers = predictions['walkers']['future']
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=df_sorted['date'],
            y=df_sorted['walkers'],
            mode='lines+markers',
            name='Walkers (Actual)',
            line=dict(color=colors['green'])
        ))
        fig.add_trace(go.Scatter(
            x=future_dates,
            y=future_walkers,
            mode='lines',
            name='Walkers (AI Predicted)',
            line=dict(color=colors['blue'], dash='dash')
        ))
        fig.update_layout(hovermode='x unified')
        st.plotly_chart(fig, use_container_width=True)
        
        st.info("🤖 **AI Insight:** " + 
                ("Walking is trending UP! Keep encouraging students to walk." if predictions['walkers']['trend'] == 'up' else 
                 "Walking is trending DOWN. Time for a new walking campaign!"))
    else:
        st.warning("Not enough data for predictions. Enter at least 4 days of data.")

# ============================================================
# PAGE 5: LEADERBOARD
# ============================================================
elif selected_page == "🏆 Leaderboard":
    st.subheader("🏆 Classroom Leaderboard")
    
    st.markdown("### How Points Are Earned:")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.caption("💡 Lights Off: +3 pts per classroom")
        st.caption("♻️ Recycling: +2 pts per lb")
    with col2:
        st.caption("🚶 Walk/Bike: +1 pt per 5 students")
        st.caption("🌳 Trees Planted: +5 pts per tree")
    with col3:
        st.caption("🍎 Food Waste Reduced: +2 pts per lb under 25")
    
    classes = ["Room 101", "Room 102", "Room 103", "Room 104", "Room 105"]
    scores = [random.randint(40, 95) for _ in classes]
    improvements = [random.randint(-5, 15) for _ in classes]
    
    leaderboard = sorted(zip(classes, scores, improvements), key=lambda x: x[1], reverse=True)
    
    st.markdown("---")
    for i, (cls, score, improvement) in enumerate(leaderboard):
        medal = "🥇" if i == 0 else "🥈" if i == 1 else "🥉" if i == 2 else f"{i+1}."
        if improvement > 0:
            st.success(f"{medal} **{cls}** — {score} pts  (+{improvement})")
        else:
            st.info(f"{medal} **{cls}** — {score} pts  ({improvement})")
    
    st.markdown("---")
    st.markdown(f"🎉 **Winner:** {leaderboard[0][0]} with {leaderboard[0][1]} points!")

# ============================================================
# PAGE 6: ACTION PLAN
# ============================================================
elif selected_page == "📋 Action Plan":
    st.subheader("📋 Custom Action Plan")
    st.caption("Based on your school's data, here are the highest-impact actions.")
    
    latest = df.iloc[-1]
    walk_bike_pct, diversion_pct, energy_score, overall = calculate_metrics(df)
    
    st.markdown("### 🔴 PRIORITY 1: Energy Efficiency")
    st.markdown(f"**Problem:** {latest['lights_left_on']} classrooms leave lights on daily.")
    st.markdown(f"**Impact:** Save ${latest['lights_left_on'] * 10:.0f}/month by turning off lights.")
    st.markdown("**Easy First Step:** Assign an 'Energy Monitor' in each classroom.")
    
    st.markdown("### 🟠 PRIORITY 2: Transportation")
    st.markdown(f"**Problem:** {latest['car_dropoffs']} cars drop off students daily.")
    st.markdown(f"**Impact:** Reduce {latest['car_dropoffs'] * 5:.0f} lbs CO2/week by encouraging walking.")
    st.markdown("**Easy First Step:** Launch a 'Walk & Roll Wednesday' program.")
    
    st.markdown("### 🟡 PRIORITY 3: Food Waste")
    st.markdown(f"**Problem:** {latest['food_waste_lbs']} lbs of food wasted daily.")
    st.markdown(f"**Impact:** Divert {latest['food_waste_lbs'] * 180:.0f} lbs/year to hungry people.")
    st.markdown("**Easy First Step:** Start a 'Share Table' for unopened food.")
    
    st.markdown("### 🟢 PRIORITY 4: Recycling")
    st.markdown(f"**Problem:** {latest['recycling_lbs']} lbs recycled daily. Goal: 70% diversion.")
    st.markdown("**Impact:** Save 1 tree per 500 lbs recycled.")
    st.markdown("**Easy First Step:** Add more recycling bins in hallways.")
    
    st.markdown("---")
    st.markdown("### 📊 Estimated Total Impact")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("🌡️ Temperature Reduction", "2-3°F", "with 20 trees")
    with col2:
        st.metric("💰 Cost Savings", "$500/year", "from energy & waste")
    with col3:
        st.metric("🌿 CO2 Reduced", "2,000 lbs/year", "with all actions")

# ============================================================
# PAGE 7: SIMULATOR
# ============================================================
elif selected_page == "🌡️ Simulator":
    st.subheader("🌡️ What If Simulator")
    st.caption("See the impact of your actions before you take them.")
    
    latest = df.iloc[-1]
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 🌳 Tree Planting")
        trees = st.slider("Number of trees to plant:", 0, 100, 20)
        temp_reduction = trees * 0.15
        co2_absorbed = trees * 48
        st.metric("🌡️ Temperature Reduction", f"-{temp_reduction:.1f}°F")
        st.metric("🌿 CO2 Absorbed/Year", f"{co2_absorbed} lbs")
    
    with col2:
        st.markdown("#### 🚶 Walk to School")
        walk_increase = st.slider("Increase walk/bike by:", 0, 100, 20)
        cars_removed = int(latest['car_dropoffs'] * walk_increase / 100)
        co2_saved = cars_removed * 5
        st.metric("🚗 Fewer Cars Daily", f"-{cars_removed}")
        st.metric("🌿 CO2 Saved Daily", f"{co2_saved} lbs")
    
    st.markdown("---")
    st.markdown("### 📊 Combined Impact")
    combined_score = (trees * 0.5 + walk_increase * 0.5)
    # FIX: Progress bar expects value between 0.0 and 1.0
    st.progress(min(100, combined_score) / 100)
    st.caption(f"🌱 Combined Impact Score: {min(100, combined_score):.0f}/100")

# ============================================================
# FOOTER
# ============================================================
st.markdown("---")
st.caption("🏫 Eco-School Dashboard · Made for USAII Hackathon 2026 · Data is saved locally")