options compress=yes nofmterr;
libname ecl '/sasdata/credit_risk';

proc import datafile="/sasdata/input/loan_scored.csv"
    out=ecl.loan_scored
    dbms=csv replace;
    guessingrows=10000;
run;

/* LGD lookup by collateral type */
data ecl.lgd_lookup;
    length Property_Ownership $15;
    input Property_Ownership $ LGD;
    datalines;
OWN        0.25
MORTGAGE   0.35
RENT       0.55
;
run;

proc sql;
    create table ecl.loan_ecl as
    select a.*,
           coalesce(b.LGD, 0.45) as LGD
    from ecl.loan_scored a
    left join ecl.lgd_lookup b 
        on a.Property_Ownership = b.Property_Ownership;
quit;

/* ECL calculation */
data ecl.loan_ecl;
    set ecl.loan_ecl;
    
    EAD = Loan_Amount;
    Remaining_Term_Years = Loan_Term_Months / 12;
    
    PD_12M = Predicted_PD;
    PD_Lifetime = 1 - (1 - Predicted_PD) ** Remaining_Term_Years;
    
    if IFRS9_Stage = 'Stage 1' then PD_ECL = PD_12M;
    else PD_ECL = PD_Lifetime;
    
    ECL = EAD * PD_ECL * LGD;
    
    if EAD > 0 then Coverage_Ratio = ECL / EAD;
    else Coverage_Ratio = 0;
    
    format Predicted_PD PD_12M PD_Lifetime PD_ECL Coverage_Ratio percent8.2
           EAD ECL comma18.2;
run;

/* Stage summary */
proc sql;
    create table ecl.stage_summary as
    select IFRS9_Stage,
           count(*) as Accounts format=comma12.0,
           sum(EAD) as Total_EAD format=comma18.0,
           sum(ECL) as Total_ECL format=comma18.0,
           sum(ECL) / sum(EAD) as Coverage_Ratio format=percent8.2,
           mean(Predicted_PD) as Avg_PD format=percent8.2,
           sum(Defaulted) as Default_Count format=comma10.0
    from ecl.loan_ecl
    group by IFRS9_Stage
    order by IFRS9_Stage;
quit;

/* Risk band summary */
proc sql;
    create table ecl.risk_band_summary as
    select Risk_Band,
           count(*) as Accounts format=comma12.0,
           sum(EAD) as Total_EAD format=comma18.0,
           sum(ECL) as Total_ECL format=comma18.0,
           mean(Predicted_PD) as Avg_PD format=percent8.2,
           mean(Defaulted) as Actual_Default_Rate format=percent8.2
    from ecl.loan_ecl
    group by Risk_Band
    order by Avg_PD;
quit;

/* Segment breakdowns */
proc sql;
    create table ecl.ecl_by_region as
    select Region, IFRS9_Stage,
           count(*) as Accounts format=comma12.0,
           sum(EAD) as Total_EAD format=comma18.0,
           sum(ECL) as Total_ECL format=comma18.0
    from ecl.loan_ecl
    group by Region, IFRS9_Stage
    order by Region, IFRS9_Stage;

    create table ecl.ecl_by_purpose as
    select Loan_Purpose, IFRS9_Stage,
           count(*) as Accounts format=comma12.0,
           sum(EAD) as Total_EAD format=comma18.0,
           sum(ECL) as Total_ECL format=comma18.0
    from ecl.loan_ecl
    group by Loan_Purpose, IFRS9_Stage
    order by Loan_Purpose, IFRS9_Stage;

    create table ecl.ecl_by_channel as
    select Approval_Channel, IFRS9_Stage,
           count(*) as Accounts format=comma12.0,
           sum(EAD) as Total_EAD format=comma18.0,
           sum(ECL) as Total_ECL format=comma18.0
    from ecl.loan_ecl
    group by Approval_Channel, IFRS9_Stage
    order by Approval_Channel, IFRS9_Stage;
quit;

/* Decile analysis for model validation */
proc rank data=ecl.loan_ecl out=ecl.ranked groups=10 descending;
    var Predicted_PD;
    ranks Decile;
run;

proc sql;
    create table ecl.decile_analysis as
    select Decile + 1 as Decile,
           count(*) as Accounts format=comma12.0,
           sum(Defaulted) as Defaults format=comma10.0,
           mean(Predicted_PD) as Avg_PD format=percent8.2,
           mean(Defaulted) as Actual_DR format=percent8.2,
           sum(EAD) as Total_EAD format=comma18.0
    from ecl.ranked
    group by Decile
    order by Decile;
quit;

/* Export for reporting */
proc export data=ecl.stage_summary outfile="/sasdata/output/ecl_stage_summary.csv" dbms=csv replace; run;
proc export data=ecl.decile_analysis outfile="/sasdata/output/ecl_decile_analysis.csv" dbms=csv replace; run;
proc export data=ecl.loan_ecl outfile="/sasdata/output/loan_ecl_calculated.csv" dbms=csv replace; run;
