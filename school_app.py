import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# ===== PAGE CONFIG =====
st.set_page_config(
    page_title="Eco-School Dashboard",
    page_icon="🌱",
    layout="wide"
)

# ===== CUSTOM CSS FOR COLORFUL CARDS =====
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

/* Color themes for cards */
.card-green { background: linear-gradient(135deg, #2e8b57 0%, #3cb371 100%); color: white; }
.card-blue { background: linear-gradient(135deg, #1e6f9f 0%, #3b82f6 100%); color: white; }
.card-orange { background: linear-gradient(135deg, #d97706 0%, #f59e0b 100%); color: white; }
.card-red { background: linear-gradient(135deg, #dc2626 0%, #ef4444 100%); color: white; }
.card-purple { background: linear-gradient(135deg, #7c3aed 0%, #a78bfa 100%); color: white; }
.card-teal { background: linear-gradient(135deg, #0d9488 0%, #14b8a6 100%); color: white; }
.card-pink { background: linear-gradient(135deg, #db2777 0%, #f472b6 100%); color: white; }
.card-indigo { background: linear-gradient(135deg, #4338ca 0%, #6366f1 100%); color: white; }
.card-gray { background: linear-gradient(135deg, #4b5563 0%, #9ca3af 100%); color: white; }

/* Section headers */
.section-header {
    font-size: 1.5rem;
    font-weight: 700;
    margin: 1.5rem 0 1rem 0;
    padding-left: 0.8rem;
    border-left: 4px solid #2e8b57;
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
.leaderboard-rank {
    font-size: 1.3rem;
    font-weight: 700;
}
.leaderboard-name {
    font-weight: 600;
}
.leaderboard-score {
    font-weight: 800;
    color: #2e8b57;
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
</style>
""", unsafe_allow_html=True)

# ===== HEADER =====
st.markdown('<h1 style="text-align: center; color: #2e8b57;">🌱 Eco-School Dashboard</h1>', unsafe_allow_html=True)
st.markdown('<p style="text-align: center; color: #4a5568;">Track your school\'s environmental impact · AI-powered insights</p>', unsafe_allow_html=True)

# ===== SIDEBAR =====
with st.sidebar:
    st.markdown("### 🏫 Your School")
    school_name = st.text_input("School Name:", value="Washington Middle School")
    
    st.markdown("---")
    
    if st.button("🤖 Why AI?", use_container_width=True):
        st.info("AI analyzes transportation, waste, and energy data to find the highest-impact actions for YOUR school.")
    
    st.markdown("---")
    
    st.markdown("### 📍 Navigate")
    view = st.radio("", [
        "📊 Dashboard", 
        "🏆 Leaderboard", 
        "📋 Action Plan", 
        "🌡️ Simulator", 
        "🌱 Community", 
        "📥 Data Entry"
    ], label_visibility="collapsed")
    
    st.markdown("---")
    
    st.link_button("🐦 Share on Twitter", "https://twitter.com/intent/tweet?text=Check%20out%20Eco-School%20Dashboard!%20🌱", use_container_width=True)

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

# ===== DASHBOARD =====
if view == "📊 Dashboard":
    st.markdown(f'<div class="section-header">📊 {school_name} Dashboard</div>', unsafe_allow_html=True)
    
    # Row 1: Main metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f'''
        <div class="metric-card card-green">
            <div class="metric-value">{school_data["trees"]}<span style="font-size:1rem;"> / {school_data["goal_trees"]}</span></div>
            <div class="metric-label">🌳 Trees on Campus</div>
            <div class="metric-sub">+{school_data["goal_trees"] - school_data["trees"]} needed</div>
        </div>
        ''', unsafe_allow_html=True)
    
    with col2:
        st.markdown(f'''
        <div class="metric-card card-blue">
            <div class="metric-value">{school_data["walk_bike"]}<span style="font-size:1rem;">%</span></div>
            <div class="metric-label">🚶 Walk/Bike to School</div>
            <div class="metric-sub">Goal: {school_data["goal_walk_bike"]}%</div>
        </div>
        ''', unsafe_allow_html=True)
    
    with col3:
        st.markdown(f'''
        <div class="metric-card card-purple">
            <div class="metric-value">{school_data["recycle"]}<span style="font-size:1rem;">%</span></div>
            <div class="metric-label">♻️ Waste Diverted</div>
            <div class="metric-sub">Goal: {school_data["goal_recycle"]}%</div>
        </div>
        ''', unsafe_allow_html=True)
    
    with col4:
        st.markdown(f'''
        <div class="metric-card card-teal">
            <div class="metric-value">{school_data["bottles"]}</div>
            <div class="metric-label">💧 Bottles Saved/Week</div>
            <div class="metric-sub">Plastic bottles kept from landfill</div>
        </div>
        ''', unsafe_allow_html=True)
    
    # Row 2: Problem cards
    st.markdown('<div class="section-header">⚠️ Areas Needing Attention</div>', unsafe_allow_html=True)
    
    col5, col6, col7 = st.columns(3)
    
    with col5:
        st.markdown(f'''
        <div class="metric-card card-red">
            <div class="metric-value">{school_data["car_alone"]}</div>
            <div class="metric-label">🚗 Solo Cars Daily</div>
            <div class="metric-sub">Save {school_data["co2_save"]} lbs CO2/week with carpooling</div>
        </div>
        ''', unsafe_allow_html=True)
    
    with col6:
        st.markdown(f'''
        <div class="metric-card card-orange">
            <div class="metric-value">{school_data["food_waste"]}<span style="font-size:1rem;"> lbs</span></div>
            <div class="metric-label">🍎 Food Wasted Daily</div>
            <div class="metric-sub">{school_data["food_waste"] * 180:,} lbs/year could feed hungry people</div>
        </div>
        ''', unsafe_allow_html=True)
    
    with col7:
        st.markdown(f'''
        <div class="metric-card card-gray">
            <div class="metric-value">{school_data["paper_reams"]}<span style="font-size:1rem;"> reams/week</span></div>
            <div class="metric-label">📄 Paper Usage</div>
            <div class="metric-sub">{school_data["paper_reams"] / 16.6:.1f} trees used per year</div>
        </div>
        ''', unsafe_allow_html=True)
    
    # Row 3: Classroom energy
    st.markdown('<div class="section-header">💡 Classroom Energy Scores</div>', unsafe_allow_html=True)
    
    cols = st.columns(5)
    for idx, (room, data) in enumerate(school_data['classrooms'].items()):
        score = data['score']
        if score >= 80:
            color = "card-green"
        elif score >= 50:
            color = "card-teal"
        else:
            color = "card-red"
        
        with cols[idx]:
            st.markdown(f'''
            <div class="metric-card {color}">
                <div class="metric-value">{score}</div>
                <div class="metric-label">{room}</div>
                <div class="metric-sub">{"✅ Lights Off" if data['lights'] else "❌ Lights Left On"}</div>
            </div>
            ''', unsafe_allow_html=True)

# ===== LEADERBOARD =====
elif view == "🏆 Leaderboard":
    st.markdown('<div class="section-header">🏆 Green Classroom Leaderboard</div>', unsafe_allow_html=True)
    
    leaderboard = []
    for room, data in school_data['classrooms'].items():
        leaderboard.append({"room": room, "score": data['score'], "lights": data['lights']})
    
    leaderboard = sorted(leaderboard, key=lambda x: x['score'], reverse=True)
    
    for i, item in enumerate(leaderboard):
        if i == 0:
            medal = "🥇"
            bg = "#fef3c7"
        elif i == 1:
            medal = "🥈"
            bg = "#f0fdf4"
        elif i == 2:
            medal = "🥉"
            bg = "#e0f2fe"
        else:
            medal = f"{i+1}."
            bg = "#f8faf8"
        
        lights_status = "✅ Lights Off" if item['lights'] else "❌ Lights Left On"
        
        st.markdown(f'''
        <div class="leaderboard-item" style="background: {bg};">
            <div style="display: flex; justify-content: space-between; width: 100%;">
                <div class="leaderboard-rank">{medal}</div>
                <div class="leaderboard-name">{item['room']}</div>
                <div class="leaderboard-score">{item['score']} points</div>
                <div style="font-size: 0.8rem;">{lights_status}</div>
            </div>
        </div>
        ''', unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("### 📋 Weekly Challenge Checklist")
    st.checkbox("☐ Turn off lights when leaving (10 points/day)")
    st.checkbox("☐ Shut down computers at end of day (10 points/day)")
    st.checkbox("☐ Sort waste correctly (20 points/day)")
    st.checkbox("☐ Walk, bike, or carpool to school (15 points/day)")

# ===== ACTION PLAN =====
elif view == "📋 Action Plan":
    st.markdown('<div class="section-header">📋 Your School\'s Custom Action Plan</div>', unsafe_allow_html=True)
    
    st.markdown(f'''
    <div class="action-item action-priority-1">
        <strong>🔴 PRIORITY 1: Reduce Solo Car Drop-offs</strong><br>
        <strong>Problem:</strong> {school_data["car_alone"]} cars arrive daily with just one student.<br>
        <strong>Solution:</strong> Launch a "Walk & Roll Wednesday" program.<br>
        <strong>Impact:</strong> Save {school_data["co2_save"]} lbs CO2/week.
    </div>
    ''', unsafe_allow_html=True)
    
    st.markdown(f'''
    <div class="action-item action-priority-2">
        <strong>🟠 PRIORITY 2: Stop Wasting Edible Food</strong><br>
        <strong>Problem:</strong> {school_data["food_waste"]} lbs of unopened food thrown away daily.<br>
        <strong>Solution:</strong> Start a "Share Table" where students place unwanted unopened food.<br>
        <strong>Impact:</strong> Divert {school_data["food_waste"] * 180:,} lbs/year to hungry people.
    </div>
    ''', unsafe_allow_html=True)
    
    st.markdown(f'''
    <div class="action-item action-priority-3">
        <strong>🟢 PRIORITY 3: Turn Off Lights</strong><br>
        <strong>Problem:</strong> {school_data["lights_on"]} classrooms leave lights on when empty.<br>
        <strong>Solution:</strong> Assign daily "Energy Monitor" student job in each classroom.<br>
        <strong>Impact:</strong> Save $50/month on electricity bills.
    </div>
    ''', unsafe_allow_html=True)

# ===== SIMULATOR =====
elif view == "🌡️ Simulator":
    st.markdown('<div class="section-header">🌡️ What If Simulator</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="metric-card card-green" style="text-align: center; padding: 1.5rem;">', unsafe_allow_html=True)
        trees = st.slider("🌳 Trees to plant:", 0, 100, 20, key="trees_sim")
        temp_reduction = trees * 0.3
        st.markdown(f'<div class="metric-value">-{temp_reduction:.1f}°F</div>', unsafe_allow_html=True)
        st.markdown('<div class="metric-label">Temperature Reduction</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="metric-card card-blue" style="text-align: center; padding: 1.5rem;">', unsafe_allow_html=True)
        walk_pct = st.slider("🚶 Increase walk/bike by:", 0, 100, 20, key="walk_sim")
        cars_removed = int(54 * walk_pct / 100)
        st.markdown(f'<div class="metric-value">-{cars_removed}</div>', unsafe_allow_html=True)
        st.markdown('<div class="metric-label">Fewer Solo Cars Daily</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

# ===== COMMUNITY =====
elif view == "🌱 Community":
    st.markdown('<div class="section-header">🌱 Community Action Tracker</div>', unsafe_allow_html=True)
    
    actions = [
        "🌳 Planted a tree on campus",
        "🚗 Started a carpool group",
        "🗑️ Organized a waste audit",
        "💡 Created an energy monitor program",
        "💧 Added a water bottle refill station"
    ]
    
    selected = st.selectbox("What did your school do this week?", actions)
    
    if st.button("✅ Log This Action", type="primary"):
        st.balloons()
        st.success("Thanks for helping your school go green! 🌍")
    
    st.markdown("---")
    st.markdown('<div class="metric-card card-gray" style="text-align: center;">', unsafe_allow_html=True)
    st.markdown('<div class="metric-label">💡 Every action counts</div>', unsafe_allow_html=True)
    st.markdown('<div class="metric-sub">Small changes add up to big impact!</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ===== DATA ENTRY =====
elif view == "📥 Data Entry":
    st.markdown('<div class="section-header">📥 Enter Your School\'s Data</div>', unsafe_allow_html=True)
    
    with st.form("data_entry"):
        st.markdown("### 🚗 Transportation")
        col_a, col_b = st.columns(2)
        with col_a:
            walk = st.number_input("Students who walked:", min_value=0, value=135)
            bike = st.number_input("Students who biked:", min_value=0, value=45)
        with col_b:
            car_alone = st.number_input("Students in car alone:", min_value=0, value=54)
        
        st.markdown("### 🗑️ Cafeteria Waste")
        food_waste = st.number_input("Pounds of uneaten food:", min_value=0.0, value=24.0)
        
        st.markdown("### 💡 Energy")
        lights_left = st.number_input("Classrooms that left lights on:", min_value=0, value=5)
        
        submitted = st.form_submit_button("💾 Save Data", type="primary")
        
        if submitted:
            st.balloons()
            st.success("✅ Data saved! Track progress week over week.")

# ===== FOOTER =====
st.markdown("""
<div class="footer">
    <strong>🌱 Eco-School Dashboard</strong> · AI-powered · Built for USAII Hackathon 2026
</div>
""", unsafe_allow_html=True)