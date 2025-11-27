SELECT * FROM Projects.loan_applications;

 -- Customer Demographics Overview
SELECT 
    AVG(Age) AS avg_age,
    MIN(Age) AS min_age,
    MAX(Age) AS max_age,
    COUNT(*) AS total_customers
FROM loan_applications;

-- Income Distribution by Education Level
SELECT 
    Education_Level,
    AVG(Income) AS avg_income,
    COUNT(*) AS total_applicants
FROM loan_applications
GROUP BY Education_Level
ORDER BY avg_income DESC;


-- Credit Score Analysis by Region
SELECT 
    Region,
    AVG(Credit_Score) AS avg_credit_score,
    MIN(Credit_Score) AS min_score,
    MAX(Credit_Score) AS max_score
FROM loan_applications
GROUP BY Region;

-- Missing Property Ownership Data
SELECT 
    COUNT(*) AS missing_property_ownership
FROM loan_applications
WHERE Property_Ownership IS NULL;

-- Loan Amount vs. Term Correlation
SELECT 
    Loan_Term_Months,
    AVG(Loan_Amount) AS avg_loan_amount
FROM loan_applications
GROUP BY Loan_Term_Months
ORDER BY Loan_Term_Months;

-- Default Rate by Credit Score Range
SELECT 
    CASE 
        WHEN Credit_Score < 500 THEN 'Poor'
        WHEN Credit_Score BETWEEN 500 AND 650 THEN 'Fair'
        WHEN Credit_Score BETWEEN 651 AND 750 THEN 'Good'
        ELSE 'Excellent'
    END AS credit_band,
    COUNT(*) AS total_applicants,
    SUM(Defaulted) AS total_defaults,
    ROUND(SUM(Defaulted) * 100.0 / COUNT(*), 2) AS default_rate_percent
FROM loan_applications
GROUP BY credit_band;

-- Business Analyst SQL Queries

-- Total Loans Approved vs. Rejected
SELECT 
    Approval_Status,
    COUNT(*) AS total_applications
FROM loan_applications
GROUP BY Approval_Status;

-- Loan Purpose Popularity
SELECT 
    Loan_Purpose,
    COUNT(*) AS total_requests
FROM loan_applications
GROUP BY Loan_Purpose
ORDER BY total_requests DESC;

-- Approval Channel Performance
SELECT 
    Approval_Channel,
    COUNT(*) AS total_approved
FROM loan_applications
WHERE Approval_Status = 'Approved'
GROUP BY Approval_Channel
ORDER BY total_approved DESC;

-- Regional Loan Demand
SELECT 
    Region,
    COUNT(*) AS total_applications,
    SUM(Loan_Amount) AS total_loan_value
FROM loan_applications
GROUP BY Region
ORDER BY total_loan_value DESC;

-- Customer Segmentation by Age and Marital Status
SELECT 
    Marital_Status,
    CASE 
        WHEN Age < 30 THEN 'Under 30'
        WHEN Age BETWEEN 30 AND 50 THEN '30-50'
        ELSE 'Over 50'
    END AS age_group,
    COUNT(*) AS total_customers
FROM loan_applications
GROUP BY Marital_Status, age_group
ORDER BY total_customers DESC;

-- Default Rate by Employment Status
SELECT 
    Employment_Status,
    COUNT(*) AS total_applicants,
    SUM(Defaulted) AS total_defaults,
    ROUND(SUM(Defaulted) * 100.0 / COUNT(*), 2) AS default_rate_percent
FROM loan_applications
GROUP BY Employment_Status
ORDER BY default_rate_percent DESC;
