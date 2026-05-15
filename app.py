import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier

@st.cache_data
def load_data():
    return pd.pd.read_csv("telecom_churn_data.csv")

st.title("Telecom Churn Prediction UI")

st.markdown("This application allows you to explore the synthetic telecom dataset and make real-time churn predictions.")

try:
    df = pd.read_csv("telecom_churn_data.csv")
    
    st.header("1. Dataset Explorer")
    if st.checkbox("Show Raw Data"):
        st.write(df.head(100))
        
    st.write(f"**Total Records:** {df.shape[0]}")
    st.write(f"**Churn Rate:** {(df['target'].mean() * 100):.2f}%")
    
    # Train a local model for the interactive UI
    X = df.drop(columns=['target'])
    y = df['target']
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X, y)
    
    st.header("2. Predict Churn for a New Customer")
    st.markdown("Adjust the sliders and toggles below to see how different factors affect the likelihood of a customer churning.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        tenure_months = st.slider("Tenure (Months)", 1, 72, 12)
        monthly_charges = st.slider("Monthly Charges ($)", 20.0, 120.0, 60.0)
        total_charges = tenure_months * monthly_charges
        st.write(f"**Calculated Total Charges:** ${total_charges:.2f}")
        
    with col2:
        internet_service_fiber = st.selectbox("Internet Service (Fiber Optic)", [0, 1])
        has_device_protection = st.selectbox("Has Device Protection", [0, 1])
        has_tech_support = st.selectbox("Has Tech Support", [0, 1])
        contract_type = st.selectbox("Contract Type", ["Month-to-Month", "One Year", "Two Year"])
        paperless_billing = st.selectbox("Paperless Billing", [0, 1])
        
    is_contract_one_year = 1 if contract_type == "One Year" else 0
    is_contract_two_year = 1 if contract_type == "Two Year" else 0
    
    input_data = pd.DataFrame({
        'tenure_months': [tenure_months],
        'monthly_charges': [monthly_charges],
        'internet_service_fiber': [internet_service_fiber],
        'has_device_protection': [has_device_protection],
        'has_tech_support': [has_tech_support],
        'is_contract_one_year': [is_contract_one_year],
        'is_contract_two_year': [is_contract_two_year],
        'paperless_billing': [paperless_billing],
        'total_charges': [total_charges]
    })
    
    if st.button("Predict Churn"):
        prediction = model.predict(input_data)[0]
        prob = model.predict_proba(input_data)[0][1]
        
        if prediction == 1:
            st.error(f"⚠️ High Risk of Churn! (Probability: {prob*100:.1f}%)")
        else:
            st.success(f"✅ Low Risk of Churn. (Probability: {prob*100:.1f}%)")
            
except FileNotFoundError:
    st.error("Error: 'telecom_churn_data.csv' not found. Please run generate_telecom_data.py first.")
