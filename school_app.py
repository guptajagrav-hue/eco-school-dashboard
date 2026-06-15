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

# ===== DARK MODE STATE =====
if 'dark_mode' not in st.session_state:
    st.session_state.dark_mode = False

# ===== CUSTOM CSS WITH ANIMATED TOGGLE =====
def get_css(dark_mode):
    if dark_mode:
        return """
        <style>
        /* Dark mode styles */
        .stApp { background: linear-gradient(135deg, #070b1d 0%, #101425 100%); }
        .metric-card { background: #0f3460; color: white; box-shadow: 0 8px 20px rgba(0,0,0,0.3); border-radius: 20px; padding: 1.2rem; text-align: center; transition: transform 0.2s; margin-bottom: 1rem; }
        .metric-card:hover { transform: translateY(-5px); background: #1a1a2e; }
        .metric-value { font-size: 2.2rem; font-weight: 800; color: white; }
        .metric-label { font-size: 0.85rem; text-transform: uppercase; letter-spacing: 1px; font-weight: 600; color: #a4a5b8; }
        .metric-sub { font-size: 0.7rem; color: #a0aec0; }
        .section-header { font-size: 1.5rem; font-weight: 700; color: #00b894; margin-top: 1.5rem; margin-bottom: 1rem; border-left: 4px solid #00b894; padding-left: 1rem; }
        .leaderboard-item { padding: 0.8rem 1rem; margin: 0.5rem 0; border-radius: 12px; background: #0f3460; color: white; display: flex; justify-content: space-between; align-items: center; }
        .footer { text-align: center; padding: 2rem; color: #718096; font-size: 0.8rem; border-top: 1px solid #2d3436; margin-top: 2rem; }
        .profile-box { background: #0f3460; border-radius: 24px; padding: 1.5rem; text-align: center; margin-bottom: 1rem; }
        .profile-box h3 { color: white; }
        .stMarkdown, .stText, label, .stMetric label, .stNumberInput label, .stSelectbox label, .stRadio label, .stSlider label, .stCheckbox label { color: #ffffff !important; }
        .stMetric div[data-testid="stMetricValue"] { color: #00b894 !important; }
        .stButton > button { background: linear-gradient(135deg, #00b894 0%, #55efc4 100%); color: #1a1a2e; border-radius: 30px; transition: all 0.2s; }
        .stButton > button:hover { transform: scale(1.02); }
        [data-testid="stSidebar"] { background: #0f3460; }
        [data-testid="stSidebar"] * { color: white !important; }
        .stTextInput > div > div > input { background-color: #1a1a2e !important; color: #ffffff !important; border: 1px solid #00b894 !important; border-radius: 8px !important; }
        /* Animated Toggle Button */
        .theme-switch {
            background: #101425;
            border: none;
            border-radius: 50%;
            width: 50px;
            height: 50px;
            padding: 0;
            cursor: pointer;
            transition: all 0.3s ease;
            display: flex;
            justify-content: center;
            align-items: center;
        }
        .theme-switch:hover {
            transform: scale(1.05);
            background: #1a1a2e;
        }
        .theme-switch svg {
            fill: #a4a5b8;
            transition: fill 0.3s ease;
        }
        .card-green { background: linear-gradient(135deg, #00b894 0%, #55efc4 100%); color: white; }
        .card-blue { background: linear-gradient(135deg, #1e6f9f 0%, #3b82f6 100%); color: white; }
        .card-orange { background: linear-gradient(135deg, #d97706 0%, #f59e0b 100%); color: white; }
        .card-red { background: linear-gradient(135deg, #dc2626 0%, #ef4444 100%); color: white; }
        .card-purple { background: linear-gradient(135deg, #7c3aed 0%, #a78bfa 100%); color: white; }
        .card-teal { background: linear-gradient(135deg, #0d9488 0%, #14b8a6 100%); color: white; }
        </style>
        """
    else:
        return """
        <style>
        /* Light mode styles */
        .stApp { background: linear-gradient(135deg, #f5f7fa 0%, #e8edf2 100%); }
        .metric-card { background: white; color: #111528; box-shadow: 0 8px 20px rgba(0,0,0,0.08); border-radius: 20px; padding: 1.2rem; text-align: center; transition: transform 0.2s; margin-bottom: 1rem; }
        .metric-card:hover { transform: translateY(-5px); box-shadow: 0 15px 30px rgba(0,0,0,0.12); }
        .metric-value { font-size: 2.2rem; font-weight: 800; color: #111528; }
        .metric-label { font-size: 0.85rem; text-transform: uppercase; letter-spacing: 1px; font-weight: 600; color: #232738; }
        .metric-sub { font-size: 0.7rem; color: #718096; }
        .section-header { font-size: 1.5rem; font-weight: 700; color: #111528; margin-top: 1.5rem; margin-bottom: 1rem; border-left: 4px solid #2e8b57; padding-left: 1rem; }
        .leaderboard-item { padding: 0.8rem 1rem; margin: 0.5rem 0; border-radius: 12px; background: #f8faf8; color: #111528; display: flex; justify-content: space-between; align-items: center; }
        .footer { text-align: center; padding: 2rem; color: #718096; font-size: 0.8rem; border-top: 1px solid #e2e8f0; margin-top: 2rem; }
        .profile-box { background: white; border-radius: 24px; padding: 1.5rem; text-align: center; margin-bottom: 1rem; }
        .profile-box h3 { color: #111528; }
        .stMarkdown, .stText, label, .stMetric label, .stNumberInput label, .stSelectbox label, .stRadio label, .stSlider label, .stCheckbox label { color: #111528 !important; }
        .stMetric div[data-testid="stMetricValue"] { color: #2e8b57 !important; }
        .stButton > button { background: linear-gradient(135deg, #2e8b57 0%, #3cb371 100%); color: white; border-radius: 30px; transition: all 0.2s; }
        .stButton > button:hover { transform: scale(1.02); }
        [data-testid="stSidebar"] { background: #ffffff; }
        [data-testid="stSidebar"] * { color: #111528 !important; }
        .stTextInput > div > div > input { background-color: #ffffff !important; color: #111528 !important; border: 1px solid #cbd5e1 !important; border-radius: 8px !important; }
        /* Animated Toggle Button */
        .theme-switch {
            background: #e8e9ed;
            border: none;
            border-radius: 50%;
            width: 50px;
            height: 50px;
            padding: 0;
            cursor: pointer;
            transition: all 0.3s ease;
            display: flex;
            justify-content: center;
            align-items: center;
        }
        .theme-switch:hover {
            transform: scale(1.05);
            background: #d0d1d5;
        }
        .theme-switch svg {
            fill: #3a435d;
            transition: fill 0.3s ease;
        }
        .card-green { background: linear-gradient(135deg, #2e8b57 0%, #3cb371 100%); color: white; }
        .card-blue { background: linear-gradient(135deg, #1e6f9f 0%, #3b82f6 100%); color: white; }
        .card-orange { background: linear-gradient(135deg, #d97706 0%, #f59e0b 100%); color: white; }
        .card-red { background: linear-gradient(135deg, #dc2626 0%, #ef4444 100%); color: white; }
        .card-purple { background: linear-gradient(135deg, #7c3aed 0%, #a78bfa 100%); color: white; }
        .card-teal { background: linear-gradient(135deg, #0d9488 0%, #14b8a6 100%); color: white; }
        </style>
        """

# Apply CSS
st.markdown(get_css(st.session_state.dark_mode), unsafe_allow_html=True)

# ===== ANIMATED TOGGLE BUTTON (Sun/Moon Icons) =====
# SVG icons (same as your reference)
sun_svg = '<svg xmlns="http://www.w3.org/2000/svg" height="24px" viewBox="0 -960 960 960" width="24px" fill="currentColor"><path d="M480-120q-150 0-255-105T120-480q0-150 105-255t255-105q14 0 27.5 1t26.5 3q-41 29-65.5 75.5T444-660q0 90 63 153t153 63q55 0 101-24.5t75-65.5q2 13 3 26.5t1 27.5q0 150-105 255T480-120Z"/></svg>'
moon_svg = '<svg xmlns="http://www.w3.org/2000/svg" height="24px" viewBox="0 -960 960 960" width="24px" fill="currentColor"><path d="M480-280q-83 0-141.5-58.5T280-480q0-83 58.5-141.5T480-680q83 0 141.5 58.5T680-480q0 83-58.5 141.5T480-280ZM200-440H40v-80h160v80Zm720 0H760v-80h160v80ZM440-760v-160h80v160h-80Zm0 720v-160h80v160h-80ZM256-650l-101-97 57-59 96 100-52 56Zm492 496-97-101 53-55 101 97-57 59Zm-98-550 97-101 59 57-100 96-56-52ZM154-212l101-97 55 53-97 101-59-57Z"/></svg>'

# Header with toggle
col_title, col_toggle = st.columns([4, 1])
with col_title:
    st.markdown('<h1 style="margin: 0; text-align: center;">🌱 Eco-School Dashboard</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; margin-top: 0;">Track your school\'s environmental impact · AI-powered insights</p>', unsafe_allow_html=True)
with col_toggle:
    # Display the appropriate icon based on current mode
    if st.session_state.dark_mode:
        toggle_html = f'<button class="theme-switch" id="themeToggle">{moon_svg}</button>'
    else:
        toggle_html = f'<button class="theme-switch" id="themeToggle">{sun_svg}</button>'
    
    st.markdown(toggle_html, unsafe_allow_html=True)
    
    # JavaScript to handle toggle click and rerun Streamlit
    st.markdown("""
    <script>
        const toggleBtn = document.getElementById('themeToggle');
        if (toggleBtn) {
            toggleBtn.addEventListener('click', () => {
                const url = new URL(window.location.href);
                const currentMode = url.searchParams.get('dark_mode');
                if (currentMode === 'true') {
                    url.searchParams.delete('dark_mode');
                } else {
                    url.searchParams.set('dark_mode', 'true');
                }
                window.location.href = url;
            });
        }
    </script>
    """, unsafe_allow_html=True)

# Check URL params for dark mode toggle
query_params = st.query_params
if 'dark_mode' in query_params and query_params['dark_mode'] == 'true':
    if not st.session_state.dark_mode:
        st.session_state.dark_mode = True
        st.rerun()
elif 'dark_mode' not in query_params and st.session_state.dark_mode:
    st.session_state.dark_mode = False
    st.rerun()

# ===== SESSION STATE FOR NAVIGATION =====
if 'page' not in st.session_state:
    st.session_state.page = "Dashboard"

# ===== FUNCTION TO CHANGE PAGE =====
def set_page(page_name):
    st.session_state.page = page_name
    st.rerun()

# ===== NAVIGATION BUTTONS =====
st.markdown('<div style="display: flex; justify-content: center; gap: 0.8rem; flex-wrap: wrap; margin: 1rem 0; padding: 0.5rem; background: white; border-radius: 50px; box-shadow: 0 2px 8px rgba(0,0,0,0.05);">', unsafe_allow_html=True)

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
<div style="background: linear-gradient(135deg, #2e8b57 0%, #3cb371 100%); border-radius: 24px; padding: 1.5rem; color: white; margin-bottom: 1rem; text-align: center;">
    <h2 style="margin: 0;">🌱 {school_name}</h2>
    <p style="margin: 0; opacity: 0.9;">Environmental Profile · AI-Powered Insights</p>
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
    
    # Hexagon Chart
    st.markdown('<div class="profile-box">', unsafe_allow_html=True)
    st.markdown('<h3 style="text-align: center; margin-bottom: 1rem;">🌿 Environmental Profile</h3>', unsafe_allow_html=True)
    hex_fig = create_hexagon_chart(environmental_profile, f"{school_name_input} - 6 Pillars of Sustainability")
    st.plotly_chart(hex_fig, use_container_width=True)
    avg_score = sum(environmental_profile.values()) / len(environmental_profile)
    st.markdown(f"""
    <div style="text-align: center; margin-top: 0.5rem;">
        <span style="background: #2e8b57; color: white; padding: 0.5rem 1.5rem; border-radius: 30px; font-weight: bold;">🌟 Overall Score: {avg_score:.0f}/100</span>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Metrics Row
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f'<div class="metric-card card-green"><div class="metric-value">{school_data["trees"]}<span style="font-size:1rem;"> / {school_data["goal_trees"]}</span></div><div class="metric-label">🌳 Trees on Campus</div></div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div class="metric-card card-blue"><div class="metric-value">{school_data["walk_bike"]}<span style="font-size:1rem;">%</span></div><div class="metric-label">🚶 Walk/Bike to School</div></div>', unsafe_allow_html=True)
    with col3:
        st.markdown(f'<div class="metric-card card-purple"><div class="metric-value">{school_data["recycle"]}<span style="font-size:1rem;">%</span></div><div class="metric-label">♻️ Waste Diverted</div></div>', unsafe_allow_html=True)
    with col4:
        st.markdown(f'<div class="metric-card card-teal"><div class="metric-value">{school_data["bottles"]}</div><div class="metric-label">💧 Bottles Saved/Week</div></div>', unsafe_allow_html=True)
    
    # Problem Areas
    st.markdown('<div class="section-header">⚠️ Areas Needing Attention</div>', unsafe_allow_html=True)
    col5, col6, col7 = st.columns(3)
    with col5:
        st.markdown(f'<div class="metric-card card-red"><div class="metric-value">{school_data["car_alone"]}</div><div class="metric-label">🚗 Solo Cars Daily</div></div>', unsafe_allow_html=True)
    with col6:
        st.markdown(f'<div class="metric-card card-orange"><div class="metric-value">{school_data["food_waste"]}<span style="font-size:1rem;"> lbs</span></div><div class="metric-label">🍎 Food Wasted Daily</div></div>', unsafe_allow_html=True)
    with col7:
        st.markdown(f'<div class="metric-card" style="background: linear-gradient(135deg, #4b5563 0%, #9ca3af 100%); color: white;"><div class="metric-value">{school_data["paper_reams"]}<span style="font-size:1rem;"> reams</span></div><div class="metric-label">📄 Paper/Week</div></div>', unsafe_allow_html=True)
    
    # AI Feature: Smart Anomaly Detection
    st.markdown('<div class="section-header">🤖 AI Insights</div>', unsafe_allow_html=True)
    if os.path.exists(data_file):
        history = pd.read_csv(data_file)
        if len(history) > 3:
            walk_mean = history['walk'].mean()
            walk_std = history['walk'].std()
            last_walk = history['walk'].iloc[-1]
            if last_walk < walk_mean - 2 * walk_std:
                st.warning("🚨 AI Alert: Unusual drop in students walking to school!")
            elif last_walk > walk_mean + 2 * walk_std:
                st.success("🎉 AI Insight: Walking to school is at an all-time high!")
            else:
                st.info("✅ AI Analysis: Walking trends are stable.")
            
            waste_mean = history['food_waste_lbs'].mean()
            waste_std = history['food_waste_lbs'].std()
            last_waste = history['food_waste_lbs'].iloc[-1]
            if last_waste > waste_mean + waste_std:
                st.warning("🚨 AI Alert: Food waste is higher than usual!")
            elif last_waste < waste_mean - waste_std:
                st.success("🎉 AI Insight: Food waste is down!")
        else:
            st.info("📊 AI needs at least 4 days of data to detect patterns.")
    
    # AI Feature: Peer School Comparison
    if os.path.exists(data_file):
        history = pd.read_csv(data_file)
        if len(history) > 3:
            st.markdown('<div class="section-header">🏫 How You Compare to National Average</div>', unsafe_allow_html=True)
            total_walk = history['walk'].sum()
            total_car = history['car_alone'].sum()
            your_walk_rate = total_walk / (total_walk + total_car) * 100 if (total_walk + total_car) > 0 else 0
            national_avg = 45
            
            if your_walk_rate > national_avg:
                st.success(f"✅ Your school ({your_walk_rate:.0f}% walk) beats the national average of {national_avg}%!")
            else:
                st.warning(f"⚠️ Your school ({your_walk_rate:.0f}% walk) is below the national average of {national_avg}%.")

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
        st.markdown(f'<div class="leaderboard-item"><span><b>{medal}</b></span><span><b>{item["room"]}</b></span><span><b style="color: #2e8b57;">{item["score"]} points</b></span><span>{lights_status}</span></div>', unsafe_allow_html=True)

# ===== ACTION PLAN PAGE =====
elif st.session_state.page == "Action Plan":
    st.markdown('<div class="section-header">📋 Custom Action Plan</div>', unsafe_allow_html=True)
    
    if st.session_state.dark_mode:
        bg1, bg2, bg3 = "#2d1a1a", "#2d2a1a", "#1a2d1a"
        text_color = "white"
    else:
        bg1, bg2, bg3 = "#fef2f2", "#fffbeb", "#ecfdf5"
        text_color = "#1a202c"
    
    st.markdown(f'<div style="padding: 1rem; margin: 1rem 0; border-radius: 16px; border-left: 4px solid #dc2626; background: {bg1}; color: {text_color};"><strong>🔴 PRIORITY 1: Reduce Solo Car Drop-offs</strong><br>🚗 {school_data["car_alone"]} solo cars daily → Save {school_data["co2_save"]} lbs CO2/week</div>', unsafe_allow_html=True)
    st.markdown(f'<div style="padding: 1rem; margin: 1rem 0; border-radius: 16px; border-left: 4px solid #f59e0b; background: {bg2}; color: {text_color};"><strong>🟠 PRIORITY 2: Stop Wasting Food</strong><br>🍎 {school_data["food_waste"]} lbs wasted daily → Divert {school_data["food_waste"] * 180:,} lbs/year</div>', unsafe_allow_html=True)
    st.markdown(f'<div style="padding: 1rem; margin: 1rem 0; border-radius: 16px; border-left: 4px solid #10b981; background: {bg3}; color: {text_color};"><strong>🟢 PRIORITY 3: Turn Off Lights</strong><br>💡 {school_data["lights_on"]} classrooms leave lights on → Save $50/month</div>', unsafe_allow_html=True)
    
    # AI Feature: Personalized Recommendations
    if os.path.exists(data_file):
        history = pd.read_csv(data_file)
        if len(history) > 3:
            st.markdown("### 🤖 AI-Powered Custom Recommendations")
            walk_rate = history['walk'].mean() / (history['walk'].mean() + history['car_alone'].mean()) * 100 if (history['walk'].mean() + history['car_alone'].mean()) > 0 else 50
            waste_avg = history['food_waste_lbs'].mean()
            lights_avg = history['lights_left_on'].mean()
            
            if walk_rate < 40:
                st.info(f"🚶 **Low walking rate** — Only {walk_rate:.0f}% walk vs car.")
            if waste_avg > 25:
                st.info(f"🍎 **High food waste** — Average {waste_avg:.0f} lbs/day.")
            if lights_avg > 3:
                st.info(f"💡 **Lights left on** — Average {lights_avg:.0f} classrooms.")
            if walk_rate >= 40 and waste_avg <= 25 and lights_avg <= 3:
                st.success("🎉 Your school is doing great across all metrics!")
    
    # AI Feature: Smart Goal Setting
    if os.path.exists(data_file):
        history = pd.read_csv(data_file)
        if len(history) > 3:
            st.markdown("### 🎯 AI-Generated Goals")
            col_goal1, col_goal2 = st.columns(2)
            with col_goal1:
                walk_last = history['walk'].iloc[-1]
                goal_30d = walk_last + 10
                st.metric("🤖 30-Day Walk Goal", f"{int(goal_30d)} students", delta="Aim for +10 students")
            with col_goal2:
                waste_last = history['food_waste_lbs'].iloc[-1]
                goal_30d_waste = max(0, waste_last - 5)
                st.metric("🤖 30-Day Waste Goal", f"{int(goal_30d_waste)} lbs", delta="Aim for -5 lbs")

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
    
    # AI Feature: Trend Prediction
    if os.path.exists(data_file):
        history = pd.read_csv(data_file)
        if len(history) > 3:
            st.markdown("---")
            st.markdown("### 🤖 AI Trend Prediction")
            days = np.array(range(len(history))).reshape(-1, 1)
            walks = history['walk'].values
            model = LinearRegression()
            model.fit(days, walks)
            future_days = np.array(range(len(history), len(history) + 30)).reshape(-1, 1)
            future_walks = model.predict(future_days)
            st.metric("🤖 AI Predicts: Walkers in 30 days", f"{int(future_walks[-1])} students", delta=f"{int(future_walks[-1] - history['walk'].iloc[-1]):+d}")
            
            pred_days = list(range(len(history) + 30))
            pred_walks = list(walks) + list(future_walks)
            fig_pred = go.Figure()
            fig_pred.add_trace(go.Scatter(x=list(range(len(history))), y=walks, mode='lines+markers', name='Actual Data', line=dict(color='#2e8b57')))
            fig_pred.add_trace(go.Scatter(x=list(range(len(history), len(history) + 30)), y=future_walks, mode='lines', name='AI Prediction', line=dict(color='#f59e0b', dash='dash')))
            fig_pred.update_layout(title='AI Predicted Walking Trend (Next 30 Days)', xaxis_title='Days', yaxis_title='Students Walking')
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
    
    col_clear1, col_clear2 = st.columns([4, 1])
    with col_clear2:
        if st.button("🗑️ Clear All Data", type="secondary", use_container_width=True):
            if os.path.exists(data_file):
                os.remove(data_file)
                st.success("✅ All data cleared successfully!")
                st.rerun()
    
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
            new_data = pd.DataFrame([{"date": date, "walk": walk, "bike": bike, "car_alone": car_alone, "total_students": walk + bike + car_alone, "food_waste_lbs": food_waste, "lights_left_on": lights_left}])
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
        st.dataframe(history.sort_values("date", ascending=False), use_container_width=True)
        
        csv = history.to_csv(index=False)
        st.download_button("📥 Download All Data as CSV", data=csv, file_name=f"eco_school_data_{datetime.now().strftime('%Y%m%d')}.csv", mime="text/csv")

# ===== FOOTER =====
st.markdown("""
<div style="text-align: center; padding: 2rem; color: #718096; font-size: 0.8rem; border-top: 1px solid #e2e8f0; margin-top: 2rem;">
    <strong>🌱 Eco-School Dashboard</strong> · AI-powered · Built for USAII Hackathon 2026
</div>
""", unsafe_allow_html=True)