import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import random

# ==========================================
# PAGE CONFIG & STYLES (Instacart Brand)
# ==========================================
st.set_page_config(page_title="Instacart Intelligence | Availability & Subs", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #ffffff; }
    .stMetric {
        background-color: #f3f7f3;
        padding: 15px;
        border-radius: 12px;
        border-left: 5px solid #24be51;
    }
    h1, h2, h3 { color: #24be51; font-family: 'Inter', sans-serif; }
    .status-card {
        padding: 10px;
        border-radius: 8px;
        margin-bottom: 10px;
        border: 1px solid #eee;
    }
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# DATA ENGINE: PRODUCT CATALOG & REAL-TIME FEED
# ==========================================
products_catalog = {
    "Organic Bananas": {"price": 1.99, "category": "Produce", "subs": ["Bananas", "Organic Plantains"]},
    "Whole Milk (1 Gallon)": {"price": 4.50, "category": "Dairy", "subs": ["2% Milk", "Oat Milk (Large)"]},
    "Avocados (Bag of 5)": {"price": 5.99, "category": "Produce", "subs": ["Single Avocados", "Guacamole Mix"]},
    "Organic Baby Spinach": {"price": 3.49, "category": "Produce", "subs": ["Organic Kale", "Spring Mix"]},
    "Greek Yogurt (Vanilla)": {"price": 5.25, "category": "Dairy", "subs": ["Plain Greek Yogurt", "Low-fat Yogurt"]}
}

@st.cache_data
def get_historical_oos_data():
    np.random.seed(42)
    dates = [datetime.now() - timedelta(hours=i) for i in range(48)]
    data = []
    for date in dates:
        for prod in products_catalog.keys():
            # Simulate OOS spikes during busy hours (17:00-19:00)
            base_oos = 0.05
            hour = date.hour
            if 17 <= hour <= 19: base_oos = 0.25
            
            is_found = np.random.choice([1, 0], p=[1-base_oos, base_oos])
            data.append({"Timestamp": date, "Product": prod, "Found": is_found})
    return pd.DataFrame(data)

# ==========================================
# CORE LOGIC: AVAILABILITY SCORER
# ==========================================
def calculate_availability_score(product, history):
    prod_history = history[history['Product'] == product].sort_values('Timestamp', ascending=False)
    # Weighting recent SHOPS more heavily (Decay logic)
    recent_shops = prod_history.head(10)
    if len(recent_shops) == 0: return 1.0
    
    score = recent_shops['Found'].mean()
    return score

# ==========================================
# CORE LOGIC: SMART SUBSTITUTION RANKER
# ==========================================
def rank_substitutions(original_product, score_threshold=0.6):
    subs = products_catalog[original_product]["subs"]
    ranked_subs = []
    
    for sub in subs:
        # Mocking a dynamic availability check for the substitute
        # In real life, this would call `calculate_availability_score` for the sub
        sub_score = random.uniform(0.4, 0.95)
        if sub_score > score_threshold:
            ranked_subs.append({"Substitute": sub, "Confidence": sub_score, "Reason": "High Availability + User Preference Match"})
    
    return sorted(ranked_subs, key=lambda x: x['Confidence'], reverse=True)

# ==========================================
# DASHBOARD UI
# ==========================================
st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/9/9f/Instacart_logo.svg", width=180)
st.sidebar.title("Inventory Intelligence")
st.sidebar.markdown("---")
view_mode = st.sidebar.radio("Module", ["Fulfillment Center", "Substitution Lab", "Predictive Alerts"])

history_df = get_historical_oos_data()

if view_mode == "Fulfillment Center":
    st.title("🛍️ Real-Time Availability Intelligence")
    st.markdown("Predicting shelf inventory using **Shopper Feedback Loops**.")

    # Top Metrics
    col1, col2, col3 = st.columns(3)
    avg_found_rate = history_df['Found'].mean()
    col1.metric("Avg. Found Rate", f"{avg_found_rate:.1%}")
    col2.metric("OOS Risk Items", "12", delta="3 New spikes", delta_color="inverse")
    col3.metric("Shopper Confidence", "94%", help="Based on real-time feedback accuracy")

    # Availability Grid
    st.subheader("Current Shelf Prediction")
    cols = st.columns(len(products_catalog))
    for i, (prod, info) in enumerate(products_catalog.items()):
        score = calculate_availability_score(prod, history_df)
        status_color = "green" if score > 0.8 else "orange" if score > 0.5 else "red"
        cols[i].markdown(f"""
            <div style="text-align:center; padding:10px; border:1px solid #eee; border-radius:10px;">
                <p style="font-size:12px; margin-bottom:0;">{prod}</p>
                <h2 style="color:{status_color}; margin-top:0;">{score:.0%}</h2>
                <p style="font-size:10px; color:#666;">Prob. Available</p>
            </div>
        """, unsafe_allow_html=True)

    # Found Rate Trends
    st.markdown("---")
    st.subheader("Trending: Out-of-Stock (OOS) Spikes")
    trend_data = history_df.groupby('Timestamp')['Found'].mean().reset_index()
    fig = px.line(trend_data, x='Timestamp', y='Found', title="Network Found Rate (48h)", color_discrete_sequence=['#24be51'])
    fig.update_layout(yaxis_title="Found Probability", template="plotly_white")
    st.plotly_chart(fig, use_container_width=True)

elif view_mode == "Substitution Lab":
    st.title("🔄 Bayesian Substitution Engine")
    st.markdown("Automating the backup-item selection to prevent lost sales.")
    
    target_prod = st.selectbox("Select Out-of-Stock Item", list(products_catalog.keys()))
    
    col_a, col_b = st.columns([1, 2])
    
    with col_a:
        st.info(f"**Original Item:** {target_prod}")
        st.write(f"Category: {products_catalog[target_prod]['category']}")
        st.write(f"Price: ${products_catalog[target_prod]['price']}")
    
    with col_b:
        st.subheader("Recommended Replacements")
        recommendations = rank_substitutions(target_prod)
        for rec in recommendations:
            with st.expander(f"⭐ {rec['Substitute']} ({int(rec['Confidence']*100)}% Match)"):
                st.write(f"**Rationale:** {rec['Reason']}")
                st.progress(rec['Confidence'])

elif view_mode == "Predictive Alerts":
    st.title("⚠️ Predictive Inventory Alerts")
    st.warning("The following items are showing high OOS variance at local retailers.")
    
    st.table([
        {"Product": "Organic Bananas", "Risk": "CRITICAL", "Impact": "$1.2k hourly loss", "Prediction": "OOS within 30 mins"},
        {"Product": "Greek Yogurt", "Risk": "MODERATE", "Impact": "$400 hourly loss", "Prediction": "Stock low across 5 stores"},
    ])

# ==========================================
# FOOTER
# ==========================================
st.markdown("---")
st.markdown("<center>Instacart Data Science | Solving Real-Time Fulfillment Variance</center>", unsafe_allow_html=True)
