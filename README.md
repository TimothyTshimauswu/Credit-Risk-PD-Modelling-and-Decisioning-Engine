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

## 📘 Project Background

Banks depend on Probability of Default (PD) models to control non-performing loans, price credit risk, support IFRS9 staging, and drive lending decisions across digital and branch channels.  
Strong PD engines help lenders:

- Improve approval accuracy  
- Reduce early delinquency  
- Strengthen expected credit loss (ECL) stability  
- Provide consistent decisions across touchpoints  

Industry benchmarks show that well-calibrated PD models can:

- Reduce NPL inflows by **10–25%**  
- Improve approval efficiency by **15–20%**  
- Increase collections effectiveness by **20–30%**

This project replicates a real PD modelling and deployment workflow used in lending environments.

---

## 🧠 Project Overview

This system includes:

### **1. Model Development**
- 1M+ loan applications processed  
- Full exploratory and risk analysis  
- Variable engineering aligned with credit-scorecard design  
- Optuna hyperparameter tuning  
- Benchmarking of four models  
- Final production model: **Tuned XGBoost pipeline**

### **2. Production Model Scoring (FastAPI)**
- Feature engineering encoded server-side  
- `/predict` scoring endpoint returning:
  - PD (Probability of Default)  
  - Binary default prediction  
  - Risk band (Low, Medium, High Risk)  

### **3. Frontend Credit Scoring App (Streamlit)**
- Business-facing scoring panel  
- Single-customer scoring  
- CSV batch scoring  
- Full API integration  
- Shows scoring payloads and outputs

### **4. Containerised Microservice Deployment**
- FastAPI backend container  
- Streamlit UI container  
- Shared Docker network  
- Orchestrated with Docker Compose

### **5. Analytics & Reporting**
- SQL portfolio analytics  
- Power BI credit performance dashboard  
- Exploratory analysis and behavioural insights

---

## 🎯 Key Objectives

- Build and validate a PD model using lending-grade data  
- Engineer affordability, behavioural, tenure, and credit-score features  
- Benchmark and tune multiple ML models  
- Deploy a production scoring engine with a REST API  
- Create a scoring UI for analysts and credit teams  
- Generate portfolio insights using SQL and Power BI  

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

## 🧹 Data Preprocessing & Feature Engineering

Risk-focused engineered variables:

- **DTI (Debt-to-Income)**  
- **Income/LTV ratios**  
- **Loan-to-Income Ratio**  
- **Monthly Instalment (amortisation formula)**  
- **Affordability Score**  
- **Age Band**  
- **Credit Score Band**  
- **Employment Tenure Band**  
- **Flags: High DTI, Low Affordability, Past Default**  
- **Vintage (Months since application)**  

These transformations were reproduced **inside the FastAPI container** for consistent production scoring.

---

## 📈 Exploratory Data Analysis

- Default rate trends across demographics and regions  
- Correlation and multicollinearity analysis  
- Risk by loan purpose, employment, property type  
- Affordability vs default likelihood  
- Vintage and time-based delinquency patterns  
- Portfolio segmentation and NPL concentration  

---

## 🤖 Modelling Approach

### **Models Benchmarked**
- XGBoost (final model)  
- LightGBM  
- Random Forest  
- Linear Regression (baseline)

### **Model Evaluation**
- AUC  
- Recall on the default class  
- KS statistic  
- Calibration curves  
- Segment stability and uplift  

### **Optuna Tuning**
- Automated multi-trial search  
- Early pruning  
- Best hyperparameters exported to final model pipeline  

### **Final Model: XGBoost**
Chosen for:

- High discriminatory power  
- Robust calibration  
- Strong risk-segmentation uplift  
- Operational stability

---

## 🟢 Streamlit Scoring UI

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

## 🚀 FastAPI Scoring Service

### **Endpoints**
#### `GET /health`
Health check.

#### `POST /predict`
Returns:

```json
{
  "Customer_ID": 1,
  "Predicted_PD": 0.236,
  "Predicted_Class": 0,
  "Risk_Band": "Low Risk"
}

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
