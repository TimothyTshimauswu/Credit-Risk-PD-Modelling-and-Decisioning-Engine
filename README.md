<p align="center">
  <img src="assets/project_banner.png" width="100%" alt="Credit Risk PD Modelling and Decisioning Engine Banner">
</p>

<h1 align="center">Credit Risk PD Modelling and Decisioning Engine</h1>

<h3 align="center">
  XGBoost • LightGBM • Optuna Tuning • FastAPI Deployment • Streamlit Scoring • SQL Analytics • Power BI
</h3>

<p align="center">
  A full end-to-end Probability of Default modelling and decisioning engine built on one million loan records. Designed for real lending environments to support credit approvals, reduce losses, and improve portfolio performance.
</p>


## Project Background

Retail banking and unsecured lending rely on accurate risk models to manage non-performing loans, optimise pricing, and strengthen portfolio growth. With rising competition and tighter regulatory expectations, banks need PD models that deliver strong discrimination, operational stability, and scalable deployment.

Industry benchmarks show that effective PD models can reduce early-stage delinquency by **10–25%**, improve approval accuracy by **15–20%**, and support more accurate Expected Credit Loss (ECL) forecasting.  
Major lenders such as **FNB, Capitec, ABSA, and Standard Bank** depend on these systems to manage exposure, inform credit policy, and guide collections strategies.


## 🧠 Project Overview

This project delivers a full credit risk modelling and decisioning engine that enables:

- 🔍 Probability of Default (PD) modelling on one million loan records  
- ⏳ Optuna-driven hyperparameter tuning of multiple ML models  
- 🧩 Feature engineering aligned with credit risk scorecard practices  
- 📉 Portfolio and risk analytics using SQL  
- 🖥️ Streamlit app for real-time customer scoring  
- 🚀 FastAPI + Docker service for production deployment  
- 📊 Power BI dashboards for portfolio monitoring and ECL insights  

---

## 🎯 Key Objectives

- Build a full PD model using retail loan data  
- Engineer borrower- and behaviour-based risk features  
- Benchmark Random Forest, XGBoost, LightGBM, and Linear Regression  
- Use Optuna to optimise model calibration and uplift  
- Deploy the final model into a scoring engine for business use  
- Provide credit policy and collections teams with actionable risk insights  

---

## 📁 Project Structure

| File / Folder | Description |
|---------------|-------------|
| `data/` | Raw and cleaned datasets (1M loan records) |
| `notebooks/` | EDA, feature engineering, modelling, validation |
| `src/` | Data pipeline, feature engineering, model training |
| `deployment/streamlit_app/` | Streamlit scoring app |
| `deployment/fastapi_app/` | FastAPI scoring service |
| `dashboards/` | Power BI credit risk dashboard |
| `sql/portfolio_analysis.sql` | SQL queries for risk and portfolio analytics |
| `assets/` | Project banner and visuals |
| `Dockerfile` | Container for cloud deployment |

---

## 🧹 Data Preprocessing

- Removed duplicates and corrected inconsistent entries  
- Handled missing values in income, employment, and loan attributes  
- Normalised financial variables for improved model stability  
- Capped extreme outliers using winsorisation  
- Created risk-focused engineered features:
  - Debt-service ratios  
  - Repayment behaviour metrics  
  - Utilisation trends  
  - Affordability indicators  
  - Temporal delinquency variables  

---

## 📈 Exploratory Data Analysis

- 📊 Default rate distribution by income, tenure, and loan product  
- 🔥 Correlation analysis of financial and behavioural variables  
- 🧭 Segment-level exposure and NPL concentration  
- 💳 Repayment and delinquency trend patterns  
- 📉 Risk signals across borrower demographics  

---

## 🤖 Modelling Approach

### **Model Benchmarking**
Four models were evaluated:

- XGBoost  
- LightGBM  
- Random Forest  
- Linear Regression (baseline)  

Metrics evaluated:

- AUC  
- Precision/Recall on default class  
- Calibration stability  
- Uplift on high-risk segments  

### **Hyperparameter Tuning – Optuna**
- Multi-trial tuning to maximise AUC  
- Stability checks across folds  
- Parameter optimisation for interpretability and robustness  

### **Final Model**
**XGBoost** selected for:

- Strong discriminatory power  
- Stability across segments  
- PD calibration reliability  
- High uplift in high-risk identification  

---

## 🟢 Streamlit App Overview

The Streamlit application enables:

- 🧍 **Individual client scoring**  
- 📤 **CSV batch scoring for business teams**  
- ✔️ **Probability of Default output**  
- 🔑 **Key driver explanations for credit analysts**  

This mirrors credit decision-support tools used by lending and risk teams in banks.

---

## 🚀 Deployment

### **FastAPI Service**
- Dockerised API for real-time scoring  
- Compatible with digital channels and internal credit systems  
- Allows API-based scoring for automated approvals  

### **AWS Cloud Deployment**
- Containerised using Docker  
- Supports scalable, low-latency model inference  
- Ready for enterprise production environments  

---

## 🧠 Business Impact

This solution supports:

- More accurate credit approval decisions  
- Stronger identification of high-risk applicants  
- Improved Expected Credit Loss (ECL) accuracy  
- Better collections targeting using PD outputs  
- Reduction in approval error rates  
- More consistent decisioning across channels  

Industry impact benchmarks:

- PD models improve approval efficiency by **15–20%**  
- Reduce NPL inflows by **10–25%**  
- Increase collections effectiveness with earlier segmentation  

This aligns with KPIs across Credit Risk, Finance, Data Science, and Lending Operations.

---

## 🛠️ Tech Stack

- **Python:** Pandas, NumPy, Scikit-Learn, XGBoost, LightGBM, Optuna  
- **Database & Analytics:** SQL  
- **Deployment:** Streamlit, FastAPI, Docker, AWS  
- **Reporting:** Power BI  
- **Versioning & Packaging:** joblib, pickle  

---

## 📌 Future Enhancements

- Add SHAP explainability for model governance  
- Deploy Airflow for automated model monitoring  
- Add drift detection for ongoing PD stability  
- Integrate with enterprise data warehouse  
- Build a challenger model for IFRS9 staging  

---
