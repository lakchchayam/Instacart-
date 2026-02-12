# Instacart Fulfillment Intelligence Platform

A specialized data science platform focused on solving Instacart's real-world "Item Availability" and "Substitution" challenges.

## 🚀 Overview
Instacart operates in a dynamic environment where store inventory is never static. This platform uses **Shopper Feedback Loops** to predict real-time shelf availability and recommends optimal substitutions using **Bayesian Ranking**.

### Key Modules
- **Backend (Streamlit/Python):** 
  - `AvailabilityScorer`: Calculates real-time found rates.
  - `SubstitutionRanker`: Optimizes backup item selection.
- **Frontend (HTML/CSS/JS):** 
  - A premium, light-mode dashboard for retail partners to monitor marketplace health.

## 🧪 Research Basis
This implementation is inspired by the research focus of **Dr. Muhammad Iftekher Chowdhury** (Instacart Engineering Manager) on TCN-Transformer forecasting and modeling dependencies in retail order data.

## 🛠️ Tech Stack
- **Languages:** Python, JavaScript, HTML, CSS
- **Libraries:** Streamlit, Pandas, Plotly, Chart.js, Lucide Icons
- **ML Methodology:** Bayesian Ranking, Weighted Average Decay Models

## 🏃 Run the Platform
1. **Backend:**
   ```bash
   cd backend
   pip install -r requirements.txt
   streamlit run app.py
   ```
2. **Frontend:**
   Open `frontend/index.html` in any modern browser.
