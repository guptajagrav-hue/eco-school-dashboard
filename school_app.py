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

/* Hexagon chart container */
.hexagon-container {
    background: white;
    border-radius: 24px;
    padding: 1.5rem;
    box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    text-align: center;
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

# Calculate environmental profile scores (0-100)
# These are normalized scores for the hexagon chart
environmental_profile = {
    "🌳 Tree Canopy": min(100, (school_data["trees"] / school_data["goal_trees"]) * 100),
    "🚶 Active Transport": min(100, (school_data["walk_bike"] / school_data["goal_walk_bike"]) * 100),
    "♻️ Waste Diversion": min(100, (school_data["recycle"] / school_data["goal_recycle"]) * 100),
    "💡 Energy Efficiency": min(100, 100 - (school_data["lights_on"] * 5)),
    "📄 Paper Reduction": min(100, 100 - ((school_data["paper_reams"] - 8) / 8 * 100) if school_data["paper_reams"] > 8 else 100),
    "💧 Water Conservation": min(100, (school_data["bottles"] / 500) * 100 if school_data["bottles"] < 500 else 100),
}

# ===== FUNCTION TO CREATE HEXAGONAL RADAR CHART =====
def create_hexagon_chart(scores, title="Environmental Profile"):
    """Create a hexagonal radar/spider chart"""
    
    categories = list(scores.keys())
    values = list(scores.values())
    
    # Close the polygon by repeating the first value
    categories_closed = categories + [categories[0]]
    values_closed = values + [values[0]]
    
    # Create radar chart
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
    
    # Add ideal reference line (100%)
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
            font=dict(size=18, weight='bold', color='#2d3748'),
            x=0.5
        ),
        showlegend=True,
        legend=dict(
            x=0.9,
            y=1.1,
            orientation='h',
            bgcolor='rgba(255,255,255,0.8)'
        ),
        height=500,
        width=600,
        margin=dict(l=80, r=80, t=80, b=80)
    )
    
    # Add annotation for overall score
    avg_score = sum(values) / len(values)
    fig.add_annotation(
        x=0.5,
        y=-0.15,
        xref="paper",
        yref="paper",
        text=f"Overall Environmental Score: {avg_score:.0f}/100",
        showarrow=False,
        font=dict(size=14, weight='bold', color='#2e8b57'),
        bgcolor='rgba(255,255,255,0.9)',
        bordercolor='#2e8b57',
        borderwidth=1,
        borderpad=8,
        borderradius=8
    )
    
    return fig

# ===== DASHBOARD =====
if view == "📊 Dashboard":
    st.markdown(f'<div class="section-header">📊 {school_name} Dashboard</div>', unsafe_allow_html=True)
    
    # Row 1: Environmental Profile Hexagon Chart (NEW!)
    st.markdown('<div class="hexagon-container">', unsafe_allow_html=True)
    st.markdown('<h3 style="text-align: center; margin-bottom: 1rem;">🌿 Environmental Profile</h3>', unsafe_allow_html=True)
    
    # Create and display the hexagon chart
    hex_fig = create_hexagon_chart(environmental_profile, f"{school_name} - 6 Pillars of Sustainability")
    st.plotly_chart(hex_fig, use_container_width=True)
    
    # Add explanation of the chart
    st.caption("📊 This hexagonal chart shows your school's performance across 6 key environmental categories. The green area is your school; the gray dashed line is the 100% goal. The closer you are to the outer edge, the better!")
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Row 2: Main metrics
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
    
    # Row 3: Problem cards
    st.markdown('<div class="section-header">⚠️ Areas Needing Attention</div>', unsafe_allow_html=True)
    
    col5, col6, col7 = st.columns(3)
    
    with col5:
        st.markdown(f'''
        <div class="metric-card card-red">
            <div class="metric-value">{school_data["car_alone"]}</div>
            <div class="metric-label">🚗 Solo Cars Daily</div>
            <div class="metric-sub">Save {school_data["co2_save"]} lbs CO2/week</div>
        </div>
        ''', unsafe_allow_html=True)
    
    with col6:
        st.markdown(f'''
        <div class="metric-card card-orange">
            <div class="metric-value">{school_data["food_waste"]}<span style="font-size:1rem;"> lbs</span></div>
            <div class="metric-label">🍎 Food Wasted Daily</div>
            <div class="metric-sub">{school_data["food_waste"] * 180:,} lbs/year</div>
        </div>
        ''', unsafe_allow_html=True)
    
    with col7:
        st.markdown(f'''
        <div class="metric-card" style="background: linear-gradient(135deg, #4b5563 0%, #9ca3af 100%); color: white;">
            <div class="metric-value">{school_data["paper_reams"]}<span style="font-size:1rem;"> reams/week</span></div>
            <div class="metric-label">📄 Paper Usage</div>
            <div class="metric-sub">{school_data["paper_reams"] / 16.6:.1f} trees/year</div>
        </div>
        ''', unsafe_allow_html=True)
    
    # Row 4: Classroom energy
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
    
    # Detailed breakdown of hexagon scores
    with st.expander("📊 View Detailed Environmental Profile Breakdown"):
        st.markdown("### Category Scores (0-100)")
        for category, score in environmental_profile.items():
            st.markdown(f"**{category}:** {score:.0f}/100")
            st.progress(int(score))
        st.caption("These 6 scores are combined to create the hexagonal environmental profile chart above.")

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
                <div style="font-size: 1.3rem; font-weight: 700;">{medal}</div>
                <div style="font-weight: 600;">{item['room']}</div>
                <div style="font-weight: 800; color: #2e8b57;">{item['score']} points</div>
                <div style="font-size: 0.8rem;">{lights_status}</div>
            </div>
        </div>
        ''', unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("### 📋 Weekly Challenge Checklist")
    col_check1, col_check2 = st.columns(2)
    with col_check1:
        st.checkbox("☐ Turn off lights when leaving (10 points/day)")
        st.checkbox("☐ Shut down computers at end of day (10 points/day)")
    with col_check2:
        st.checkbox("☐ Sort waste correctly (20 points/day)")
        st.checkbox("☐ Walk, bike, or carpool to school (15 points/day)")

# ===== ACTION PLAN =====
elif view == "📋 Action Plan":
    st.markdown('<div class="section-header">📋 Your School\'s Custom Action Plan</div>', unsafe_allow_html=True)
    
    # Show the hexagon chart with lowest scores highlighted
    st.markdown("### Based on Your Environmental Profile:")
    low_scores = [(cat, score) for cat, score in environmental_profile.items() if score < 60]
    if low_scores:
        st.warning(f"⚠️ Priority areas: {', '.join([cat for cat, _ in low_scores])}")
    
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
    st.markdown('<div class="metric-card" style="background: linear-gradient(135deg, #4b5563 0%, #9ca3af 100%); color: white; text-align: center;">', unsafe_allow_html=True)
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
    <strong>🌱 Eco-School Dashboard</strong> · AI-powered · Environmental Profile Hexagon · Built for USAII Hackathon 2026
</div>
""", unsafe_allow_html=True)