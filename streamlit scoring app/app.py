import os
import streamlit as st
import pandas as pd
import numpy as np
from datetime import date
import requests

# ✅ set_page_config MUST be the first Streamlit command
st.set_page_config(
    page_title="Loan Default Risk Management System",
    layout="wide"
)

# =====================================================
# 1. API configuration
# =====================================================

# Read API URL from environment (Docker), fallback to local for dev
API_URL = os.getenv("API_URL", "http://127.0.0.1:8000/predict")

# Optional: show which API URL is being used (helps debug)
st.sidebar.write("API URL:", API_URL)


# =====================================================
# 2. Helper: Affordability score (same logic as before)
# =====================================================

def compute_affordability_score(income: float, loan_amount: float, term_months: float) -> float:
    """
    Reproduce the affordability score logic from the original feature engineering.
    """
    r = 0.12 / 12
    P = loan_amount
    n = term_months

    if n <= 0 or P <= 0 or income <= 0:
        return 0.0

    monthly_installment = P * (r * (1 + r) ** n) / ((1 + r) ** n - 1)
    monthly_income = income / 12

    if monthly_income <= 0:
        return 0.0

    burden = monthly_installment / monthly_income
    aff_raw = 1 - burden
    aff_score = np.clip(aff_raw, 0, 1) * 100
    return float(round(aff_score, 0))


def call_pd_api(payload: dict) -> dict:
    """
    Call the FastAPI PD prediction endpoint.
    """
    try:
        response = requests.post(API_URL, json=payload, timeout=10)
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"API error {response.status_code}: {response.text}"}
    except Exception as e:
        return {"error": str(e)}


# =====================================================
# 3. Streamlit UI
# =====================================================

st.title("Loan Default Risk Management System")
st.write("Scoring UI powered by the Credit Risk PD Modelling and Decisioning Engine API.")

mode = st.sidebar.radio(
    "Scoring mode",
    ["Single customer", "Batch scoring (CSV)"]
)

# Common reference lists
regions = [
    "Gauteng", "KwaZulu-Natal", "Western Cape", "Eastern Cape",
    "Northern Cape", "Free State", "North West", "Limpopo", "Mpumalanga"
]

employment_statuses = [
    "10+ years", "9 years", "8 years", "7 years", "6 years",
    "5 years", "4 years", "3 years", "2 years", "1 year", "< 1 year"
]

marital_statuses = ["Single", "Married", "Divorced"]
education_levels = ["High School", "Diploma", "Degree", "Masters"]
property_types = ["OWN", "RENT", "MORTGAGE", "ANY", "OTHER", "NONE"]
loan_purposes = [
    "debt_consolidation", "credit_card", "home_improvement", "medical",
    "small_business", "vacation", "major_purchase", "other"
]
approval_channels = ["Web", "Agent", "Branch", "Mobile App"]
co_applicant_opts = ["No", "Yes"]


# -----------------------------------------------------
# Mode 1: Single customer scoring (via API)
# -----------------------------------------------------
if mode == "Single customer":
    st.subheader("Single Customer Scoring")

    with st.form("single_customer_form"):
        col1, col2, col3 = st.columns(3)

        with col1:
            customer_id = st.number_input("Customer ID", min_value=1, value=1, step=1)
            age = st.slider("Age", min_value=21, max_value=70, value=35)
            income = st.number_input("Annual Income (ZAR)", min_value=0, value=80000, step=1000)
            expenses = st.number_input("Annual Expenses (ZAR)", min_value=0, value=35000, step=1000)
            loan_amount = st.number_input("Loan Amount (ZAR)", min_value=1000, max_value=40000, value=15000, step=500)
            term = st.selectbox("Loan Term (months)", options=[36, 48, 60], index=0)

        with col2:
            credit_score = st.slider("Credit Score", min_value=660, max_value=850, value=700, step=1)
            employment_status = st.selectbox("Employment Status", employment_statuses)
            marital_status = st.selectbox("Marital Status", marital_statuses)
            education_level = st.selectbox("Education Level", education_levels)
            property_owner = st.selectbox("Property Ownership", property_types)
            past_defaults = st.number_input("Past Defaults", min_value=0, value=0, step=1)

        with col3:
            loan_purpose = st.selectbox("Loan Purpose", loan_purposes)
            co_applicant = st.selectbox("Co-Applicant", co_applicant_opts)
            approval_channel = st.selectbox("Approval Channel", approval_channels)
            region = st.selectbox("Region", regions)
            app_date = st.date_input("Application Date", value=date.today())

        submitted = st.form_submit_button("Score Customer")

    if submitted:
        # Compute affordability score on the frontend to send to API
        affordability_score = compute_affordability_score(income, loan_amount, term)
        app_date_str = app_date.isoformat()
        app_month = app_date.strftime("%b")  # e.g. "Jan", "Feb"

        payload = {
            "Customer_ID": customer_id,
            "Age": age,
            "Income": income,
            "Annual_Expenses": expenses,
            "Loan_Amount": loan_amount,
            "Loan_Term_Months": term,
            "Credit_Score": credit_score,
            "Employment_Status": employment_status,
            "Marital_Status": marital_status,
            "Education_Level": education_level,
            "Property_Ownership": property_owner,
            "Loan_Purpose": loan_purpose,
            "Co_Applicant": co_applicant,
            "Approval_Channel": approval_channel,
            "Region": region,
            "Application_Date": app_date_str,
            "Past_Defaults": past_defaults,
            "DTI": 0,                     # will be recomputed in API
            "Income_Loan_Ratio": 0,       # recomputed in API
            "Monthly_Installment": 0,     # recomputed or not used
            "Loan_to_Income_Ratio": 0,    # recomputed in API
            "Affordability_Score": affordability_score,
            "App_Month": app_month
        }

        with st.spinner("Scoring customer via API..."):
            result = call_pd_api(payload)

        if "error" in result:
            st.error("Error from API")
            st.write(result["error"])
        else:
            st.subheader("Scoring Result")
            pd_val = result.get("Predicted_PD", None)
            band_val = result.get("Risk_Band", None)
            pred_val = result.get("Predicted_Class", None)

            if pd_val is not None:
                st.metric("Predicted PD (Default)", f"{pd_val:.3f}")
            else:
                st.write("Predicted PD not returned by API")

            if band_val is not None:
                st.write(f"**Risk Band:** {band_val}")
            if pred_val is not None:
                st.write(f"**Predicted Class:** {int(pred_val)} (1 = Default, 0 = Non-Default)")

            st.write("Payload sent to API:")
            st.json(payload)


# -----------------------------------------------------
# Mode 2: Batch scoring – CSV via API (row by row)
# -----------------------------------------------------
else:
    st.subheader("Batch Scoring – CSV Upload")

    st.write("Upload a CSV with raw application data. Expected columns include:")
    st.code(
        "Customer_ID, Age, Income, Annual_Expenses, Loan_Amount, Loan_Term_Months,\n"
        "Credit_Score, Employment_Status, Marital_Status, Education_Level,\n"
        "Property_Ownership, Loan_Purpose, Co_Applicant, Approval_Channel,\n"
        "Region, Application_Date, Past_Defaults"
    )

    file = st.file_uploader("Upload CSV file", type=["csv"])

    if file is not None:
        df_upload = pd.read_csv(file)
        st.write("Preview of uploaded data:")
        st.dataframe(df_upload.head())

        if st.button("Run Scoring via API"):
            results = []
            for idx, row in df_upload.iterrows():
                try:
                    # Compute affordability for this row
                    income = float(row.get("Income", 0) or 0)
                    loan_amount = float(row.get("Loan_Amount", 0) or 0)
                    term = float(row.get("Loan_Term_Months", 0) or 0)
                    affordability_score = compute_affordability_score(income, loan_amount, term)

                    # Application date handling
                    app_date_val = pd.to_datetime(row.get("Application_Date"), errors="coerce")
                    if pd.isna(app_date_val):
                        app_date_str = date.today().isoformat()
                        app_month = date.today().strftime("%b")
                    else:
                        app_date_str = app_date_val.date().isoformat()
                        app_month = app_date_val.strftime("%b")

                    payload = {
                        "Customer_ID": int(row.get("Customer_ID", 0)),
                        "Age": float(row.get("Age", 0) or 0),
                        "Income": income,
                        "Annual_Expenses": float(row.get("Annual_Expenses", 0) or 0),
                        "Loan_Amount": loan_amount,
                        "Loan_Term_Months": term,
                        "Credit_Score": float(row.get("Credit_Score", 0) or 0),
                        "Employment_Status": str(row.get("Employment_Status", "")),
                        "Marital_Status": str(row.get("Marital_Status", "")),
                        "Education_Level": str(row.get("Education_Level", "")),
                        "Property_Ownership": str(row.get("Property_Ownership", "")),
                        "Loan_Purpose": str(row.get("Loan_Purpose", "")),
                        "Co_Applicant": str(row.get("Co_Applicant", "")),
                        "Approval_Channel": str(row.get("Approval_Channel", "")),
                        "Region": str(row.get("Region", "")),
                        "Application_Date": app_date_str,
                        "Past_Defaults": float(row.get("Past_Defaults", 0) or 0),
                        "DTI": 0,
                        "Income_Loan_Ratio": 0,
                        "Monthly_Installment": 0,
                        "Loan_to_Income_Ratio": 0,
                        "Affordability_Score": affordability_score,
                        "App_Month": app_month
                    }

                    result = call_pd_api(payload)

                    if "error" in result:
                        results.append({
                            **row.to_dict(),
                            "PD_Default": None,
                            "Default_Pred": None,
                            "Risk_Band": f"API error: {result['error']}"
                        })
                    else:
                        results.append({
                            **row.to_dict(),
                            "PD_Default": result.get("Predicted_PD", None),
                            "Default_Pred": result.get("Predicted_Class", None),
                            "Risk_Band": result.get("Risk_Band", None)
                        })

                except Exception as e:
                    results.append({
                        **row.to_dict(),
                        "PD_Default": None,
                        "Default_Pred": None,
                        "Risk_Band": f"Exception: {e}"
                    })

            scored_batch = pd.DataFrame(results)
            st.success("Batch scoring via API completed.")
            st.write("Sample of scored records:")
            st.dataframe(scored_batch.head())

            # Download button
            csv_out = scored_batch.to_csv(index=False).encode("utf-8")
            st.download_button(
                label="Download scored file as CSV",
                data=csv_out,
                file_name="scored_loan_applications_api.csv",
                mime="text/csv",
            )