def get_css(dark_mode):
    bg = "#0a0a12" if dark_mode else "#f8fafc"
    card_bg = "rgba(255,255,255,0.04)" if dark_mode else "white"
    text = "#f0f3f8" if dark_mode else "#0a0a12"
    border = "rgba(255,255,255,0.06)" if dark_mode else "rgba(0,0,0,0.04)"
    
    return f"""
    <style>
    .stApp {{ background: {bg}; }}
    .stApp header {{ background: {bg}; backdrop-filter: blur(10px); }}
    h1, h2, h3, h4, .stMarkdown, .stText, label, .stMetric label {{ color: {text} !important; }}
    
    /* SIDEBAR ARROW — VISIBLE GREEN BUTTON */
    [data-testid="stSidebarCollapsedControl"] {{
        background: #2e8b57 !important;
        border-radius: 50% !important;
        padding: 4px !important;
        box-shadow: 0 2px 10px rgba(46,139,87,0.3) !important;
        border: 2px solid #3cb371 !important;
        z-index: 1000 !important;
    }}
    [data-testid="stSidebarCollapsedControl"] svg {{
        fill: white !important;
    }}
    [data-testid="stSidebarCollapsedControl"]:hover {{
        background: #3cb371 !important;
        transform: scale(1.05);
        box-shadow: 0 4px 20px rgba(46,139,87,0.5) !important;
    }}
    
    .metric-card {{
        background: {card_bg};
        border: 1px solid {border};
        border-radius: 16px;
        padding: 1.5rem;
        text-align: center;
        transition: all 0.3s ease;
    }}
    .metric-card:hover {{ transform: translateY(-2px); }}
    .metric-card .value {{ font-size: 2.5rem; font-weight: 700; }}
    .metric-card .label {{ font-size: 0.85rem; opacity: 0.7; text-transform: uppercase; letter-spacing: 0.05em; }}
    .metric-card .sub {{ font-size: 0.7rem; opacity: 0.5; margin-top: 0.5rem; }}
    
    .feature-card {{
        background: {card_bg};
        border: 1px solid {border};
        border-radius: 16px;
        padding: 1.5rem;
        transition: all 0.3s ease;
        height: 100%;
    }}
    .feature-card:hover {{ transform: translateY(-4px); }}
    .feature-card .icon {{ font-size: 2rem; margin-bottom: 0.5rem; }}
    .feature-card .title {{ font-weight: 600; font-size: 1.1rem; }}
    .feature-card .desc {{ opacity: 0.6; font-size: 0.9rem; }}
    
    .stButton > button {{
        background: linear-gradient(135deg, #2e8b57, #3cb371) !important;
        color: white !important;
        border: none !important;
        border-radius: 30px !important;
        padding: 0.6rem 1.8rem !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
        width: 100% !important;
    }}
    .stButton > button:hover {{
        transform: scale(1.02);
        box-shadow: 0 8px 30px rgba(46,139,87,0.3);
    }}
    
    .anomaly-card {{
        background: rgba(239,68,68,0.08);
        border: 1px solid rgba(239,68,68,0.15);
        border-radius: 12px;
        padding: 0.75rem 1rem;
        margin: 0.25rem 0;
    }}
    .badge-card {{
        display: inline-block;
        background: rgba(46,139,87,0.15);
        border: 1px solid rgba(46,139,87,0.2);
        border-radius: 30px;
        padding: 0.25rem 0.75rem;
        margin: 0.25rem;
        font-size: 0.8rem;
    }}
    .alert-box {{
        background: rgba(251,146,60,0.1);
        border: 1px solid rgba(251,146,60,0.2);
        border-radius: 12px;
        padding: 1rem;
        margin: 0.5rem 0;
    }}
    [data-testid="stSidebar"] {{
        background: {card_bg};
        border-right: 1px solid {border};
    }}
    [data-testid="stSidebar"] * {{ color: {text} !important; }}
    
    .stTextInput > div > div > input {{
        background: {card_bg} !important;
        color: {text} !important;
        border: 1px solid {border} !important;
        border-radius: 8px !important;
    }}
    
    @media (max-width: 640px) {{
        .metric-card {{ padding: 1rem; }}
        .metric-card .value {{ font-size: 1.8rem; }}
        .feature-card {{ padding: 1rem; }}
        .stButton > button {{ padding: 0.5rem 1rem !important; font-size: 0.9rem; }}
    }}
    </style>
    """