import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import numpy as np

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

/* Top Navigation Bar */
.top-nav {
    display: flex;
    justify-content: center;
    gap: 0.5rem;
    flex-wrap: wrap;
    margin: 1rem 0;
    padding: 0.5rem;
    background: white;
    border-radius: 50px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.05);
}
.nav-btn {
    background: transparent;
    border: none;
    padding: 0.6rem 1.2rem;
    border-radius: 40px;
    font-size: 1rem;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.2s;
    color: #4a5568;
}
.nav-btn:hover {
    background: #e2e8f0;
}
.nav-btn-active {
    background: linear-gradient(135deg, #2e8b57 0%, #3cb371 100%);
    color: white;
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

/* Hexagon container */
.hexagon-container {
    background: white;
    border-radius: 24px;
    padding: 1.5rem;
    box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    text-align: center;
}

/* School profile header */
.profile-header {
    background: linear-gradient(135deg, #2e8b57 0%, #3cb371 100%);
    border-radius: 24px;
    padding: 1.5rem;
    color: white;
    margin-bottom: 1rem;
}
</style>
""", unsafe_allow_html=True)

# ===== SESSION STATE FOR NAVIGATION =====
if 'page' not in st.session_state:
    st.session_state.page = "Dashboard"

# ===== NAVIGATION BUTTONS (Horizontal - Like Previous Site) =====
st.markdown("""
<div style="display: flex; justify-content: center; gap: 0.8rem; flex-wrap: wrap; margin: 1rem 0;">
    <button class="nav-btn" onclick="window.location.href='?page=Dashboard'">📊 Dashboard</button>
    <button class="nav-btn" onclick="window.location.href='?page=Leaderboard'">🏆 Leaderboard</button>
    <button class="nav-btn" onclick="window.location.href='?page=Action Plan'">📋 Action Plan</button>
    <button class="nav-btn" onclick="window.location.href='?page=Simulator'">🌡️ Simulator</button>
    <button class="nav-btn" onclick="window.location.href='?page=Community'">🌱 Community</button>
    <button class="nav-btn" onclick="window.location.href='?page=Data Entry'">📥 Data Entry</button>
</div>
""", unsafe_allow_html=True)

# Handle navigation via query params
query_params = st.query_params
if 'page' in query_params:
    st.session_state.page = query_params['page']

# Active page display
page = st.session_state.page

# ===== SCHOOL PROFILE HEADER =====
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown(f"""
    <div class="profile-header" style="text-align: center;">
        <h2>🌱 {school_name if 'school_name' in dir() else 'Washington Middle School'}</h2>
        <p>Environmental Profile · AI-Powered Insights</p>
    </div>
    """, unsafe_allow_html=True)

# ===== SIDEBAR (Minimal - Only for settings) =====
with st.sidebar:
    st.markdown("### ⚙️ Settings")
    school_name = st.text_input("School Name:", value="Washington Middle School")
    st.markdown("---")
    if st.button("🤖 Why AI?", use_container_width=True):
        st.info("AI analyzes transportation, waste, and energy data to find the highest-impact actions for YOUR school.")
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
if page == "Dashboard":
    st.markdown('<div class="section-header">📊 Environmental Dashboard</div>', unsafe_allow_html=True)
    
    # Hexagon Chart
    st.markdown('<div class="hexagon-container">', unsafe_allow_html=True)
    st.markdown('<h3 style="text-align: center; margin-bottom: 1rem;">🌿 Environmental Profile</h3>', unsafe_allow_html=True)
    
    hex_fig = create_hexagon_chart(environmental_profile, f"{school_name} - 6 Pillars of Sustainability")
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

# ===== LEADERBOARD PAGE =====
elif page == "Leaderboard":
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
elif page == "Action Plan":
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

# ===== SIMULATOR PAGE =====
elif page == "Simulator":
    st.markdown('<div class="section-header">🌡️ What If Simulator</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        trees = st.slider("🌳 Trees to plant:", 0, 100, 20)
        st.metric("Temperature Reduction", f"-{trees * 0.3:.1f}°F")
    with col2:
        walk_pct = st.slider("🚶 Increase walk/bike by:", 0, 100, 20)
        st.metric("Fewer Solo Cars Daily", f"-{int(54 * walk_pct / 100)}")

# ===== COMMUNITY PAGE =====
elif page == "Community":
    st.markdown('<div class="section-header">🌱 Community Action Tracker</div>', unsafe_allow_html=True)
    
    actions = ["🌳 Planted a tree", "🚗 Started carpooling", "🗑️ Waste audit", "💡 Energy monitors", "💧 Water station"]
    selected = st.selectbox("What did your school do?", actions)
    
    if st.button("✅ Log Action"):
        st.balloons()
        st.success("Thanks for helping! 🌍")

# ===== DATA ENTRY PAGE =====
elif page == "Data Entry":
    st.markdown('<div class="section-header">📥 Enter School Data</div>', unsafe_allow_html=True)
    
    with st.form("data_form"):
        walk = st.number_input("Students who walked:", 0, 500, 135)
        bike = st.number_input("Students who biked:", 0, 500, 45)
        submitted = st.form_submit_button("💾 Save")
        if submitted:
            st.success("Data saved!")

# ===== FOOTER =====
st.markdown("""
<div class="footer">
    <strong>🌱 Eco-School Dashboard</strong> · AI-powered · Built for USAII Hackathon 2026
</div>
""", unsafe_allow_html=True)