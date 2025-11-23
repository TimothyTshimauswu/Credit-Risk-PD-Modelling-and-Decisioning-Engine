<p align="center">
  <img src="assets/project_banner.png" width="100%" alt="Credit Risk PD Modelling and Decisioning Engine Banner">
</p>

<h1 align="center">Credit Risk PD Modelling and Decisioning Engine</h1>

<h3 align="center">
  Python. XGBoost. LightGBM. Optuna. SQL. Power BI. Streamlit. FastAPI. Docker. AWS.
</h3>

<p align="center">
  A production-grade Probability of Default modelling and decisioning engine built on one million borrower records. Designed to support credit approvals, reduce losses, and strengthen portfolio performance across retail and unsecured lending environments.
</p>

---

# 1. Business Overview

Retail and unsecured lending requires accurate Probability of Default (PD) models to control non-performing loans, maintain capital adequacy, and support sustainable portfolio growth.  
This solution delivers a full credit risk modelling workflow used in banks: data engineering, risk feature creation, PD model development, challenger model validation, deployment, portfolio analytics, and early warning insights.

---

# 2. Business Problem

Legacy rule-based assessments and manual credit evaluations lead to inconsistent decisions and weak risk discrimination. High-risk customers enter the book, Expected Credit Loss (ECL) rises, and collections performance declines.  
A scalable, data-driven PD model and decisioning engine is required to improve approval accuracy, optimise pricing, and highlight high-risk exposure early.

---

# 3. Business Value Delivered

This system produces measurable outcomes aligned with banking performance metrics:

- Strong uplift in identifying high-risk customers across income and product segments.  
- Higher PD model discrimination and stability across folds.  
- Improved approval and decline consistency under model-driven rules.  
- Portfolio-level insights used for ECL forecasting, IFRS9 inputs, and risk committee reporting.  
- Early warning indicators that improve collections strategy.  
- Reduced operational risk through automated scoring and reproducible pipelines.  
- Challenger model framework aligned with internal model risk governance.

---

# 4. Project Architecture

## Data Engineering  
Processes one million loan-level records with robust cleaning and transformation.  
Builds reproducible datasets for model development, risk reporting, and monitoring.

## Credit Risk Analytics  
Identifies key loss drivers, behavioural risk indicators, and segment-level exposure.  
Supports pricing, strategy, and credit policy refinement.

## Feature Engineering  
Creates risk features aligned with PD scorecard development:

- Debt-service ratios  
- Utilisation and exposure patterns  
- Payment behaviour and delinquency indicators  
- Affordability and income stability metrics  
- Temporal trends and behavioural drift variables  

## Modelling and Validation  
Models trained: Random Forest, XGBoost, LightGBM, Linear Regression baseline.  
Optuna tuning improves AUC, precision, recall, and calibration robustness.

Model selection based on:

- Discriminatory power (AUC)  
- Stability across borrower segments  
- Performance on minority default class  
- PD calibration behaviour  
- Portfolio impact under approval scenarios  

## Deployment  
- Streamlit front-end scoring tool for credit analysts  
- FastAPI service for real-time digital decisioning  
- Docker packaging for production-grade deployment  
- AWS hosting for scalable inference  

## Reporting and Monitoring  
SQL analysis and Power BI dashboards used for:

- Monthly risk reporting  
- PD stability monitoring  
- Vintage and cohort tracking  
- Exposure measurement  
- Delinquency and loss trend analysis  
- Collections segmentation  

---

# 5. Banking Use Cases

This engine aligns with how risk and lending teams operate:

- Real-time loan application scoring  
- Limit and pricing decisions based on PD  
- Challenger model development for internal scorecards  
- Exposure and EAD concentration analysis  
- IFRS9 impairment input preparation  
- High-risk customer identification  
- Early delinquency detection and collections prioritisation  
- Portfolio analytics for risk committees  

---

# 6. Key Risk Metrics

- AUC for discriminatory power  
- Recall on high-risk customers  
- PD calibration stability  
- Segment-level default rate profiles  
- Approval rate impacts under model-driven cut-offs  
- Exposure and EAD concentration metrics  

---

# 7. Dataset

One million borrower-level applications containing demographic, financial, behavioural, and loan performance data.  
Includes the target variable for supervised PD modelling.

---

# 8. Exploratory Insights

Key findings from EDA:

- High default concentration in low-income and short-tenure groups  
- Payment behaviour features strongly linked to PD  
- Affordability ratios identified as major risk drivers  
- Risk exposure concentrated in specific product groups  
- Portfolio mix shifts highlight credit policy opportunities  

---

# 9. Feature Engineering

Risk-focused engineered features:

- Normalised affordability and income measures  
- Repayment consistency and delinquency flags  
- Behavioural trend windows  
- Utilisation and exposure indicators  
- Loan-to-income and risk-weighted affordability ratios  
- Temporal drift and stability signals  

---

# 10. Model Development and Selection

Algorithms evaluated:

- Random Forest  
- XGBoost  
- LightGBM  
- Linear Regression baseline  

Optuna tuning improved:

- Model calibration  
- Recall on minority class  
- AUC lift  
- Stability across folds  

Final model: **XGBoost**, selected for superior lift and operational stability.

---

# 11. Production Deployment

## Streamlit Decisioning Tool  
Used by credit analysts and branch officers.  
Shows:

- PD score  
- Confidence interval  
- Top behavioural drivers  

## FastAPI Scoring Service  
Dockerised service for:

- Real-time scoring  
- Digital channel integration  
- Batch inference for risk teams  

## AWS Deployment  
Scalable, low-latency model inference aligned with enterprise system requirements.

---

# 12. SQL Portfolio Analysis

Portfolio analytics layer includes:

- Vintage and cohort analysis  
- Exposure and EAD reporting  
- Segment-level PD analysis  
- Delinquency trend breakdowns  
- Collections segmentation  
- IFRS9 input support  

---

# 13. Power BI Portfolio Dashboard

Built for Credit, Risk, Finance, and Collections teams:

- Default rate trends  
- Exposure distribution by segment  
- PD drift and stability  
- High-risk customer flags  
- Approval and decline patterns  
- Portfolio mix insights  
- Early warning indicators  

---

# 14. Tech Stack

- Python  
- Pandas  
- Scikit-learn  
- XGBoost  
- LightGBM  
- Optuna  
- SQL  
- Streamlit  
- FastAPI  
- Docker  
- AWS  
- Power BI  

---

# 15. Folder Structure

project_root/
│
├── data/
│   ├── raw/
│   ├── processed/
│
├── notebooks/
│   ├── 01_EDA.ipynb
│   ├── 02_FeatureEngineering.ipynb
│   ├── 03_ModelTraining.ipynb
│   ├── 04_ModelValidation.ipynb
│
├── src/
│   ├── data_pipeline.py
│   ├── risk_features.py
│   ├── model_training.py
│   ├── optuna_tuning.py
│   ├── inference_service.py
│
├── deployment/
│   ├── streamlit_app/
│   ├── fastapi_app/
│   ├── Dockerfile
│
├── sql/
│   ├── portfolio_analysis.sql
│
├── dashboards/
│   ├── credit_risk_dashboard.pbix
│
└── README.md


---

# 16. Future Enhancements

- SHAP interpretability for credit committees  
- Automated model monitoring and retraining pipelines  
- Drift detection and PD stability tracking  
- Enterprise data warehouse integration  
- Batch scoring for month-end IFRS9 processes  

---

# License  
MIT License.
