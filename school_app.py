import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# ===== PAGE CONFIG =====
st.set_page_config(
    page_title="Eco-School Dashboard",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ===== HEADER =====
st.title("🌱 Eco-School Dashboard")
st.caption("Track your school's environmental impact · AI-powered insights")

# ===== SIDEBAR =====
with st.sidebar:
    st.header("🏫 Your School")
    school_name = st.text_input("School Name:", value="Washington Middle School")
    
    st.divider()
    
    if st.button("🤖 Why AI?", use_container_width=True):
        st.info("AI analyzes transportation, waste, and energy data to find the highest-impact actions for YOUR school.")
    
    st.divider()
    
    st.subheader("📍 Navigate")
    view = st.radio("", [
        "📊 Dashboard", 
        "🏆 Leaderboard", 
        "📋 Action Plan", 
        "🌡️ Simulator", 
        "🌱 Community", 
        "📥 Data Entry"
    ], label_visibility="collapsed")
    
    st.divider()
    
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
    st.header(f"📊 {school_name} Dashboard")
    
    # Metrics row
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric("🌳 Trees on Campus", school_data["trees"], f"Goal: {school_data['goal_trees']}")
    with c2:
        st.metric("🚶 Walk/Bike to School", f"{school_data['walk_bike']}%", f"Goal: {school_data['goal_walk_bike']}%")
    with c3:
        st.metric("♻️ Waste Diverted", f"{school_data['recycle']}%", f"Goal: {school_data['goal_recycle']}%")
    with c4:
        st.metric("💧 Bottles Saved/Week", school_data["bottles"])
    
    st.divider()
    
    # Charts row
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🚗 Transportation")
        transport = pd.DataFrame({
            'Mode': ['Walk', 'Bike', 'Bus', 'Car Alone', 'Carpool'],
            'Students': [135, 45, 180, 54, 36]
        })
        fig = px.pie(transport, values='Students', names='Mode', title='How Students Get to School')
        st.plotly_chart(fig, use_container_width=True)
        st.info(f"💡 {school_data['car_alone']} solo cars daily → Save {school_data['co2_save']} lbs CO2/week with carpooling!")
    
    with col2:
        st.subheader("🗑️ Daily Waste")
        waste = pd.DataFrame({
            'Type': ['Food Wasted', 'Recycled', 'Composted', 'Trash'],
            'Pounds': [24, 16, 28, 12]
        })
        fig = px.bar(waste, x='Type', y='Pounds', title='Daily Waste (lbs)', color='Type')
        st.plotly_chart(fig, use_container_width=True)
        st.info(f"💡 {school_data['food_waste']} lbs food wasted daily = {school_data['food_waste'] * 180:,} lbs/year!")
    
    col3, col4 = st.columns(2)
    
    with col3:
        st.subheader("💡 Classroom Energy")
        energy_data = []
        for room, data in school_data['classrooms'].items():
            energy_data.append({"Classroom": room, "Score": data['score']})
        energy_df = pd.DataFrame(energy_data)
        fig = px.bar(energy_df, x='Classroom', y='Score', title='Energy Score (0-100)', color='Score', range_y=[0,100])
        st.plotly_chart(fig, use_container_width=True)
        st.warning(f"⚠️ {school_data['lights_on']} classrooms leave lights on when empty!")
    
    with col4:
        st.subheader("📄 Paper Usage")
        trees_used = school_data['paper_reams'] / 16.6
        st.metric("Reams of Paper per Week", school_data['paper_reams'])
        st.metric("Trees Used per Year", f"{trees_used:.1f}")
        st.info("💡 Print two-sided to save 50% of paper!")

# ===== LEADERBOARD =====
elif view == "🏆 Leaderboard":
    st.header("🏆 Green Classroom Leaderboard")
    
    leaderboard = []
    for room, data in school_data['classrooms'].items():
        leaderboard.append({
            "Classroom": room,
            "Score": data['score'],
            "Lights Off": "✅" if data['lights'] else "❌"
        })
    
    leaderboard = sorted(leaderboard, key=lambda x: x['Score'], reverse=True)
    
    for i, row in enumerate(leaderboard):
        if i == 0:
            st.success(f"🥇 **1st Place: {row['Classroom']} — {row['Score']} points** | Lights: {row['Lights Off']}")
        elif i == 1:
            st.info(f"🥈 **2nd Place: {row['Classroom']} — {row['Score']} points** | Lights: {row['Lights Off']}")
        elif i == 2:
            st.info(f"🥉 **3rd Place: {row['Classroom']} — {row['Score']} points** | Lights: {row['Lights Off']}")
        else:
            st.write(f"**{i+1}. {row['Classroom']} — {row['Score']} points** | Lights: {row['Lights Off']}")

# ===== ACTION PLAN =====
elif view == "📋 Action Plan":
    st.header("📋 Your School's Custom Action Plan")
    
    st.subheader("🔴 PRIORITY 1: Reduce Solo Car Drop-offs")
    st.write(f"**Problem:** {school_data['car_alone']} cars arrive daily with just one student.")
    st.write("**Solution:** Launch a 'Walk & Roll Wednesday' program.")
    st.write(f"**Impact:** Save {school_data['co2_save']} lbs CO2/week.")
    
    st.subheader("🟠 PRIORITY 2: Stop Wasting Edible Food")
    st.write(f"**Problem:** {school_data['food_waste']} lbs of unopened food thrown away daily.")
    st.write("**Solution:** Start a 'Share Table' where students place unwanted unopened food.")
    st.write(f"**Impact:** Divert {school_data['food_waste'] * 180:,} lbs/year to hungry people.")
    
    st.subheader("🟡 PRIORITY 3: Turn Off Lights")
    st.write(f"**Problem:** {school_data['lights_on']} classrooms leave lights on when empty.")
    st.write("**Solution:** Assign daily 'Energy Monitor' student job in each classroom.")
    st.write("**Impact:** Save $50/month on electricity bills.")

# ===== SIMULATOR =====
elif view == "🌡️ Simulator":
    st.header("🌡️ What If Simulator")
    st.caption("See how different actions would change your school's environmental impact")
    
    c1, c2 = st.columns(2)
    
    with c1:
        trees = st.slider("🌳 Trees to plant:", 0, 100, 20)
        temp_reduction = trees * 0.3
        st.metric("Temperature Reduction", f"-{temp_reduction:.1f}°F")
        st.caption("Cooler playground on hot days")
    
    with c2:
        walk_pct = st.slider("🚶 Increase walk/bike by:", 0, 100, 20)
        cars_removed = int(54 * walk_pct / 100)
        st.metric("Fewer Solo Cars Daily", f"-{cars_removed}")
        st.caption(f"{cars_removed * 5} lbs CO2 saved daily")

# ===== COMMUNITY =====
elif view == "🌱 Community":
    st.header("🌱 Community Action Tracker")
    
    actions = [
        "🌳 Planted a tree on campus",
        "🚗 Started a carpool group",
        "🗑️ Organized a waste audit",
        "💡 Created an energy monitor program",
        "💧 Added a water bottle refill station"
    ]
    
    selected = st.selectbox("What did your school do this week?", actions)
    
    if st.button("✅ Log This Action", type="primary"):
        st.success("Thanks for helping your school go green! 🌍")
        st.balloons()
    
    st.divider()
    st.caption("Every action counts. Small changes add up to big impact!")

# ===== DATA ENTRY =====
elif view == "📥 Data Entry":
    st.header("📥 Enter Your School's Data")
    st.caption("Fill out this form daily or weekly to track progress")
    
    with st.form("data_entry"):
        st.subheader("🚗 Transportation (Today)")
        walk = st.number_input("Students who walked:", min_value=0, value=135)
        bike = st.number_input("Students who biked:", min_value=0, value=45)
        car_alone = st.number_input("Students in car alone:", min_value=0, value=54)
        
        st.subheader("🗑️ Cafeteria Waste (Today)")
        food_waste = st.number_input("Pounds of uneaten food:", min_value=0.0, value=24.0)
        
        st.subheader("💡 Energy (Today)")
        lights_left = st.number_input("Classrooms that left lights on:", min_value=0, value=5)
        
        submitted = st.form_submit_button("💾 Save Data", type="primary")
        
        if submitted:
            st.success("✅ Data saved! Track progress week over week.")
            st.balloons()

# ===== FOOTER =====
st.divider()
st.caption("🌱 Eco-School Dashboard · AI-powered · Built for USAII Hackathon 2026")