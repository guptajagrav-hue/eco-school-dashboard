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

# ===== DARK MODE CSS (FULL TEXT COLOR SUPPORT) =====
def get_dark_mode_css():
    return """
    <style>
    /* Main background */
    .stApp {
        background: linear-gradient(135deg, #0f1722 0%, #1a1f2e 100%);
    }
    
    /* All main text */
    .stMarkdown, .stText, .stTitle, .stHeader, .stSubheader, 
    .stCaption, p, h1, h2, h3, h4, .stMetric label, 
    .stNumberInput label, .stSelectbox label, .stRadio label, 
    .stSlider label, .stCheckbox label, .stTextInput label {
        color: #f0f3f8 !important;
    }
    
    /* Metric cards */
    .metric-card {
        background: #1e2a3a;
        border-radius: 20px;
        padding: 1.2rem;
        text-align: center;
        margin-bottom: 1rem;
        box-shadow: 0 8px 20px rgba(0,0,0,0.3);
        transition: transform 0.2s;
    }
    .metric-card:hover {
        transform: translateY(-5px);
        background: #2a3a4a;
    }
    .metric-value {
        font-size: 2.2rem;
        font-weight: 800;
        color: #86efac !important;
    }
    .metric-label {
        font-size: 0.85rem;
        text-transform: uppercase;
        letter-spacing: 1px;
        color: #cbd5e6 !important;
    }
    .metric-sub {
        font-size: 0.7rem;
        color: #94a3b8 !important;
    }
    
    /* Section headers */
    .section-header {
        font-size: 1.5rem;
        font-weight: 700;
        color: #86efac !important;
        margin-top: 1.5rem;
        margin-bottom: 1rem;
        border-left: 4px solid #86efac;
        padding-left: 1rem;
    }
    
    /* Leaderboard items */
    .leaderboard-item {
        background: #1e2a3a;
        color: #f0f3f8;
        padding: 0.8rem 1rem;
        border-radius: 12px;
        margin: 0.5rem 0;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    
    /* Profile box */
    .profile-box {
        background: #1e2a3a;
        border-radius: 24px;
        padding: 1.5rem;
        text-align: center;
        margin-bottom: 1rem;
    }
    .profile-box h3 {
        color: #f0f3f8 !important;
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background: #0f1722;
    }
    [data-testid="stSidebar"] * {
        color: #f0f3f8 !important;
    }
    [data-testid="stSidebar"] .stTextInput > div > div > input {
        background-color: #1e2a3a !important;
        color: #f0f3f8 !important;
        border: 1px solid #86efac !important;
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #86efac 0%, #4ade80 100%);
        color: #0f1722 !important;
        border-radius: 30px;
        font-weight: 600;
    }
    .stButton > button:hover {
        transform: scale(1.02);
    }
    
    /* Metric values */
    .stMetric div[data-testid="stMetricValue"] {
        color: #86efac !important;
    }
    .stMetric div[data-testid="stMetricDelta"] {
        color: #4ade80 !important;
    }
    
    /* Dataframe */
    .stDataFrame, div[data-testid="stDataFrame"] table, 
    div[data-testid="stDataFrame"] th, div[data-testid="stDataFrame"] td {
        color: #f0f3f8 !important;
        background-color: #1e2a3a !important;
    }
    
    /* Info/Warning/Success boxes */
    .stInfo, .stWarning, .stSuccess, .stError {
        background-color: #1e2a3a !important;
        color: #f0f3f8 !important;
    }
    .stInfo { border-left-color: #86efac !important; }
    
    /* Footer */
    .footer {
        text-align: center;
        padding: 2rem;
        color: #94a3b8;
        font-size: 0.8rem;
        border-top: 1px solid #334155;
        margin-top: 2rem;
    }
    
    /* Card backgrounds */
    .card-green { background: linear-gradient(135deg, #065f46 0%, #047857 100%); color: white; }
    .card-blue { background: linear-gradient(135deg, #1e3a5f 0%, #1e40af 100%); color: white; }
    .card-orange { background: linear-gradient(135deg, #78350f 0%, #9a3412 100%); color: white; }
    .card-red { background: linear-gradient(135deg, #7f1d1d 0%, #991b1b 100%); color: white; }
    .card-purple { background: linear-gradient(135deg, #4c1d95 0%, #6d28d9 100%); color: white; }
    .card-teal { background: linear-gradient(135deg, #134e4a 0%, #0f766e 100%); color: white; }
    </style>
    """

def get_light_mode_css():
    return """
    <style>
    /* Main background */
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #e8edf2 100%);
    }
    
    /* All main text */
    .stMarkdown, .stText, .stTitle, .stHeader, .stSubheader, 
    .stCaption, p, h1, h2, h3, h4, .stMetric label, 
    .stNumberInput label, .stSelectbox label, .stRadio label, 
    .stSlider label, .stCheckbox label, .stTextInput label {
        color: #1a202c !important;
    }
    
    /* Metric cards */
    .metric-card {
        background: white;
        border-radius: 20px;
        padding: 1.2rem;
        text-align: center;
        margin-bottom: 1rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        transition: transform 0.2s;
    }
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 20px rgba(0,0,0,0.1);
    }
    .metric-value {
        font-size: 2.2rem;
        font-weight: 800;
        color: #1a202c !important;
    }
    .metric-label {
        font-size: 0.85rem;
        text-transform: uppercase;
        letter-spacing: 1px;
        color: #4a5568 !important;
    }
    .metric-sub {
        font-size: 0.7rem;
        color: #718096 !important;
    }
    
    /* Section headers */
    .section-header {
        font-size: 1.5rem;
        font-weight: 700;
        color: #1a202c !important;
        margin-top: 1.5rem;
        margin-bottom: 1rem;
        border-left: 4px solid #2e8b57;
        padding-left: 1rem;
    }
    
    /* Leaderboard items */
    .leaderboard-item {
        background: #f8faf8;
        color: #1a202c;
        padding: 0.8rem 1rem;
        border-radius: 12px;
        margin: 0.5rem 0;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    
    /* Profile box */
    .profile-box {
        background: white;
        border-radius: 24px;
        padding: 1.5rem;
        text-align: center;
        margin-bottom: 1rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    }
    .profile-box h3 {
        color: #1a202c !important;
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background: #ffffff;
    }
    [data-testid="stSidebar"] * {
        color: #1a202c !important;
    }
    [data-testid="stSidebar"] .stTextInput > div > div > input {
        background-color: #ffffff !important;
        color: #1a202c !important;
        border: 1px solid #cbd5e1 !important;
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #2e8b57 0%, #3cb371 100%);
        color: white !important;
        border-radius: 30px;
        font-weight: 600;
    }
    .stButton > button:hover {
        transform: scale(1.02);
    }
    
    /* Metric values */
    .stMetric div[data-testid="stMetricValue"] {
        color: #2e8b57 !important;
    }
    
    /* Info/Warning/Success boxes */
    .stInfo { background-color: #e8f0fe !important; color: #1a202c !important; }
    .stWarning { background-color: #fff5f0 !important; color: #c53030 !important; }
    .stSuccess { background-color: #e6f7e6 !important; color: #2e8b57 !important; }
    
    /* Footer */
    .footer {
        text-align: center;
        padding: 2rem;
        color: #718096;
        font-size: 0.8rem;
        border-top: 1px solid #e2e8f0;
        margin-top: 2rem;
    }
    
    /* Card backgrounds */
    .card-green { background: linear-gradient(135deg, #2e8b57 0%, #3cb371 100%); color: white; }
    .card-blue { background: linear-gradient(135deg, #1e6f9f 0%, #3b82f6 100%); color: white; }
    .card-orange { background: linear-gradient(135deg, #d97706 0%, #f59e0b 100%); color: white; }
    .card-red { background: linear-gradient(135deg, #dc2626 0%, #ef4444 100%); color: white; }
    .card-purple { background: linear-gradient(135deg, #7c3aed 0%, #a78bfa 100%); color: white; }
    .card-teal { background: linear-gradient(135deg, #0d9488 0%, #14b8a6 100%); color: white; }
    </style>
    """

# Apply the correct CSS based on dark mode
if st.session_state.dark_mode:
    st.markdown(get_dark_mode_css(), unsafe_allow_html=True)
else:
    st.markdown(get_light_mode_css(), unsafe_allow_html=True)

# ===== HEADER WITH TOGGLE =====
col_title, col_toggle = st.columns([4, 1])
with col_title:
    st.markdown('<h1 style="text-align: center;">🌱 Eco-School Dashboard</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center;">Track your school\'s environmental impact · AI-powered insights</p>', unsafe_allow_html=True)
with col_toggle:
    # Toggle with correct text for each mode
    if st.session_state.dark_mode:
        toggle_label = "☀️ Light Mode"
    else:
        toggle_label = "🌙 Dark Mode"
    
    new_mode = st.toggle(toggle_label, value=st.session_state.dark_mode)
    if new_mode != st.session_state.dark_mode:
        st.session_state.dark_mode = new_mode
        st.rerun()
# ===== NAVIGATION =====
if 'page' not in st.session_state:
    st.session_state.page = "Dashboard"

def set_page(page_name):
    st.session_state.page = page_name
    st.rerun()

# Navigation buttons
st.markdown('<div style="display: flex; justify-content: center; gap: 0.8rem; flex-wrap: wrap; margin: 1rem 0; padding: 0.5rem; background: white; border-radius: 50px; box-shadow: 0 2px 8px rgba(0,0,0,0.05);">', unsafe_allow_html=True)

cols = st.columns(6)
with cols[0]:
    if st.button("📊 Dashboard", use_container_width=True):
        set_page("Dashboard")
with cols[1]:
    if st.button("🏆 Leaderboard", use_container_width=True):
        set_page("Leaderboard")
with cols[2]:
    if st.button("📋 Action Plan", use_container_width=True):
        set_page("Action Plan")
with cols[3]:
    if st.button("🌡️ Simulator", use_container_width=True):
        set_page("Simulator")
with cols[4]:
    if st.button("🌱 Community", use_container_width=True):
        set_page("Community")
with cols[5]:
    if st.button("📥 Data Entry", use_container_width=True):
        set_page("Data Entry")

st.markdown('</div>', unsafe_allow_html=True)

# ===== SCHOOL HEADER =====
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
    
    data_file = "school_data_log.csv"
    if os.path.exists(data_file):
        file_size = os.path.getsize(data_file) // 1024
        st.success(f"✅ {file_size} KB of data saved")

# ===== DEMO DATA =====
data_file = "school_data_log.csv"
if not os.path.exists(data_file):
    demo_data = pd.DataFrame([
        {"date": "2026-06-10", "walk": 120, "bike": 40, "car_alone": 60, "food_waste_lbs": 28, "lights_left_on": 6},
        {"date": "2026-06-11", "walk": 125, "bike": 42, "car_alone": 58, "food_waste_lbs": 26, "lights_left_on": 5},
        {"date": "2026-06-12", "walk": 130, "bike": 44, "car_alone": 55, "food_waste_lbs": 25, "lights_left_on": 5},
        {"date": "2026-06-13", "walk": 135, "bike": 45, "car_alone": 54, "food_waste_lbs": 24, "lights_left_on": 4},
        {"date": "2026-06-14", "walk": 140, "bike": 46, "car_alone": 52, "food_waste_lbs": 22, "lights_left_on": 4},
        {"date": "2026-06-15", "walk": 145, "bike": 47, "car_alone": 50, "food_waste_lbs": 21, "lights_left_on": 3},
    ])
    demo_data.to_csv(data_file, index=False)

# ===== SCHOOL DATA =====
school_data = {
    "trees": 31, "goal_trees": 50, "walk_bike": 40, "goal_walk_bike": 50,
    "recycle": 55, "goal_recycle": 70, "car_alone": 54, "food_waste": 24,
    "lights_on": 5, "paper_reams": 12, "bottles": 392, "co2_save": 1200,
    "classrooms": {
        "Room 101": {"score": 45, "lights": False},
        "Room 102": {"score": 95, "lights": True},
        "Room 103": {"score": 60, "lights": False},
        "Room 104": {"score": 80, "lights": True},
        "Room 105": {"score": 25, "lights": False},
    }
}

# ===== ENVIRONMENTAL PROFILE =====
environmental_profile = {
    "🌳 Tree Canopy": min(100, (school_data["trees"] / school_data["goal_trees"]) * 100),
    "🚶 Active Transport": min(100, (school_data["walk_bike"] / school_data["goal_walk_bike"]) * 100),
    "♻️ Waste Diversion": min(100, (school_data["recycle"] / school_data["goal_recycle"]) * 100),
    "💡 Energy Efficiency": min(100, max(0, 100 - (school_data["lights_on"] * 8))),
    "📄 Paper Reduction": min(100, max(0, 100 - ((school_data["paper_reams"] - 8) / 8 * 100))),
    "💧 Water Conservation": min(100, (school_data["bottles"] / 500) * 100),
}

# ===== HEXAGON CHART =====
def create_hexagon_chart(scores, title="Environmental Profile"):
    categories = list(scores.keys())
    values = list(scores.values())
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(r=values, theta=categories, fill='toself', name='Your School', line_color='#2e8b57', fillcolor='rgba(46, 139, 86, 0.3)'))
    fig.add_trace(go.Scatterpolar(r=[100] * len(categories), theta=categories, name='Goal (100%)', line_color='#cbd5e1', line_dash='dash'))
    fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 100]), angularaxis=dict(tickfont=dict(size=12))), height=500, showlegend=True, legend=dict(x=0.5, y=-0.1, orientation='h'))
    return fig

# ===== DASHBOARD PAGE =====
if st.session_state.page == "Dashboard":
    st.markdown('<div class="section-header">📊 Environmental Dashboard</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="profile-box">', unsafe_allow_html=True)
    st.markdown('<h3 style="text-align: center;">🌿 Environmental Profile</h3>', unsafe_allow_html=True)
    hex_fig = create_hexagon_chart(environmental_profile)
    st.plotly_chart(hex_fig, use_container_width=True)
    avg_score = sum(environmental_profile.values()) / len(environmental_profile)
    st.markdown(f'<div style="text-align: center;"><span style="background: #2e8b57; color: white; padding: 0.5rem 1.5rem; border-radius: 30px;">🌟 Overall Score: {avg_score:.0f}/100</span></div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f'<div class="metric-card card-green"><div class="metric-value">{school_data["trees"]}<span style="font-size:1rem;"> / {school_data["goal_trees"]}</span></div><div class="metric-label">🌳 Trees on Campus</div></div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div class="metric-card card-blue"><div class="metric-value">{school_data["walk_bike"]}<span style="font-size:1rem;">%</span></div><div class="metric-label">🚶 Walk/Bike to School</div></div>', unsafe_allow_html=True)
    with col3:
        st.markdown(f'<div class="metric-card card-purple"><div class="metric-value">{school_data["recycle"]}<span style="font-size:1rem;">%</span></div><div class="metric-label">♻️ Waste Diverted</div></div>', unsafe_allow_html=True)
    with col4:
        st.markdown(f'<div class="metric-card card-teal"><div class="metric-value">{school_data["bottles"]}</div><div class="metric-label">💧 Bottles Saved/Week</div></div>', unsafe_allow_html=True)
    
    st.markdown('<div class="section-header">⚠️ Areas Needing Attention</div>', unsafe_allow_html=True)
    col5, col6, col7 = st.columns(3)
    with col5:
        st.markdown(f'<div class="metric-card card-red"><div class="metric-value">{school_data["car_alone"]}</div><div class="metric-label">🚗 Solo Cars Daily</div></div>', unsafe_allow_html=True)
    with col6:
        st.markdown(f'<div class="metric-card card-orange"><div class="metric-value">{school_data["food_waste"]}<span style="font-size:1rem;"> lbs</span></div><div class="metric-label">🍎 Food Wasted Daily</div></div>', unsafe_allow_html=True)
    with col7:
        st.markdown(f'<div class="metric-card" style="background: linear-gradient(135deg, #4b5563 0%, #9ca3af 100%); color: white;"><div class="metric-value">{school_data["paper_reams"]}<span style="font-size:1rem;"> reams</span></div><div class="metric-label">📄 Paper/Week</div></div>', unsafe_allow_html=True)

# ===== LEADERBOARD PAGE =====
elif st.session_state.page == "Leaderboard":
    st.markdown('<div class="section-header">🏆 Green Classroom Leaderboard</div>', unsafe_allow_html=True)
    leaderboard = sorted([{"room": room, "score": data['score'], "lights": data['lights']} for room, data in school_data['classrooms'].items()], key=lambda x: x['score'], reverse=True)
    for i, item in enumerate(leaderboard):
        medal = "🥇" if i == 0 else "🥈" if i == 1 else "🥉" if i == 2 else f"{i+1}."
        lights_status = "✅ Lights Off" if item['lights'] else "❌ Lights Left On"
        st.markdown(f'<div class="leaderboard-item"><span><b>{medal}</b></span><span><b>{item["room"]}</b></span><span><b style="color: #2e8b57;">{item["score"]} points</b></span><span>{lights_status}</span></div>', unsafe_allow_html=True)

# ===== ACTION PLAN PAGE =====
elif st.session_state.page == "Action Plan":
    st.markdown('<div class="section-header">📋 Custom Action Plan</div>', unsafe_allow_html=True)
    
    if st.session_state.dark_mode:
        bg1, bg2, bg3, text_color = "#2d1a1a", "#2d2a1a", "#1a2d1a", "white"
    else:
        bg1, bg2, bg3, text_color = "#fef2f2", "#fffbeb", "#ecfdf5", "#1a202c"
    
    st.markdown(f'<div style="padding: 1rem; margin: 1rem 0; border-radius: 16px; border-left: 4px solid #dc2626; background: {bg1}; color: {text_color};"><strong>🔴 PRIORITY 1: Reduce Solo Car Drop-offs</strong><br>🚗 {school_data["car_alone"]} solo cars daily → Save {school_data["co2_save"]} lbs CO2/week</div>', unsafe_allow_html=True)
    st.markdown(f'<div style="padding: 1rem; margin: 1rem 0; border-radius: 16px; border-left: 4px solid #f59e0b; background: {bg2}; color: {text_color};"><strong>🟠 PRIORITY 2: Stop Wasting Food</strong><br>🍎 {school_data["food_waste"]} lbs wasted daily → Divert {school_data["food_waste"] * 180:,} lbs/year</div>', unsafe_allow_html=True)
    st.markdown(f'<div style="padding: 1rem; margin: 1rem 0; border-radius: 16px; border-left: 4px solid #10b981; background: {bg3}; color: {text_color};"><strong>🟢 PRIORITY 3: Turn Off Lights</strong><br>💡 {school_data["lights_on"]} classrooms leave lights on → Save $50/month</div>', unsafe_allow_html=True)

# # ===== SIMULATOR PAGE =====
elif st.session_state.page == "Simulator":
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
    
    if os.path.exists(data_file):
        history = pd.read_csv(data_file)
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
                st.success("All data cleared!")
                st.rerun()
    
    with st.form("data_form"):
        st.markdown("### 🚗 Transportation")
        col_a, col_b = st.columns(2)
        with col_a:
            walk = st.number_input("Students who walked:", min_value=0, value=145)
            bike = st.number_input("Students who biked:", min_value=0, value=47)
        with col_b:
            car_alone = st.number_input("Students in car alone:", min_value=0, value=50)
        
        st.markdown("### 🗑️ Cafeteria Waste")
        food_waste = st.number_input("Pounds of uneaten food:", min_value=0.0, value=21.0)
        
        st.markdown("### 💡 Energy")
        lights_left = st.number_input("Classrooms that left lights on:", min_value=0, value=3)
        
        date = st.date_input("Date:", datetime.now())
        submitted = st.form_submit_button("💾 Save Data", type="primary")
        
        if submitted:
            new_data = pd.DataFrame([{"date": date, "walk": walk, "bike": bike, "car_alone": car_alone, "food_waste_lbs": food_waste, "lights_left_on": lights_left}])
            if os.path.exists(data_file):
                existing = pd.read_csv(data_file)
                combined = pd.concat([existing, new_data], ignore_index=True)
                combined.to_csv(data_file, index=False)
            else:
                new_data.to_csv(data_file, index=False)
            st.success("Data saved!")
            st.balloons()
    
    # Show saved data history
    if os.path.exists(data_file):
        st.markdown("---")
        st.markdown("### 📊 Data History")
        history = pd.read_csv(data_file)
        st.dataframe(history.sort_values("date", ascending=False), use_container_width=True)
        
        # Download button
        csv = history.to_csv(index=False)
        st.download_button("📥 Download All Data as CSV", data=csv, file_name=f"eco_school_data_{datetime.now().strftime('%Y%m%d')}.csv", mime="text/csv")
        
        # ===== LINE GRAPHS =====
        if len(history) > 1:
            st.markdown("---")
            st.markdown("### 📈 Trends Over Time")
            
            # Convert date to datetime
            history['date'] = pd.to_datetime(history['date'])
            
            # Walk trend chart
            st.markdown("#### 🚶 Walk to School Over Time")
            fig_walk = px.line(history, x='date', y='walk', 
                               title='Students Walking to School',
                               labels={'date': 'Date', 'walk': 'Number of Students'},
                               markers=True)
            fig_walk.update_layout(hovermode='x unified')
            st.plotly_chart(fig_walk, use_container_width=True)
            
            # Food waste trend chart
            st.markdown("#### 🍎 Food Waste Over Time")
            fig_waste = px.line(history, x='date', y='food_waste_lbs', 
                                title='Pounds of Food Waste per Day',
                                labels={'date': 'Date', 'food_waste_lbs': 'Pounds'},
                                markers=True,
                                color_discrete_sequence=['#f59e0b'])
            fig_waste.update_layout(hovermode='x unified')
            st.plotly_chart(fig_waste, use_container_width=True)
            
            # Optional: Car alone trend
            st.markdown("#### 🚗 Solo Cars Over Time")
            fig_cars = px.line(history, x='date', y='car_alone', 
                               title='Students Arriving by Car Alone',
                               labels={'date': 'Date', 'car_alone': 'Number of Students'},
                               markers=True,
                               color_discrete_sequence=['#ef4444'])
            fig_cars.update_layout(hovermode='x unified')
            st.plotly_chart(fig_cars, use_container_width=True)
    else:
        st.info("No data yet. Submit the form above to start tracking!")
# ===== FOOTER =====
st.markdown("""
<div class="footer">
    <strong>🌱 Eco-School Dashboard</strong> · AI-powered · Built for USAII Hackathon 2026
</div>
""", unsafe_allow_html=True)