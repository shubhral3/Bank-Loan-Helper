import streamlit as st
import requests
import json

# Define the backend URL
API_URL = "http://127.0.0.1:8000/score_loan"

st.set_page_config(page_title="Magic Bank Loan Helper", page_icon="🏦")

st.title("🏦 Magic Bank Loan Helper")
st.markdown("### Intelligent Underwriting Demo")
st.markdown("Enter applicant details below to get an instant AI-powered credit decision.")

# --- Sidebar Inputs ---
with st.sidebar:
    st.header("Applicant Details")
    name = st.text_input("Full Name", value="John Doe")
    age = st.number_input("Age", min_value=18, max_value=70, value=30)
    employment_type = st.selectbox(
        "Employment Type", 
        ["salaried", "self-employed", "student", "unemployed"]
    )
    
    st.header("Financials")
    monthly_income = st.number_input("Monthly Income ($)", min_value=0.0, value=5000.0, step=100.0)
    existing_emi = st.number_input("Existing Monthly EMI ($)", min_value=0.0, value=500.0, step=50.0)
    credit_score = st.slider("Credit Score", 0, 900, 720)
    
    st.header("Loan Request")
    loan_amount = st.number_input("Loan Amount Requested ($)", min_value=1000.0, value=50000.0, step=1000.0)
    tenure_years = st.slider("Tenure (Years)", 1, 30, 5)

# --- Logic ---
if st.button("Analyze Application", type="primary"):
    # Construct payload matching Pydantic model
    payload = {
        "name": name,
        "age": age,
        "monthly_income": monthly_income,
        "existing_emi": existing_emi,
        "loan_amount": loan_amount,
        "tenure_years": tenure_years,
        "credit_score": credit_score,
        "employment_type": employment_type
    }
    
    with st.spinner("Crunching numbers..."):
        try:
            response = requests.post(API_URL, json=payload)
            
            if response.status_code == 200:
                data = response.json()
                
                # --- Result Display ---
                st.divider()
                
                # 1. Decision Header
                decision = data['approval']
                risk_score = data['risk_score']
                
                if decision == "Approved":
                    st.success(f"## ✅ Decision: {decision}")
                elif decision == "Rejected":
                    st.error(f"## ❌ Decision: {decision}")
                else:
                    st.warning(f"## ⚠️ Decision: {decision}")
                
                # 2. Score Gauge
                col1, col2 = st.columns([1, 2])
                with col1:
                    st.metric("Risk Score (0-100)", f"{risk_score:.1f}")
                    st.progress(int(risk_score))
                    st.caption("Lower is better")
                
                # 3. Reasons
                with col2:
                    st.subheader("Analysis Report")
                    for reason in data['reasons']:
                        st.write(f"• {reason}")
                
                # Raw JSON expander for tech demo purposes
                with st.expander("View Raw API Response"):
                    st.json(data)
                    
            else:
                st.error(f"Error {response.status_code}: {response.text}")
                
        except requests.exceptions.ConnectionError:
            st.error("❌ Could not connect to the Backend API. Is it running on port 8000?")
            
st.markdown("---")
st.caption("⚠️ **Disclaimer:** This is a demo application for educational purposes only. It does not provide real financial advice.")