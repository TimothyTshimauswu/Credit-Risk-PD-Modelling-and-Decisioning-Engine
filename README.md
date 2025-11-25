<p align="center">
  <img src="assets/project_banner.png" width="100%" alt="Credit Risk PD Modelling and Decisioning Engine Banner">
</p>

<h1 align="center">Credit Risk PD Modelling and Decisioning Engine</h1>

<h3 align="center">
  XGBoost • Optuna • Feature Engineering • FastAPI Microservice • Streamlit UI • Docker • SQL • Power BI
</h3>

<p align="center">
  A complete end-to-end Probability of Default (PD) modelling and credit decisioning system built on 1,000,000+ retail loan records. 
  The solution includes model development, feature engineering, API deployment, containerised microservices, a business-facing scoring 
  application, SQL portfolio analytics, and a Power BI dashboard for credit-risk monitoring.
</p>

---
# Loan Default Risk Management System

A full-stack credit-risk modeling and scoring pipeline I built to improve lending decisions, reduce losses, and support portfolio analytics.

## Executive Summary

This project started with my own experience applying for car finance. When I met with a Credit Risk Analyst at Standard Bank, we discussed my net income, monthly expenses, credit score, and repayment behaviour to determine my affordability and default risk.

Different banks gave me different quotations. Some took long to assess my profile, requested multiple documents, and delayed their decisions. One bank assessed me within minutes with a clear risk score, an affordability view, and an interest rate aligned to my risk level.

That comparison showed me the value of an efficient, well-calibrated risk engine. I realised how much time, capital, and decision quality depend on a robust scoring system.

This experience inspired me to build a production-grade credit-risk pipeline that replicates how banks should evaluate customers at scale.

I engineered a system that processes more than one million loan applications, predicts probability of default with high accuracy, segments customers by risk profile, and exposes a real-time scoring API deployed with Docker, FastAPI, and AWS. I built dashboards so risk and management teams can assess portfolio exposure any time.

---

## Business Problem

Lending teams face long assessment cycles, inconsistent affordability checks, and limited visibility into portfolio-level exposure.

I designed this project to answer four business questions:

1. What is each applicant’s probability of default  
2. How income, expenses, credit history, and behavioural factors influence risk  
3. How approval and pricing rules should vary across risk segments  
4. How portfolio exposure changes when underwriting rules are adjusted  

The goal is to support faster decisions, lower default risk, improve affordability assessments, and strengthen capital allocation.

---

## 📁 Project Structure

| Folder / File | Description |
|---------------|-------------|
| `data/` | Raw and processed datasets |
| `notebooks/` | EDA, feature engineering, model training & tuning |
| `models pkl/` | Saved XGBoost, LightGBM, RF, Logistic models |
| `app/` | FastAPI scoring backend |
| `streamlit scoring app/` | Streamlit user interface |
| `sql/` | SQL analytics for credit portfolio insights |
| `Power BI credit dashboard/` | Power BI visuals and reporting |
| `Dockerfile` | API Docker container |
| `streamlit.Dockerfile` | Streamlit Docker container |
| `docker-compose.yml` | Orchestration for multi-container setup |
| `assets/` | Images, banners, visuals |

---
## Technical Overview

I built the system end to end, covering data engineering, modelling, deployment, and analytics.

### 1. Data Engineering

I processed more than one million loan records and engineered credit-relevant features:

- Debt-to-income ratios  
- Income stability  
- Expense structures  
- Previous arrears  
- Credit score proxies  
- Employment and repayment history  

### 2. Model Development

I benchmarked the following models:

- Logistic Regression  
- Random Forest  
- LightGBM  
- XGBoost  

I used Optuna for hyperparameter tuning and selected a tuned XGBoost model for the final pipeline.

**Model performance:**

- ROC AUC: 0.87  
- Accuracy: 82 percent  
- Strong separation across PD buckets  

### 3. Risk Segmentation

- PD buckets for approval, review, and decline  
- SHAP explanations for transparency and compliance  

### 4. Portfolio Analytics

I created portfolio-level insights to support key management KPIs:

- Approval rate  
- Expected loss  
- Non-performing loan ratio  
- Risk migration  
- Exposure by product, loan size, income group, and location  

These analytics support conservative, baseline, and relaxed scenario testing.


### 5. Deployment

- Docker for environment consistency  
- FastAPI endpoint for real-time scoring  
- AWS-hosted deployment  
- Streamlit web app for underwriting and risk teams  

## 🟢 Streamlit Scoring UI Deployment
<p align="center">
  <img src="assets/streamlitapp.png" width="85%" alt="Streamlit Scoring UI">
  <br>
  <em>Streamlit scoring interface integrated with the FastAPI decision engine</em>
</p>

The Streamlit UI mirrors real credit decisioning front-ends:

### ✔ **Single Customer Scoring**
- Borrower attributes entered manually  
- UI calculates affordability  
- Data sent to FastAPI  
- Displays PD, class, and risk band  

### ✔ **Batch CSV Scoring**
- Upload raw data  
- Each row processed via API  
- Downloadable scored dataset  

### ✔ **Transparency**
- Full API payload displayed  
- Useful for governance & auditability  

---

## 🚀 FastAPI Deployment

The FastAPI scoring service exposes the production-ready `/predict` endpoint.  
It applies full feature engineering server-side and returns:

- Probability of Default (PD)  
- Binary default prediction  
- Assigned risk band  

Below is a screenshot of the live API running through Docker:

<p align="center">
  <img src="assets/FASTAPI_prediction.png" width="85%" alt="FastAPI Predict Endpoint Screenshot">
</p>
Returns:
```json

  {"Customer_ID": 1,
  "Predicted_PD": 0.236,
  "Predicted_Class": 0,
  "Risk_Band": "Low Risk"}

---

### **AWS Cloud Deployment**
- Containerised using Docker  
- Supports scalable, low-latency model inference  
- Ready for enterprise production environments  

---
## 🛠️ Tech Stack

- **Python:** Pandas, NumPy, Scikit-Learn, XGBoost, LightGBM, Optuna  
- **Database & Analytics:** SQL  
- **Deployment:** Streamlit, FastAPI, Docker, AWS  
- **Reporting:** Power BI  
- **Versioning & Packaging:** joblib, pickle  

---

## Results and Business Impact

The final system improves both predictive accuracy and operational efficiency:

1. Real-time scoring reduces manual assessment time  
2. Portfolio dashboards reduce ad hoc reporting by more than five hours per week  
3. High-performance PD predictions strengthen underwriting consistency  
4. Management can quantify the impact of policy changes before deployment  
5. Consistent PD buckets support better risk governance and capital planning  
6. Customer-level explanations increase transparency across the credit value chain  

These improvements reduce expected losses, improve affordability checks, and speed up customer decision times.

---

## How Teams Use This System

- Credit Underwriting uses the FastAPI endpoint for instant PD scoring  
- Risk Analysts use dashboards to track exposure and identify rising-risk groups  
- Collections teams prioritise accounts using PD buckets  
- Management uses scenario simulations for risk appetite and pricing decisions  

---

## Recommendations

1. Integrate the scoring API into the loan-origination workflow  
2. Use PD segmentation to refine approval and pricing rules  
3. Strengthen verification checks for high-risk profiles  
4. Align PD calibration with IFRS 9 reporting  

---

## Next Steps

1. Build a drift-monitoring pipeline  
2. Develop early-warning signals for existing customers  
3. Expand the engine across multiple credit products  
4. Deploy on AWS Lambda or ECS for scalable workloads





