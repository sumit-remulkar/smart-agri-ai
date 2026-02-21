import streamlit as st
import pandas as pd
import datetime

from core.recommendation import calculate_ai_score
from core.risk_engine import calculate_crop_risk

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="Smart Agriculture AI",
    layout="wide",
    page_icon="🌱"
)

# =========================
# LOAD SOIL DATA
# =========================
@st.cache_data
def load_soil():
    return pd.read_csv("data/maharashtra_soil_full.csv")

soil_df = load_soil()
STATES = soil_df["state"].unique()

def get_districts(state):
    return soil_df[soil_df["state"] == state]["district"].unique()

def get_soil_data(state, district):
    try:
        row = soil_df[
            (soil_df["state"] == state) &
            (soil_df["district"] == district)
        ]
        return {
            "primary": row["primary_soil"].values[0],
            "secondary": row["secondary_soil"].values[0],
            "texture": row["texture"].values[0],
            "drainage": row["drainage"].values[0]
        }
    except:
        return {
            "primary": "Unknown",
            "secondary": "Unknown",
            "texture": "Unknown",
            "drainage": "Unknown"
        }

# =========================
# SIMPLE LOGIC
# =========================
def estimate_profit(crop, farm_size):
    base_profit = 60000
    return base_profit * farm_size

def calculate_suitability(soil, temperature):
    score = 60
    if soil in ["Black Soil", "Alluvial Soil"]:
        score += 20
    if 20 <= temperature <= 32:
        score += 20
    return min(score, 100)

def detect_season():
    month = datetime.datetime.now().month
    if month in [6,7,8,9]:
        return "Kharif"
    elif month in [10,11,12,1]:
        return "Rabi"
    else:
        return "Zaid (Summer)"

# =========================
# SIDEBAR
# =========================
st.sidebar.title("🌱 Smart Agri SaaS")
page = st.sidebar.radio(
    "Navigation",
    ["Dashboard", "Soil Intelligence", "Crop Suitability", "Profit Estimator", "Multi-State Engine"]
)

# =========================
# DASHBOARD
# =========================
if page == "Dashboard":

    st.markdown("## 🌾 Smart Agriculture AI")
    st.markdown("### Farm Analysis Dashboard")
    st.markdown("---")

    state = st.selectbox("Select State", STATES)
    district = st.selectbox("Select District", get_districts(state))

    temperature = st.slider("Temperature (°C)", 10, 45, 30)
    farm_size = st.slider("Farm Size (Acres)", 1, 50, 5)

    if st.button("🚀 Analyze Farm"):

        soil_data = get_soil_data(state, district)
        primary_soil = soil_data["primary"]

        suitability = calculate_suitability(primary_soil, temperature)
        season = detect_season()

        top_crops = calculate_ai_score(primary_soil, suitability)
        best_crop = top_crops[0][0]

        profit = estimate_profit(best_crop, farm_size)

        risk_level, risk_reasons = calculate_crop_risk(
            primary_soil,
            temperature,
            suitability,
            profit
        )

        # =========================
        # AI INSIGHTS
        # =========================
        st.subheader("📊 AI Insights")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.write("🧱 Primary Soil:", soil_data["primary"])
            st.write("Secondary Soil:", soil_data["secondary"])
            st.write("Texture:", soil_data["texture"])
            st.write("Drainage:", soil_data["drainage"])

        with col2:
            st.write("📈 Suitability Score:", f"{suitability}%")
            st.write("Season:", season)

        with col3:
            st.write("💰 Estimated Profit:", f"₹ {profit:,}")
            st.write("Recommended Crop:", best_crop)

        # =========================
        # CROP LIST
        # =========================
        st.subheader("🌾 AI Recommended Crops")

        for crop, score in top_crops:
            st.write(f"{crop} – Confidence: {score}%")

        # =========================
        # ANALYTICS CHART
        # =========================
        st.subheader("📊 Crop Confidence Analytics")

        chart_df = pd.DataFrame({
            "Crop": [c for c, _ in top_crops],
            "Confidence": [s for _, s in top_crops]
        })

        st.bar_chart(chart_df.set_index("Crop"))

        # =========================
        # RISK ALERT
        # =========================
        st.subheader("⚠ Crop Risk Alert")

        st.write("Risk Level:", risk_level)

        if risk_reasons:
            st.write("Reasons:")
            for r in risk_reasons:
                st.write("-", r)
        else:
            st.write("No major risk detected ✅")

        # =========================
        # DOWNLOAD REPORT
        # =========================
        report = f"""
SMART AGRICULTURE AI - FARM REPORT
----------------------------------

State: {state}
District: {district}

Soil Details:
Primary Soil: {soil_data['primary']}
Secondary Soil: {soil_data['secondary']}
Texture: {soil_data['texture']}
Drainage: {soil_data['drainage']}

Temperature: {temperature}°C
Season: {season}

Suitability Score: {suitability}%

Recommended Crop: {best_crop}
Estimated Profit: ₹{profit:,}

Risk Level: {risk_level}
"""

        if risk_reasons:
            report += "\nRisk Reasons:\n"
            for r in risk_reasons:
                report += f"- {r}\n"
        else:
            report += "\nNo major risk detected.\n"

        st.download_button(
            label="📥 Download Farm Report",
            data=report,
            file_name=f"{district}_farm_report.txt",
            mime="text/plain"
        )

# =========================
# OTHER PAGES
# =========================
elif page == "Soil Intelligence":
    st.header("🧱 Soil Intelligence Module")

elif page == "Crop Suitability":
    st.header("📈 Crop Suitability Engine")

elif page == "Profit Estimator":
    st.header("💰 Profit Estimation Engine")

elif page == "Multi-State Engine":
    st.header("🌍 Multi-State Scaling Engine")