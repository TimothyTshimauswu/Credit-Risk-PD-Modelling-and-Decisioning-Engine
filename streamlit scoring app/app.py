import streamlit as st
import pandas as pd
import numpy as np
import joblib
from datetime import date

# ✅ set_page_config MUST be the first Streamlit command
st.set_page_config(
    page_title="Loan Default Risk Management System",
    layout="wide"
)

# =====================================================
# 1. Load final XGBoost pipeline
# =====================================================

@st.cache_resource
def load_model():
    model_path = "xgboost_model_01.pkl"  # make sure this file is in the same folder
    pipe = joblib.load(model_path)
    return pipe

xgb_final_pipe = load_model()

# =====================================================
# 2. Feature engineering (must match training notebook)
# =====================================================

def engineer_features_for_scoring(df_raw: pd.DataFrame) -> pd.DataFrame:
    """
    Apply the SAME feature engineering used in training to new applications.
    This must stay consistent with your training notebook.
    """
    df = df_raw.copy()

    # -----------------------------
    # Core ratios and instalment
    # -----------------------------
    # DTI
    df["DTI"] = np.where(
        df["Income"] == 0,
        0,
        df["Annual_Expenses"] / df["Income"]
    )

    # Income / Loan
    df["Income_Loan_Ratio"] = np.where(
        df["Loan_Amount"] == 0,
        0,
        df["Income"] / df["Loan_Amount"]
    )

    # Loan / Income
    df["Loan_to_Income_Ratio"] = np.where(
        df["Income"] == 0,
        0,
        df["Loan_Amount"] / df["Income"]
    )

    # Monthly instalment (12% annual rate assumption)
    r = 0.12 / 12
    P = df["Loan_Amount"]
    n = df["Loan_Term_Months"]
    df["Monthly_Installment"] = (
        P * (r * (1 + r) ** n) / ((1 + r) ** n - 1)
    ).round()

    # Affordability score
    df["Monthly_Income"] = df["Income"] / 12
    burden = np.where(
        df["Monthly_Income"] == 0,
        np.nan,
        df["Monthly_Installment"] / df["Monthly_Income"]
    )
    aff_raw = 1 - burden
    df["Affordability_Score"] = (np.clip(aff_raw, 0, 1) * 100).round()
    df["Affordability_Score"] = df["Affordability_Score"].fillna(0)

    df.drop(columns=["Monthly_Income"], inplace=True)

    # -----------------------------
    # Dates and vintage
    # -----------------------------
    df["Application_Date"] = pd.to_datetime(df["Application_Date"], errors="coerce")

    max_date = df["Application_Date"].max()
    df["App_Vintage"] = ((max_date - df["Application_Date"]).dt.days / 30).round().astype("Int64")

    # -----------------------------
    # Binned variables
    # -----------------------------
    df["Age_Band"] = pd.cut(
        df["Age"],
        bins=[20, 30, 40, 50, 60, 70],
        labels=["21-30", "31-40", "41-50", "51-60", "61-70"],
        include_lowest=True
    )

    df["Credit_Band"] = pd.cut(
        df["Credit_Score"],
        bins=[0, 680, 700, 720, 900],
        labels=["Subprime", "Near-prime", "Prime", "Super-prime"],
        include_lowest=True
    )

    tenure_map = {
        "< 1 year": "0-1 yr",
        "1 year": "1-3 yrs",
        "2 years": "1-3 yrs",
        "3 years": "3-5 yrs",
        "4 years": "3-5 yrs",
        "5 years": "5-7 yrs",
        "6 years": "5-7 yrs",
        "7 years": "7-10 yrs",
        "8 years": "7-10 yrs",
        "9 years": "7-10 yrs",
        "10+ years": "10+ yrs",
    }
    df["Employment_Tenure_Band"] = df["Employment_Status"].map(tenure_map).fillna("Unknown")

    # -----------------------------
    # Flags
    # -----------------------------
    df["Has_Past_Defaults"] = (df["Past_Defaults"] > 0).astype(int)
    df["High_DTI_Flag"] = (df["DTI"] > 0.6).astype(int)
    df["Low_Affordability_Flag"] = (df["Affordability_Score"] < 85).astype(int)

    # Ensure all engineered columns exist
    engineered_cols = [
        "DTI",
        "Income_Loan_Ratio",
        "Loan_to_Income_Ratio",
        "Monthly_Installment",
        "Affordability_Score",
        "Age_Band",
        "Credit_Band",
        "Employment_Tenure_Band",
        "Has_Past_Defaults",
        "High_DTI_Flag",
        "Low_Affordability_Flag",
        "App_Vintage",
    ]
    for c in engineered_cols:
        if c not in df.columns:
            df[c] = np.nan

    return df


# =====================================================
# 3. Scoring helper
# =====================================================

def add_risk_band(pd_series: pd.Series) -> pd.Series:
    """
    Simple risk banding based on PD.
    Adjust thresholds as needed.
    """
    def band(p):
        if p >= 0.40:
            return "High Risk"
        elif p >= 0.25:
            return "Medium Risk"
        else:
            return "Low Risk"
    return pd_series.apply(band)


def score_new_applications(df_new: pd.DataFrame) -> pd.DataFrame:
    """
    Takes raw applications, applies feature engineering,
    scores with the final XGBoost pipeline, and adds risk bands.
    """
    df_fe = engineer_features_for_scoring(df_new)

    # Drop columns that were not used for training (target / leakage)
    drop_cols = ["Defaulted", "Approval_Status"]
    df_fe = df_fe.drop(columns=[c for c in drop_cols if c in df_fe.columns])

    proba = xgb_final_pipe.predict_proba(df_fe)[:, 1]
    pred = xgb_final_pipe.predict(df_fe)

    out = df_new.copy()
    out["PD_Default"] = proba
    out["Default_Pred"] = pred
    out["Risk_Band"] = add_risk_band(out["PD_Default"])

    return out


# =====================================================
# 4. Streamlit UI
# =====================================================



st.title("Loan Default Risk Management System")
st.write("Scoring UI powered by the tuned XGBoost model.")

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
# Mode 1: Single customer scoring
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
        input_dict = {
            "Customer_ID": [customer_id],
            "Age": [age],
            "Income": [income],
            "Annual_Expenses": [expenses],
            "Loan_Amount": [loan_amount],
            "Loan_Term_Months": [term],
            "Credit_Score": [credit_score],
            "Employment_Status": [employment_status],
            "Marital_Status": [marital_status],
            "Education_Level": [education_level],
            "Property_Ownership": [property_owner],
            "Loan_Purpose": [loan_purpose],
            "Co_Applicant": [co_applicant],
            "Approval_Channel": [approval_channel],
            "Region": [region],
            "Application_Date": [pd.to_datetime(app_date)],
            "Past_Defaults": [past_defaults],
            "Approval_Status": [""],  # placeholder for schema alignment
            "Defaulted": [0],         # placeholder
        }

        df_single = pd.DataFrame(input_dict)
        scored_single = score_new_applications(df_single)

        st.subheader("Scoring Result")
        pd_val = scored_single.loc[0, "PD_Default"]
        band_val = scored_single.loc[0, "Risk_Band"]
        pred_val = scored_single.loc[0, "Default_Pred"]

        st.metric("Predicted PD (Default)", f"{pd_val:.3f}")
        st.write(f"**Risk Band:** {band_val}")
        st.write(f"**Predicted Class:** {int(pred_val)} (1 = Default, 0 = Non-Default)")

        st.write("Full record:")
        st.dataframe(scored_single)

# -----------------------------------------------------
# Mode 2: Batch scoring
# -----------------------------------------------------
else:
    st.subheader("Batch Scoring – CSV Upload")

    st.write("Upload a CSV with raw application data. Expected columns include:")
    st.code(
        "Customer_ID, Age, Income, Annual_Expenses, Loan_Amount, Loan_Term_Months,\n"
        "Credit_Score, Employment_Status, Marital_Status, Education_Level,\n"
        "Property_Ownership, Loan_Purpose, Co_Applicant, Approval_Channel,\n"
        "Region, Application_Date, Past_Defaults, Approval_Status (optional), Defaulted (optional)"
    )

    file = st.file_uploader("Upload CSV file", type=["csv"])

    if file is not None:
        df_upload = pd.read_csv(file)
        st.write("Preview of uploaded data:")
        st.dataframe(df_upload.head())

        if st.button("Run Scoring"):
            scored_batch = score_new_applications(df_upload)
            st.success("Scoring completed.")
            st.write("Sample of scored records:")
            st.dataframe(scored_batch.head())

            # Download button
            csv_out = scored_batch.to_csv(index=False).encode("utf-8")
            st.download_button(
                label="Download scored file as CSV",
                data=csv_out,
                file_name="scored_loan_applications.csv",
                mime="text/csv",
            )