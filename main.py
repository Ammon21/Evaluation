import streamlit as st
import evaluation_dashboard
import teacher_ranking
import radarv6

# Set page title and favicon
st.set_page_config(page_title="Teachers Dashboard", page_icon="📊", layout="wide")

# Custom CSS to make sidebar fancy
st.markdown("""
    <style>
        [data-testid="stSidebar"] {
            background: linear-gradient(to bottom, #3498db, #85c1e9);
            color: white;
            padding: 20px;
            border-right: 4px solid #2980b9;
        }
        [data-testid="stSidebar"] h3 {
            color: #fff;
            font-size: 22px;
            font-weight: bold;
            margin-bottom: 10px;
            text-transform: uppercase;
        }
        [data-testid="stSidebar"] .stRadio {
            background-color: #85c1e9;
            border: 2px solid white;
            border-radius: 8px;
            padding: 8px;
        }
        [data-testid="stSidebar"] .stRadio label {
            color: white;
            font-weight: bold;
        }
    </style>
""", unsafe_allow_html=True)

# Sidebar - Logo and Page Selector
with st.sidebar:
    st.image("logo.png", width=120)
    st.markdown("<h3>Dashboard Options</h3>", unsafe_allow_html=True)
    
    page = st.radio(
        "Choose Page:",
        ["Teacher Evaluation Dashboard", "Teacher Ranking Dashboard", "Teacher Profile Radar"]
    )

# Display Selected Page
if page == "Teacher Evaluation Dashboard":
    evaluation_dashboard.show_evaluation_dashboard()
elif page == "Teacher Ranking Dashboard":
    teacher_ranking.show_teacher_ranking()
elif page == "Teacher Profile Radar":
    radarv6.radar_dashboard()
