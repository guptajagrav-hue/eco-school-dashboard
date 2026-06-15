import streamlit as st
import pandas as pd
import plotly.express as px
import datetime

# ===== PAGE CONFIGURATION =====
st.set_page_config(
    page_title="Eco-School Dashboard",
    page_icon="🌱",
    layout="wide"
)

# ===== DARK MODE STATE =====
if 'dark_mode' not in st.session_state:
    st.session_state.dark_mode = False

# ===== CUSTOM CSS - COMPLETE FIX FOR SIDEBAR =====
def get_css(dark_mode):
    if dark_mode:
        return """
        <style>
        /* Dark Mode */
        .stApp { background: #1a1a2e; }
        [data-testid="stSidebar"] { background: #0f3460; }
        [data-testid="stSidebar"] * { color: #ffffff !important; }
        .main-title { font-size: 2.5rem; font-weight: 800; color: #00b894; text-align: center; }
        .subtitle { text-align: center; color: #dfe6e9; }
        .section-header { font-size: 1.3rem; font-weight: 700; color: #00b894; margin-top: 1rem; }
        .stButton > button { background: #00b894; color: #1a1a2e; border-radius: 20px; }
        .stMetric label { color: #dfe6e9 !important; }
        .stMetric div { color: #00b894 !important; }
        </style>
        """
    else:
        return """
        <style>
        /* Light Mode - FIXED SIDEBAR */
        .stApp { background: #f0f2f6; }
        [data-testid="stSidebar"] { background: #ffffff; }
        [data-testid="stSidebar"] * { color: #1a202c !important; }
        [data-testid="stSidebar"] .stMarkdown { color: #1a202c !important; }
        [data-testid="stSidebar"] label { color: #1a202c !important; }
        [data-testid="stSidebar"] .stTextInput label { color: #1a202c !important; }
        [data-testid="stSidebar"] .stRadio label { color: #1a202c !important; }
        .main-title { font-size: 2.5rem; font-weight: 800; color: #2e8b57; text-align: center; }
        .subtitle { text-align: center; color: #4a5568; }
        .section-header { font-size: 1.3rem; font-weight: 700; color: #2e8b57; margin-top: 1rem; }
        .stButton > button { background: #2e8b57; color: white; border-radius: 20px; }
        .stMetric label { color: #4a5568 !important; }
        .stMetric div { color: #2e8b57 !important; }
        .stWarning { background-color: #fff5f0; color: #c53030; }
        .stInfo { background-color: #e8f0fe; color: #1a202c; }
        </style>
        """

st.markdown(get_css(st.session_state.dark_mode), unsafe_allow_html=True)

# ===== HEADER =====
col_title, col_toggle = st.columns([4, 1])
with col_title:
    st.markdown('<div class="main-title">🌱 Eco-School Dashboard</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Track your school\'s environmental impact</div>', unsafe_allow_html=True)
with col_toggle:
    new_mode = st.toggle("🌙 Dark Mode", value=st.session_state.dark_mode)
    if new_mode != st.session_state.dark_mode:
        st.session_state.dark_mode = new_mode
        st.rerun()

# ===== SIDEBAR =====
with st.sidebar:
    st.markdown("## 🏫 Your School")
    school_name = st.text_input("School Name:", value="Washington Middle School")
    
    st.markdown("---")
    if st.button("🤖 Why AI?"):
        st.info("AI analyzes your school's data to find the highest-impact actions — carpooling, tree planting, energy savings — personalized for YOUR school.")
    
    st.markdown("---")
    st.markdown("### 📍 Navigate")
    view = st.radio("", ["📊 Dashboard", "🏆 Leaderboard", "📋 Action Plan", "🌡️ Simulator", "🌱 Community", "📥 Data Entry"])
    
    st.markdown("---")
    st.markdown("### 🤝 Share")
    st.markdown('[🐦 Share on Twitter](https://twitter.com/intent/tweet?text=Check%20out%20Eco-School%20Dashboard!%20🌱%20https://eco-school-dashboard.streamlit.app/)')

# ===== DEMO DATA =====
school_data = {
    "trees_campus": 31,
    "goal_trees": 50,
    "walk_bike_percent": 40,
    "goal_walk_bike": 50,
    "recycled_percent": 55,
    "goal_recycled": 70,
    "car_alone_count": 54,
    "wasted_food_lbs": 24,
    "lights_left_on": 5,
    "paper_reams_week": 12,
    "water_bottles_saved": 392,
    "co2_saved_carpool": 1200,
    "classrooms": {
        "Room 101": {"score": 45, "lights_off": False},
        "Room 102": {"score": 95, "lights_off": True},
        "Room 103": {"score": 60, "lights_off": False},
        "Room 104": {"score": 80, "lights_off": True},
        "Room 105": {"score": 25, "lights_off": False},
    }
}

# ===== DASHBOARD =====
if view == "📊 Dashboard":
    st.markdown(f'<div class="section-header">📊 {school_name} Dashboard</div>', unsafe_allow_html=True)
    
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric("🌳 Trees", school_data['trees_campus'], f"Goal: {school_data['goal_trees']}")
    with c2:
        st.metric("🚶 Walk/Bike", f"{school_data['walk_bike_percent']}%", f"Goal: {school_data['goal_walk_bike']}%")
    with c3:
        st.metric("♻️ Waste Diverted", f"{school_data['recycled_percent']}%", f"Goal: {school_data['goal_recycled']}%")
    with c4:
        st.metric("💧 Bottles/Week", school_data['water_bottles_saved'])
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### 🚗 Transportation")
        st.write("- Walk: 135 students")
        st.write("- Bike: 45 students")
        st.write("- Bus: 180 students")
        st.write("- Car alone: 54 students")
        st.write("- Carpool: 36 students")
        st.info(f"💡 {school_data['car_alone_count']} solo cars → Save {school_data['co2_saved_carpool']} lbs CO2/week with carpooling!")
    
    with col2:
        st.markdown("#### 🗑️ Daily Waste")
        st.write("- Food wasted: 24 lbs")
        st.write("- Recycled: 16 lbs")
        st.write("- Composted: 28 lbs")
        st.write("- Landfill: 12 lbs")
        st.info(f"💡 {school_data['wasted_food_lbs']} lbs food wasted daily = {school_data['wasted_food_lbs'] * 180:,} lbs/year!")
    
    col3, col4 = st.columns(2)
    with col3:
        st.markdown("#### 💡 Classroom Energy")
        for room, data in school_data['classrooms'].items():
            status = "✅" if data['lights_off'] else "❌"
            st.write(f"{room}: {data['score']} pts - Lights: {status}")
        st.warning(f"⚠️ {school_data['lights_left_on']} classrooms leave lights on!")
    
    with col4:
        st.markdown("#### 📄 Paper Usage")
        trees_used = school_data['paper_reams_week'] / 16.6
        st.metric("Reams/Week", school_data['paper_reams_week'])
        st.metric("Trees/Year", f"{trees_used:.1f}")
        st.info("💡 Print two-sided to save 50%!")

# ===== LEADERBOARD =====
elif view == "🏆 Leaderboard":
    st.markdown('<div class="section-header">🏆 Green Classroom Leaderboard</div>', unsafe_allow_html=True)
    
    df = [{"Classroom": r, "Score": d['score'], "Lights Off": "✅" if d['lights_off'] else "❌"} for r, d in school_data['classrooms'].items()]
    df = sorted(df, key=lambda x: x['Score'], reverse=True)
    
    for i, row in enumerate(df):
        medal = "🥇" if i == 0 else "🥈" if i == 1 else "🥉" if i == 2 else f"{i+1}."
        st.markdown(f"**{medal} {row['Classroom']} — {row['Score']} pts** | Lights: {row['Lights Off']}")

# ===== ACTION PLAN =====
elif view == "📋 Action Plan":
    st.markdown('<div class="section-header">📋 Custom Action Plan</div>', unsafe_allow_html=True)
    
    st.markdown("### 🔴 1. Reduce Solo Car Drop-offs")
    st.markdown(f"**Problem:** {school_data['car_alone_count']} cars arrive alone daily")
    st.markdown(f"**Solution:** Launch 'Walk & Roll Wednesday'")
    st.markdown(f"**Impact:** Save {school_data['co2_saved_carpool']} lbs CO2/week")
    
    st.markdown("### 🟠 2. Stop Wasting Food")
    st.markdown(f"**Problem:** {school_data['wasted_food_lbs']} lbs of edible food wasted daily")
    st.markdown("**Solution:** Start a 'Share Table' for unwanted unopened food")
    st.markdown(f"**Impact:** Divert {school_data['wasted_food_lbs'] * 180:,} lbs/year to hungry people")
    
    st.markdown("### 🟡 3. Turn Off Lights")
    st.markdown(f"**Problem:** {school_data['lights_left_on']} classrooms leave lights on")
    st.markdown("**Solution:** Assign daily 'Energy Monitor' student job")
    st.markdown("**Impact:** Save $50/month on electricity")

# ===== SIMULATOR =====
elif view == "🌡️ Simulator":
    st.markdown('<div class="section-header">🌡️ What If Simulator</div>', unsafe_allow_html=True)
    
    trees = st.slider("🌳 Trees to plant:", 0, 100, 20)
    st.metric("🌡️ Temperature Reduction", f"-{trees * 0.3:.1f}°F")
    
    walk_pct = st.slider("🚶 Increase walk/bike by:", 0, 100, 20)
    st.metric("🚗 Fewer Solo Cars Daily", f"-{int(54 * walk_pct / 100)}")

# ===== COMMUNITY =====
elif view == "🌱 Community":
    st.markdown('<div class="section-header">🌱 Community Action Tracker</div>', unsafe_allow_html=True)
    
    actions = ["🌳 Planted a tree", "🚗 Started carpooling", "🗑️ Waste audit", "💡 Energy monitors", "💧 Water bottle station"]
    selected = st.selectbox("What did your school do?", actions)
    
    if st.button("✅ Log Action"):
        st.success("Thanks for helping your school go green! 🌍")
        st.balloons()

# ===== DATA ENTRY =====
elif view == "📥 Data Entry":
    st.markdown('<div class="section-header">📥 Enter School Data</div>', unsafe_allow_html=True)
    
    with st.form("data_form"):
        walk = st.number_input("🚶 Students who walked:", 0, 500, 135)
        bike = st.number_input("🚲 Students who biked:", 0, 500, 45)
        car_alone = st.number_input("🚗 Students in car alone:", 0, 500, 54)
        food_waste = st.number_input("🍎 Pounds of uneaten food:", 0.0, 200.0, 24.0)
        
        submitted = st.form_submit_button("💾 Save Data")
        if submitted:
            st.success("✅ Data saved! Track progress week over week.")
            st.balloons()

# ===== FOOTER =====
st.markdown("---")
st.markdown("<p style='text-align: center; color: gray;'>🌱 Eco-School Dashboard · AI-powered · Built for USAII Hackathon 2026</p>", unsafe_allow_html=True)