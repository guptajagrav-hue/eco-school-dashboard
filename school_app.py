import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import numpy as np
import os
from sklearn.linear_model import LinearRegression

# ===== PAGE CONFIG =====
st.set_page_config(
    page_title="Eco-School Dashboard",
    page_icon="🌱",
    layout="wide"
)

# ===== CUSTOM CSS =====
st.markdown("""
<style>
/* Card styling */
.metric-card {
    background: white;
    padding: 1.2rem;
    border-radius: 20px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    transition: transform 0.2s, box-shadow 0.2s;
    margin-bottom: 1rem;
    text-align: center;
}
.metric-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 12px 24px rgba(0,0,0,0.12);
}
.metric-value {
    font-size: 2.2rem;
    font-weight: 800;
    line-height: 1.2;
}
.metric-label {
    font-size: 0.85rem;
    text-transform: uppercase;
    letter-spacing: 1px;
    font-weight: 600;
    margin-top: 0.5rem;
}
.metric-sub {
    font-size: 0.7rem;
    margin-top: 0.3rem;
    opacity: 0.8;
}

/* Color themes */
.card-green { background: linear-gradient(135deg, #2e8b57 0%, #3cb371 100%); color: white; }
.card-blue { background: linear-gradient(135deg, #1e6f9f 0%, #3b82f6 100%); color: white; }
.card-orange { background: linear-gradient(135deg, #d97706 0%, #f59e0b 100%); color: white; }
.card-red { background: linear-gradient(135deg, #dc2626 0%, #ef4444 100%); color: white; }
.card-purple { background: linear-gradient(135deg, #7c3aed 0%, #a78bfa 100%); color: white; }
.card-teal { background: linear-gradient(135deg, #0d9488 0%, #14b8a6 100%); color: white; }

/* Section headers */
.section-header {
    font-size: 1.5rem;
    font-weight: 700;
    margin: 1.5rem 0 1rem 0;
    padding-left: 0.8rem;
    border-left: 4px solid #2e8b57;
}

/* Navigation buttons container */
.nav-container {
    display: flex;
    justify-content: center;
    gap: 0.8rem;
    flex-wrap: wrap;
    margin: 1rem 0;
    padding: 0.5rem;
    background: white;
    border-radius: 50px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.05);
}

/* Leaderboard items */
.leaderboard-item {
    padding: 0.8rem 1rem;
    margin: 0.5rem 0;
    border-radius: 12px;
    background: #f8faf8;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

/* Action plan items */
.action-item {
    padding: 1rem;
    margin: 1rem 0;
    border-radius: 16px;
    border-left: 4px solid;
}
.action-priority-1 { background: #fef2f2; border-left-color: #dc2626; }
.action-priority-2 { background: #fffbeb; border-left-color: #f59e0b; }
.action-priority-3 { background: #ecfdf5; border-left-color: #10b981; }

/* Footer */
.footer {
    text-align: center;
    padding: 2rem;
    color: #718096;
    font-size: 0.8rem;
    border-top: 1px solid #e2e8f0;
    margin-top: 2rem;
}

/* Profile box */
.profile-box {
    background: white;
    border-radius: 24px;
    padding: 1.5rem;
    box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    text-align: center;
    margin-bottom: 1rem;
}

/* School profile header */
.profile-header {
    background: linear-gradient(135deg, #2e8b57 0%, #3cb371 100%);
    border-radius: 24px;
    padding: 1.5rem;
    color: white;
    margin-bottom: 1rem;
    text-align: center;
}
</style>
""", unsafe_allow_html=True)

# ===== SESSION STATE FOR NAVIGATION =====
if 'page' not in st.session_state:
    st.session_state.page = "Dashboard"

# ===== FUNCTION TO CHANGE PAGE =====
def set_page(page_name):
    st.session_state.page = page_name
    st.rerun()

# ===== NAVIGATION BUTTONS =====
st.markdown('<div class="nav-container">', unsafe_allow_html=True)

cols = st.columns(6)
with cols[0]:
    if st.button("📊 Dashboard", key="btn_dashboard", use_container_width=True):
        set_page("Dashboard")
with cols[1]:
    if st.button("🏆 Leaderboard", key="btn_leaderboard", use_container_width=True):
        set_page("Leaderboard")
with cols[2]:
    if st.button("📋 Action Plan", key="btn_action", use_container_width=True):
        set_page("Action Plan")
with cols[3]:
    if st.button("🌡️ Simulator", key="btn_simulator", use_container_width=True):
        set_page("Simulator")
with cols[4]:
    if st.button("🌱 Community", key="btn_community", use_container_width=True):
        set_page("Community")
with cols[5]:
    if st.button("📥 Data Entry", key="btn_data", use_container_width=True):
        set_page("Data Entry")

st.markdown('</div>', unsafe_allow_html=True)

# ===== SCHOOL PROFILE HEADER =====
school_name = "Washington Middle School"
st.markdown(f"""
<div class="profile-header">
    <h2>🌱 {school_name}</h2>
    <p>Environmental Profile · AI-Powered Insights</p>
</div>
""", unsafe_allow_html=True)

# ===== SIDEBAR =====
with st.sidebar:
    st.markdown("### ⚙️ Settings")
    school_name_input = st.text_input("School Name:", value="Washington Middle School")
    st.markdown("---")
    if st.button("🤖 Why AI?", use_container_width=True):
        st.info("AI analyzes transportation, waste, and energy data to find the highest-impact actions for YOUR school.")
    st.markdown("---")
    st.link_button("🐦 Share on Twitter", "https://twitter.com/intent/tweet?text=Check%20out%20Eco-School%20Dashboard!%20🌱", use_container_width=True)
    
    # Show data file status
    data_file = "school_data_log.csv"
    if os.path.exists(data_file):
        file_size = os.path.getsize(data_file) // 1024
        st.success(f"✅ {file_size} KB of data saved")

# ===== CREATE DEMO DATA IF NO DATA EXISTS =====
data_file = "school_data_log.csv"
if not os.path.exists(data_file):
    demo_data = pd.DataFrame([
        {"date": "2026-06-10", "walk": 120, "bike": 40, "car_alone": 60, "total_students": 220, "food_waste_lbs": 28, "lights_left_on": 6},
        {"date": "2026-06-11", "walk": 125, "bike": 42, "car_alone": 58, "total_students": 225, "food_waste_lbs": 26, "lights_left_on": 5},
        {"date": "2026-06-12", "walk": 130, "bike": 44, "car_alone": 55, "total_students": 229, "food_waste_lbs": 25, "lights_left_on": 5},
        {"date": "2026-06-13", "walk": 135, "bike": 45, "car_alone": 54, "total_students": 234, "food_waste_lbs": 24, "lights_left_on": 4},
        {"date": "2026-06-14", "walk": 140, "bike": 46, "car_alone": 52, "total_students": 238, "food_waste_lbs": 22, "lights_left_on": 4},
        {"date": "2026-06-15", "walk": 145, "bike": 47, "car_alone": 50, "total_students": 242, "food_waste_lbs": 21, "lights_left_on": 3},
    ])
    demo_data.to_csv(data_file, index=False)
    st.toast("📊 Demo data loaded! AI features are now active.", icon="✅")

# ===== DATA =====
school_data = {
    "trees": 31,
    "goal_trees": 50,
    "walk_bike": 40,
    "goal_walk_bike": 50,
    "recycle": 55,
    "goal_recycle": 70,
    "car_alone": 54,
    "food_waste": 24,
    "lights_on": 5,
    "paper_reams": 12,
    "bottles": 392,
    "co2_save": 1200,
    "classrooms": {
        "Room 101": {"score": 45, "lights": False},
        "Room 102": {"score": 95, "lights": True},
        "Room 103": {"score": 60, "lights": False},
        "Room 104": {"score": 80, "lights": True},
        "Room 105": {"score": 25, "lights": False},
    }
}

# Environmental profile scores
environmental_profile = {
    "🌳 Tree Canopy": min(100, (school_data["trees"] / school_data["goal_trees"]) * 100),
    "🚶 Active Transport": min(100, (school_data["walk_bike"] / school_data["goal_walk_bike"]) * 100),
    "♻️ Waste Diversion": min(100, (school_data["recycle"] / school_data["goal_recycle"]) * 100),
    "💡 Energy Efficiency": min(100, max(0, 100 - (school_data["lights_on"] * 8))),
    "📄 Paper Reduction": min(100, max(0, 100 - ((school_data["paper_reams"] - 8) / 8 * 100))),
    "💧 Water Conservation": min(100, (school_data["bottles"] / 500) * 100),
}

# ===== HEXAGON CHART FUNCTION =====
def create_hexagon_chart(scores, title="Environmental Profile"):
    categories = list(scores.keys())
    values = list(scores.values())
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        name='Your School',
        line_color='#2e8b57',
        fillcolor='rgba(46, 139, 86, 0.3)',
        line_width=3,
        marker=dict(size=8, color='#2e8b57')
    ))
    
    fig.add_trace(go.Scatterpolar(
        r=[100] * len(categories),
        theta=categories,
        name='Goal (100%)',
        line_color='#cbd5e1',
        line_dash='dash',
        line_width=2,
        fill='none'
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                tickvals=[0, 25, 50, 75, 100],
                ticktext=['0', '25', '50', '75', '100'],
                gridcolor='#e2e8f0',
                linecolor='#cbd5e1'
            ),
            angularaxis=dict(
                tickfont=dict(size=12, weight='bold'),
                gridcolor='#e2e8f0',
                linecolor='#cbd5e1'
            ),
            bgcolor='rgba(0,0,0,0)'
        ),
        title=dict(
            text=title,
            font=dict(size=16, weight='bold', color='#2d3748'),
            x=0.5
        ),
        showlegend=True,
        legend=dict(
            x=0.5,
            y=-0.1,
            orientation='h',
            bgcolor='rgba(255,255,255,0.8)'
        ),
        height=500,
        width=600,
        margin=dict(l=80, r=80, t=80, b=80)
    )
    
    return fig

# ===== DASHBOARD PAGE =====
if st.session_state.page == "Dashboard":
    st.markdown('<div class="section-header">📊 Environmental Dashboard</div>', unsafe_allow_html=True)
    
    # Hexagon Chart INSIDE the curved box
    st.markdown('<div class="profile-box">', unsafe_allow_html=True)
    st.markdown('<h3 style="text-align: center; margin-bottom: 1rem;">🌿 Environmental Profile</h3>', unsafe_allow_html=True)
    
    hex_fig = create_hexagon_chart(environmental_profile, f"{school_name_input} - 6 Pillars of Sustainability")
    st.plotly_chart(hex_fig, use_container_width=True)
    
    avg_score = sum(environmental_profile.values()) / len(environmental_profile)
    st.markdown(f"""
    <div style="text-align: center; margin-top: 0.5rem;">
        <span style="background: #2e8b57; color: white; padding: 0.5rem 1.5rem; border-radius: 30px; font-weight: bold;">
            🌟 Overall Score: {avg_score:.0f}/100
        </span>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Metrics Row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f'''
        <div class="metric-card card-green">
            <div class="metric-value">{school_data["trees"]}<span style="font-size:1rem;"> / {school_data["goal_trees"]}</span></div>
            <div class="metric-label">🌳 Trees on Campus</div>
        </div>
        ''', unsafe_allow_html=True)
    
    with col2:
        st.markdown(f'''
        <div class="metric-card card-blue">
            <div class="metric-value">{school_data["walk_bike"]}<span style="font-size:1rem;">%</span></div>
            <div class="metric-label">🚶 Walk/Bike to School</div>
        </div>
        ''', unsafe_allow_html=True)
    
    with col3:
        st.markdown(f'''
        <div class="metric-card card-purple">
            <div class="metric-value">{school_data["recycle"]}<span style="font-size:1rem;">%</span></div>
            <div class="metric-label">♻️ Waste Diverted</div>
        </div>
        ''', unsafe_allow_html=True)
    
    with col4:
        st.markdown(f'''
        <div class="metric-card card-teal">
            <div class="metric-value">{school_data["bottles"]}</div>
            <div class="metric-label">💧 Bottles Saved/Week</div>
        </div>
        ''', unsafe_allow_html=True)
    
    # Problem Areas
    st.markdown('<div class="section-header">⚠️ Areas Needing Attention</div>', unsafe_allow_html=True)
    
    col5, col6, col7 = st.columns(3)
    with col5:
        st.markdown(f'''
        <div class="metric-card card-red">
            <div class="metric-value">{school_data["car_alone"]}</div>
            <div class="metric-label">🚗 Solo Cars Daily</div>
        </div>
        ''', unsafe_allow_html=True)
    with col6:
        st.markdown(f'''
        <div class="metric-card card-orange">
            <div class="metric-value">{school_data["food_waste"]}<span style="font-size:1rem;"> lbs</span></div>
            <div class="metric-label">🍎 Food Wasted Daily</div>
        </div>
        ''', unsafe_allow_html=True)
    with col7:
        st.markdown(f'''
        <div class="metric-card" style="background: linear-gradient(135deg, #4b5563 0%, #9ca3af 100%); color: white;">
            <div class="metric-value">{school_data["paper_reams"]}<span style="font-size:1rem;"> reams</span></div>
            <div class="metric-label">📄 Paper/Week</div>
        </div>
        ''', unsafe_allow_html=True)
    
    # ===== AI FEATURE: SMART ANOMALY DETECTION =====
    st.markdown('<div class="section-header">🤖 AI Insights</div>', unsafe_allow_html=True)
    
    if os.path.exists(data_file):
        history = pd.read_csv(data_file)
        
        if len(history) > 3:
            # Walk anomaly detection
            walk_mean = history['walk'].mean()
            walk_std = history['walk'].std()
            last_walk = history['walk'].iloc[-1]
            
            if last_walk < walk_mean - 2 * walk_std:
                st.warning("🚨 AI Alert: Unusual drop in students walking to school! Consider a walk-to-school campaign.")
            elif last_walk > walk_mean + 2 * walk_std:
                st.success("🎉 AI Insight: Walking to school is at an all-time high! Great job!")
            else:
                st.info("✅ AI Analysis: Walking trends are stable. Keep up the good work!")
            
            # Food waste anomaly
            waste_mean = history['food_waste_lbs'].mean()
            waste_std = history['food_waste_lbs'].std()
            last_waste = history['food_waste_lbs'].iloc[-1]
            
            if last_waste > waste_mean + waste_std:
                st.warning("🚨 AI Alert: Food waste is higher than usual. Check cafeteria operations.")
            elif last_waste < waste_mean - waste_std:
                st.success("🎉 AI Insight: Food waste is down! Great job reducing waste.")
        else:
            st.info("📊 AI needs at least 4 days of data to detect patterns. Keep logging!")
    else:
        st.info("📊 Start logging daily data in the Data Entry page to enable AI insights!")
    
    # ===== AI FEATURE: PEER SCHOOL COMPARISON =====
    if os.path.exists(data_file):
        history = pd.read_csv(data_file)
        if len(history) > 3:
            st.markdown('<div class="section-header">🏫 How You Compare to National Average</div>', unsafe_allow_html=True)
            
            # Calculate your school's performance
            total_walk = history['walk'].sum()
            total_car = history['car_alone'].sum()
            your_walk_rate = total_walk / (total_walk + total_car) * 100 if (total_walk + total_car) > 0 else 0
            
            # Simulated national average
            national_avg = 45
            
            col_comp1, col_comp2 = st.columns(2)
            with col_comp1:
                if your_walk_rate > national_avg:
                    st.success(f"✅ Your school ({your_walk_rate:.0f}% walk) beats the national average of {national_avg}%!")
                else:
                    st.warning(f"⚠️ Your school ({your_walk_rate:.0f}% walk) is below the national average of {national_avg}%.")
            
            with col_comp2:
                gap = national_avg - your_walk_rate
                if gap > 0:
                    avg_walk = history['walk'].mean()
                    more_students_needed = int(gap/100 * avg_walk) if avg_walk > 0 else 10
                    st.info(f"🤖 AI Suggestion: Need {more_students_needed} more students walking daily to reach average.")

# ===== LEADERBOARD PAGE =====
elif st.session_state.page == "Leaderboard":
    st.markdown('<div class="section-header">🏆 Green Classroom Leaderboard</div>', unsafe_allow_html=True)
    
    leaderboard = []
    for room, data in school_data['classrooms'].items():
        leaderboard.append({"room": room, "score": data['score'], "lights": data['lights']})
    leaderboard = sorted(leaderboard, key=lambda x: x['score'], reverse=True)
    
    for i, item in enumerate(leaderboard):
        medal = "🥇" if i == 0 else "🥈" if i == 1 else "🥉" if i == 2 else f"{i+1}."
        lights_status = "✅ Lights Off" if item['lights'] else "❌ Lights Left On"
        st.markdown(f'<div class="leaderboard-item"><b>{medal}</b> {item["room"]} — <b>{item["score"]} points</b> | {lights_status}</div>', unsafe_allow_html=True)

# ===== ACTION PLAN PAGE =====
elif st.session_state.page == "Action Plan":
    st.markdown('<div class="section-header">📋 Custom Action Plan</div>', unsafe_allow_html=True)
    
    st.markdown(f'''
    <div class="action-item action-priority-1">
        <strong>🔴 PRIORITY 1: Reduce Solo Car Drop-offs</strong><br>
        🚗 {school_data["car_alone"]} solo cars daily → Save {school_data["co2_save"]} lbs CO2/week
    </div>
    <div class="action-item action-priority-2">
        <strong>🟠 PRIORITY 2: Stop Wasting Food</strong><br>
        🍎 {school_data["food_waste"]} lbs wasted daily → Divert {school_data["food_waste"] * 180:,} lbs/year
    </div>
    <div class="action-item action-priority-3">
        <strong>🟢 PRIORITY 3: Turn Off Lights</strong><br>
        💡 {school_data["lights_on"]} classrooms leave lights on → Save $50/month
    </div>
    ''', unsafe_allow_html=True)
    
    # ===== AI FEATURE: PERSONALIZED RECOMMENDATIONS =====
    if os.path.exists(data_file):
        history = pd.read_csv(data_file)
        if len(history) > 3:
            st.markdown("### 🤖 AI-Powered Custom Recommendations")
            
            # Analyze which area needs most improvement
            walk_rate = history['walk'].mean() / (history['walk'].mean() + history['car_alone'].mean()) * 100 if (history['walk'].mean() + history['car_alone'].mean()) > 0 else 50
            waste_avg = history['food_waste_lbs'].mean()
            lights_avg = history['lights_left_on'].mean()
            
            recommendations_made = False
            
            if walk_rate < 40:
                st.info(f"🚶 **Low walking rate** — Only {walk_rate:.0f}% walk vs car. Start a 'walking school bus' program where neighbors walk together!")
                recommendations_made = True
            if waste_avg > 25:
                st.info(f"🍎 **High food waste** — Average {waste_avg:.0f} lbs/day. Start a 'Share Table' for unopened food!")
                recommendations_made = True
            if lights_avg > 3:
                st.info(f"💡 **Lights left on** — Average {lights_avg:.0f} classrooms. Assign daily 'Energy Monitor' student jobs!")
                recommendations_made = True
            if not recommendations_made:
                st.success("🎉 Your school is doing great across all metrics! Keep up the amazing work!")
    
    # ===== AI FEATURE: SMART GOAL SETTING =====
    if os.path.exists(data_file):
        history = pd.read_csv(data_file)
        if len(history) > 3:
            st.markdown("### 🎯 AI-Generated Goals")
            
            col_goal1, col_goal2 = st.columns(2)
            
            with col_goal1:
                # Walking goal
                walk_first = history['walk'].iloc[0]
                walk_last = history['walk'].iloc[-1]
                walk_change = walk_last - walk_first
                days = len(history)
                
                if walk_change > 0:
                    daily_improvement = walk_change / days
                    goal_30d = walk_last + (daily_improvement * 30)
                    st.metric("🤖 30-Day Walk Goal", f"{int(goal_30d)} students", 
                              delta=f"+{int(goal_30d - walk_last)} from today")
                else:
                    goal_30d = walk_last + 10
                    st.metric("🤖 30-Day Walk Goal", f"{int(goal_30d)} students", 
                              delta="Aim for +10 students")
            
            with col_goal2:
                # Waste reduction goal
                waste_first = history['food_waste_lbs'].iloc[0]
                waste_last = history['food_waste_lbs'].iloc[-1]
                waste_change = waste_last - waste_first
                
                if waste_change < 0:
                    daily_reduction = -waste_change / days
                    goal_30d_waste = max(0, waste_last - (daily_reduction * 30))
                    st.metric("🤖 30-Day Waste Goal", f"{int(goal_30d_waste)} lbs", 
                              delta=f"-{int(waste_last - goal_30d_waste)} lbs")
                else:
                    goal_30d_waste = max(0, waste_last - 5)
                    st.metric("🤖 30-Day Waste Goal", f"{int(goal_30d_waste)} lbs", 
                              delta="Aim for -5 lbs")

# ===== SIMULATOR PAGE =====
elif st.session_state.page == "Simulator":
    st.markdown('<div class="section-header">🌡️ What If Simulator</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        trees = st.slider("🌳 Trees to plant:", 0, 100, 20)
        st.metric("Temperature Reduction", f"-{trees * 0.3:.1f}°F")
    with col2:
        walk_pct = st.slider("🚶 Increase walk/bike by:", 0, 100, 20)
        st.metric("Fewer Solo Cars Daily", f"-{int(54 * walk_pct / 100)}")
    
    # ===== AI FEATURE: TREND PREDICTION =====
    if os.path.exists(data_file):
        history = pd.read_csv(data_file)
        if len(history) > 3:
            st.markdown("---")
            st.markdown("### 🤖 AI Trend Prediction")
            
            # Predict future walk counts using linear regression
            days = np.array(range(len(history))).reshape(-1, 1)
            walks = history['walk'].values
            
            model = LinearRegression()
            model.fit(days, walks)
            
            future_days = np.array(range(len(history), len(history) + 30)).reshape(-1, 1)
            future_walks = model.predict(future_days)
            
            col_pred1, col_pred2 = st.columns(2)
            with col_pred1:
                st.metric("🤖 AI Predicts: Walkers in 30 days", f"{int(future_walks[-1])} students", 
                          delta=f"{int(future_walks[-1] - history['walk'].iloc[-1]):+d}")
            with col_pred2:
                if future_walks[-1] > history['walk'].iloc[-1]:
                    st.success("📈 Trending upward! Keep encouraging walking to school.")
                else:
                    st.warning("📉 Trending downward. Time for a new walking campaign!")
            
            # Show prediction chart
            pred_days = list(range(len(history) + 30))
            pred_walks = list(walks) + list(future_walks)
            
            fig_pred = go.Figure()
            fig_pred.add_trace(go.Scatter(x=list(range(len(history))), y=walks, mode='lines+markers', name='Actual Data', line=dict(color='#2e8b57')))
            fig_pred.add_trace(go.Scatter(x=list(range(len(history), len(history) + 30)), y=future_walks, mode='lines', name='AI Prediction', line=dict(color='#f59e0b', dash='dash')))
            fig_pred.update_layout(title='AI Predicted Walking Trend (Next 30 Days)', xaxis_title='Days', yaxis_title='Students Walking', hovermode='x unified')
            st.plotly_chart(fig_pred, use_container_width=True)

# ===== COMMUNITY PAGE =====
elif st.session_state.page == "Community":
    st.markdown('<div class="section-header">🌱 Community Action Tracker</div>', unsafe_allow_html=True)
    
    actions = ["🌳 Planted a tree", "🚗 Started carpooling", "🗑️ Waste audit", "💡 Energy monitors", "💧 Water station"]
    selected = st.selectbox("What did your school do?", actions)
    
    if st.button("✅ Log Action"):
        st.balloons()
        st.success("Thanks for helping! 🌍")

# ===== DATA ENTRY PAGE =====
elif st.session_state.page == "Data Entry":
    st.markdown('<div class="section-header">📥 Enter School Data</div>', unsafe_allow_html=True)
    
    # Clear data button row
    col_clear1, col_clear2 = st.columns([4, 1])
    with col_clear2:
        if st.button("🗑️ Clear All Data", type="secondary", use_container_width=True):
            if os.path.exists(data_file):
                os.remove(data_file)
                st.success("✅ All data cleared successfully!")
                st.rerun()
            else:
                st.warning("No data file found to clear.")
    
    with st.form("data_form"):
        st.markdown("### 🚗 Transportation")
        col_a, col_b = st.columns(2)
        with col_a:
            walk = st.number_input("Students who walked:", min_value=0, max_value=1000, value=145)
            bike = st.number_input("Students who biked:", min_value=0, max_value=1000, value=47)
        with col_b:
            car_alone = st.number_input("Students in car alone:", min_value=0, max_value=1000, value=50)
        
        st.markdown("### 🗑️ Cafeteria Waste")
        food_waste = st.number_input("Pounds of uneaten food:", min_value=0.0, max_value=500.0, value=21.0, step=1.0)
        
        st.markdown("### 💡 Energy")
        lights_left = st.number_input("Classrooms that left lights on:", min_value=0, max_value=50, value=3)
        
        date = st.date_input("Date:", datetime.now())
        
        submitted = st.form_submit_button("💾 Save Data", type="primary")
        
        if submitted:
            # Create new data row
            new_data = pd.DataFrame([{
                "date": date,
                "walk": walk,
                "bike": bike,
                "car_alone": car_alone,
                "total_students": walk + bike + car_alone,
                "food_waste_lbs": food_waste,
                "lights_left_on": lights_left
            }])
            
            # Append to existing file or create new
            if os.path.exists(data_file):
                existing = pd.read_csv(data_file)
                combined = pd.concat([existing, new_data], ignore_index=True)
                combined.to_csv(data_file, index=False)
            else:
                new_data.to_csv(data_file, index=False)
            
            st.success("✅ Data saved!")
            st.balloons()
    
    # Show saved data history
    if os.path.exists(data_file):
        st.markdown("---")
        st.markdown("### 📊 Data History")
        history = pd.read_csv(data_file)
        history_display = history.sort_values("date", ascending=False)
        st.dataframe(history_display, use_container_width=True)
        
        # Download button
        csv = history.to_csv(index=False)
        st.download_button(
            label="📥 Download All Data as CSV",
            data=csv,
            file_name=f"eco_school_data_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )
        
        # Show trends
        if len(history) > 1:
            st.markdown("---")
            st.markdown("### 📈 Trends Over Time")
            
            col_t1, col_t2 = st.columns(2)
            with col_t1:
                walk_first = history['walk'].iloc[0]
                walk_last = history['walk'].iloc[-1]
                walk_change = walk_last - walk_first
                st.metric("🚶 Walk to School Trend", f"{walk_last} students", delta=f"{walk_change:+.0f} vs first day")
            
            with col_t2:
                waste_first = history['food_waste_lbs'].iloc[0]
                waste_last = history['food_waste_lbs'].iloc[-1]
                waste_change = waste_last - waste_first
                st.metric("🍎 Food Waste Trend", f"{waste_last:.0f} lbs", delta=f"{waste_change:+.0f} vs first day")
            
            # Simple line chart
            st.markdown("#### Walk to School Over Time")
            fig = px.line(history, x='date', y='walk', title='Students Walking to School')
            st.plotly_chart(fig, use_container_width=True)
            
            # Food waste trend chart
            st.markdown("#### Food Waste Over Time")
            fig2 = px.line(history, x='date', y='food_waste_lbs', title='Pounds of Food Waste per Day')
            st.plotly_chart(fig2, use_container_width=True)

# ===== FOOTER =====
st.markdown("""
<div class="footer">
    <strong>🌱 Eco-School Dashboard</strong> · AI-powered · Built for USAII Hackathon 2026
</div>
""", unsafe_allow_html=True)