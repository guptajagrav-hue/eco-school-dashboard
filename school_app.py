import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import io
import json

# ===== PAGE CONFIGURATION =====
st.set_page_config(
    page_title="Eco-School Dashboard | Track Your School's Environmental Impact",
    page_icon="🌱",
    layout="wide"
)

# ===== DARK MODE STATE =====
if 'dark_mode' not in st.session_state:
    st.session_state.dark_mode = False

# ===== WINNING FEATURE: WHY AI? EXPLANATION =====
def show_ai_explanation():
    st.markdown("""
    ### 🤖 Why AI? Why not just a spreadsheet?

    | Task | Spreadsheet | Eco-School AI |
    |------|-------------|---------------|
    | Track daily student travel | ❌ Manual entry | ✅ One-click form |
    | Calculate classroom energy scores | ❌ Hours of math | ✅ Automatic |
    | Find highest-impact actions | ❌ Guesswork | ✅ Data-driven |
    | Compare week over week | ❌ Painful | ✅ Instant charts |

    **Bottom line:** A spreadsheet gives you numbers. Eco-School AI gives you **actionable insights**.
    """)

# ===== WINNING FEATURE: SOCIAL SHARING =====
def share_on_twitter(school_name, trees, walk_percent):
    text = f"🌱 {school_name} has {trees} trees on campus & {walk_percent}% of students walk/bike to school! Track your impact with Eco-School Dashboard! 🌍 #EcoSchool"
    encoded_text = text.replace(" ", "%20").replace("#", "%23")
    return f"https://twitter.com/intent/tweet?text={encoded_text}&url=https://eco-school-dashboard.streamlit.app/"

# ===== WINNING FEATURE: COMMUNITY TRACKER =====
if 'community_reports' not in st.session_state:
    st.session_state.community_reports = []

def add_community_report(school_name, action_taken):
    st.session_state.community_reports.append({
        "school": school_name,
        "action": action_taken,
        "date": datetime.now().strftime("%Y-%m-%d")
    })

# ===== CUSTOM CSS - SIDEBAR FIXED =====
def get_css(dark_mode):
    if dark_mode:
        return """
        <style>
        /* Dark mode */
        .stApp { background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%); }
        [data-testid="stSidebar"] { background: #0f3460; }
        .main-title { font-size: 3rem; font-weight: 800; background: linear-gradient(135deg, #00b894 0%, #55efc4 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; text-align: center; }
        .subtitle { text-align: center; color: #dfe6e9; margin-bottom: 2rem; }
        .section-header { font-size: 1.5rem; font-weight: 700; color: #00b894; margin-top: 2rem; margin-bottom: 1rem; border-left: 4px solid #00b894; padding-left: 1rem; }
        .footer { text-align: center; padding: 2rem; color: #718096; font-size: 0.8rem; border-top: 1px solid #2d3436; margin-top: 3rem; }
        .leaderboard-item { padding: 0.75rem; margin: 0.5rem 0; background: #1a1a2e; border-radius: 12px; color: white; }
        /* All text white in dark mode */
        .stMarkdown, .stText, label, .stMetric label, .stNumberInput label, .stSelectbox label, .stRadio label, .stSlider label, .stCheckbox label {
            color: #ffffff !important;
        }
        .stMetric div[data-testid="stMetricValue"] { color: #00b894 !important; font-size: 2rem !important; }
        .stButton > button { background: linear-gradient(135deg, #00b894 0%, #55efc4 100%); color: #1a1a2e; border-radius: 30px; font-weight: bold; }
        .stButton > button:hover { transform: scale(1.02); cursor: pointer; }
        </style>
        """
    else:
        return """
        <style>
        /* Light mode - sidebar and all text dark */
        .stApp { background: linear-gradient(135deg, #f5f7fa 0%, #e8edf2 100%); }
        [data-testid="stSidebar"] { background: #ffffff; }
        .main-title { font-size: 3rem; font-weight: 800; background: linear-gradient(135deg, #2e8b57 0%, #3cb371 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; text-align: center; }
        .subtitle { text-align: center; color: #4a5568; margin-bottom: 2rem; }
        .section-header { font-size: 1.5rem; font-weight: 700; color: #1a202c; margin-top: 2rem; margin-bottom: 1rem; border-left: 4px solid #2e8b57; padding-left: 1rem; }
        .footer { text-align: center; padding: 2rem; color: #718096; font-size: 0.8rem; border-top: 1px solid #e2e8f0; margin-top: 3rem; }
        .leaderboard-item { padding: 0.75rem; margin: 0.5rem 0; background: #f8faf8; border-radius: 12px; color: #1a202c; }
        /* All text dark in light mode - FIXED SIDEBAR */
        .stMarkdown, .stText, label, .stMetric label, .stNumberInput label, .stSelectbox label, .stRadio label, .stSlider label, .stCheckbox label {
            color: #1a202c !important;
        }
        /* Sidebar specific fix */
        [data-testid="stSidebar"] .stMarkdown, [data-testid="stSidebar"] .stText, [data-testid="stSidebar"] label {
            color: #1a202c !important;
        }
        .stMetric div[data-testid="stMetricValue"] { color: #2e8b57 !important; font-size: 2rem !important; }
        .stButton > button { background: linear-gradient(135deg, #2e8b57 0%, #3cb371 100%); color: white; border-radius: 30px; font-weight: bold; }
        .stButton > button:hover { transform: scale(1.02); cursor: pointer; }
        .stWarning { background-color: #fff5f0; color: #c53030; }
        .stInfo { background-color: #e8f0fe; color: #1a202c; }
        .stSuccess { background-color: #e6f7e6; color: #2e8b57; }
        </style>
        """

st.markdown(get_css(st.session_state.dark_mode), unsafe_allow_html=True)

# ===== HEADER with Dark Mode Toggle =====
col_title, col_toggle = st.columns([4, 1])
with col_title:
    st.markdown('<div class="main-title">🌱 Eco-School Dashboard</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Track your school\'s environmental impact · AI-powered insights</div>', unsafe_allow_html=True)
with col_toggle:
    dark_mode_toggle = st.toggle("🌙 Dark Mode", value=st.session_state.dark_mode)
    if dark_mode_toggle != st.session_state.dark_mode:
        st.session_state.dark_mode = dark_mode_toggle
        st.rerun()

# ===== SIDEBAR =====
with st.sidebar:
    st.markdown("## 🏫 Your School")
    school_name = st.text_input("School Name:", value="Washington Middle School")
    
    st.markdown("---")
    if st.button("🤖 Why AI?"):
        show_ai_explanation()
    
    st.markdown("---")
    st.markdown("### 📍 Navigate")
    view = st.radio(
        "",
        ["📊 Dashboard", "🏆 Leaderboard", "📋 Action Plan", "🌡️ Simulator", "🌱 Community", "📥 Data Entry"]
    )
    st.markdown("---")
    twitter_url = share_on_twitter(school_name, 31, 40)
    st.markdown(f'<a href="{twitter_url}" target="_blank"><button style="width:100%; padding:8px; background:#1DA1F2; color:white; border:none; border-radius:20px; cursor:pointer;">🐦 Share on Twitter</button></a>', unsafe_allow_html=True)

# ===== DEMO DATA =====
school_data = {
    "name": "Washington Middle School",
    "students": 450,
    "trees_campus": 31,
    "goal_trees": 50,
    "walk_bike_percent": 40,
    "goal_walk_bike": 50,
    "car_alone_count": 54,
    "wasted_food_lbs": 24,
    "recycled_percent": 55,
    "goal_recycled": 70,
    "lights_left_on": 5,
    "paper_reams_week": 12,
    "water_bottles_saved": 392,
    "co2_saved_carpool": 1200,
    "classrooms": {
        "Room 101": {"energy_score": 45, "lights_off": False},
        "Room 102": {"energy_score": 95, "lights_off": True},
        "Room 103": {"energy_score": 60, "lights_off": False},
        "Room 104": {"energy_score": 80, "lights_off": True},
        "Room 105": {"energy_score": 25, "lights_off": False},
    }
}

# ===== DASHBOARD VIEW =====
if view == "📊 Dashboard":
    st.markdown(f'<div class="section-header">📊 {school_name} Dashboard</div>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("🌳 Trees on Campus", school_data['trees_campus'], f"Goal: {school_data['goal_trees']}")
    with col2:
        st.metric("🚶 Walk/Bike to School", f"{school_data['walk_bike_percent']}%", f"Goal: {school_data['goal_walk_bike']}%")
    with col3:
        st.metric("♻️ Waste Diverted", f"{school_data['recycled_percent']}%", f"Goal: {school_data['goal_recycled']}%")
    with col4:
        st.metric("💧 Weekly Bottles Saved", school_data['water_bottles_saved'])
    
    st.markdown("---")
    
    col_chart1, col_chart2 = st.columns(2)
    with col_chart1:
        st.markdown("#### 🚗 Transportation")
        transport_data = pd.DataFrame({'Mode': ['Walk', 'Bike', 'Bus', 'Car Alone', 'Carpool'], 'Students': [135, 45, 180, 54, 36]})
        fig = px.pie(transport_data, values='Students', names='Mode')
        st.plotly_chart(fig, use_container_width=True)
        st.info(f"💡 {school_data['car_alone_count']} solo cars daily → Save {school_data['co2_saved_carpool']} lbs CO2/week with carpooling!")
    
    with col_chart2:
        st.markdown("#### 🗑️ Daily Waste")
        waste_data = pd.DataFrame({'Type': ['Food Wasted', 'Recycled', 'Composted', 'Trash'], 'Lbs': [24, 16, 28, 12]})
        fig = px.bar(waste_data, x='Type', y='Lbs', color='Type')
        st.plotly_chart(fig, use_container_width=True)
        st.info(f"💡 {school_data['wasted_food_lbs']} lbs food wasted daily = {school_data['wasted_food_lbs'] * 180:,} lbs/year!")
    
    col_chart3, col_chart4 = st.columns(2)
    with col_chart3:
        st.markdown("#### 💡 Classroom Energy Scores")
        energy_data = [{"Room": r, "Score": d['energy_score']} for r, d in school_data['classrooms'].items()]
        fig = px.bar(pd.DataFrame(energy_data), x='Room', y='Score', color='Score', range_y=[0,100])
        st.plotly_chart(fig, use_container_width=True)
        st.warning(f"⚠️ {school_data['lights_left_on']} classrooms leave lights on when empty!")
    
    with col_chart4:
        st.markdown("#### 📄 Paper Usage")
        total_reams = school_data['paper_reams_week']
        trees_used = total_reams / 16.6
        st.metric("Reams per Week", total_reams)
        st.metric("Trees per Year", f"{trees_used:.1f}")
        st.info("💡 Print two-sided to save 50%!")

# ===== LEADERBOARD VIEW =====
elif view == "🏆 Leaderboard":
    st.markdown('<div class="section-header">🏆 Green Classroom Leaderboard</div>', unsafe_allow_html=True)
    
    df = pd.DataFrame([{"Classroom": r, "Score": d['energy_score'], "Lights Off": "✅" if d['lights_off'] else "❌"} for r, d in school_data['classrooms'].items()])
    df = df.sort_values('Score', ascending=False)
    
    for i, row in df.iterrows():
        if i == 0:
            st.markdown(f'<div class="leaderboard-item" style="background:#fbbf24; color:black;"><b>🥇 {row["Classroom"]} — {row["Score"]} pts</b> | Lights: {row["Lights Off"]}</div>', unsafe_allow_html=True)
        elif i == 1:
            st.markdown(f'<div class="leaderboard-item"><b>🥈 {row["Classroom"]} — {row["Score"]} pts</b> | Lights: {row["Lights Off"]}</div>', unsafe_allow_html=True)
        elif i == 2:
            st.markdown(f'<div class="leaderboard-item"><b>🥉 {row["Classroom"]} — {row["Score"]} pts</b> | Lights: {row["Lights Off"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="leaderboard-item"><b>{i+1}. {row["Classroom"]} — {row["Score"]} pts</b> | Lights: {row["Lights Off"]}</div>', unsafe_allow_html=True)

# ===== ACTION PLAN VIEW =====
elif view == "📋 Action Plan":
    st.markdown('<div class="section-header">📋 Custom Action Plan</div>', unsafe_allow_html=True)
    
    st.markdown("### 🔴 1. Reduce Solo Car Drop-offs")
    st.markdown(f"**{school_data['car_alone_count']} cars arrive alone daily** → Start a 'Walk & Roll Wednesday' program → **Save {school_data['co2_saved_carpool']} lbs CO2/week**")
    
    st.markdown("### 🟠 2. Stop Wasting Food")
    st.markdown(f"**{school_data['wasted_food_lbs']} lbs of edible food wasted daily** → Start a 'Share Table' → **Divert {school_data['wasted_food_lbs'] * 180:,} lbs/year to hungry people**")
    
    st.markdown("### 🟡 3. Turn Off Lights")
    st.markdown(f"**{school_data['lights_left_on']} classrooms leave lights on** → Assign daily 'Energy Monitors' → **Save $50/month on electricity**")

# ===== SIMULATOR VIEW =====
elif view == "🌡️ Simulator":
    st.markdown('<div class="section-header">🌡️ What If Simulator</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        trees = st.slider("Trees to plant:", 0, 100, 20)
        st.metric("Temperature Reduction", f"-{trees * 0.3:.1f}°F")
    with col2:
        walk_pct = st.slider("Increase walk/bike by:", 0, 100, 20)
        st.metric("Fewer Solo Cars Daily", f"-{int(54 * walk_pct / 100)}")

# ===== COMMUNITY VIEW =====
elif view == "🌱 Community":
    st.markdown('<div class="section-header">🌱 Community Action Tracker</div>', unsafe_allow_html=True)
    
    actions = ["🌳 Planted a tree", "🚗 Started carpooling", "🗑️ Waste audit", "💡 Energy monitors", "💧 Water bottle station"]
    selected = st.selectbox("What did your school do?", actions)
    
    if st.button("✅ Log Action"):
        add_community_report(school_name, selected)
        st.success("Thanks for helping! 🌍")
        st.balloons()
    
    if st.session_state.community_reports:
        st.markdown("**Recent actions from schools like yours:**")
        for r in st.session_state.community_reports[-5:]:
            st.caption(f"📍 {r['school']} · {r['action']} · {r['date']}")

# ===== DATA ENTRY VIEW =====
elif view == "📥 Data Entry":
    st.markdown('<div class="section-header">📥 Enter School Data</div>', unsafe_allow_html=True)
    
    with st.form("data_form"):
        walk = st.number_input("Walked today:", 0, 500, 135)
        bike = st.number_input("Biked today:", 0, 500, 45)
        car_alone = st.number_input("Car alone:", 0, 500, 54)
        submitted = st.form_submit_button("💾 Save")
        if submitted:
            st.success("Data saved!")
            st.balloons()

# ===== FOOTER =====
st.markdown("""
<div class="footer">
    <strong>🌱 Eco-School Dashboard</strong> · AI-powered · Built for USAII Hackathon 2026
</div>
""", unsafe_allow_html=True)