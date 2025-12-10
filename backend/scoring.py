import math
from .models import LoanApplication, LoanDecision

def calculate_monthly_emi(principal: float, annual_rate: float, years: float) -> float:
    """Helper to calculate estimated EMI for the new loan."""
    if years <= 0: return 0
    # Monthly interest rate
    r = (annual_rate / 100) / 12
    n = years * 12
    # Standard EMI formula
    if r == 0:
        return principal / n
    emi = (principal * r * (1 + r)**n) / ((1 + r)**n - 1)
    return emi

def score_loan(app: LoanApplication) -> LoanDecision:
    reasons = []
    risk_score = 50.0  # Start neutral

    # --- 1. Credit Score Analysis ---
    if app.credit_score >= 750:
        risk_score -= 20
        reasons.append("Excellent credit score.")
    elif app.credit_score >= 650:
        risk_score -= 10
        reasons.append("Good credit score.")
    elif app.credit_score < 600:
        risk_score += 20
        reasons.append("Low credit score indicates higher risk.")

    if app.credit_score < 500:
        return LoanDecision(
            approval="Rejected",
            risk_score=95.0,
            reasons=["Credit score is below minimum threshold."]
        )

    # --- 2. Debt-to-Income (DTI) Analysis ---
    # Assume a standard interest rate of 10% for estimation
    estimated_new_emi = calculate_monthly_emi(app.loan_amount, 10.0, app.tenure_years)
    total_obligation = app.existing_emi + estimated_new_emi
    dti_ratio = total_obligation / app.monthly_income

    if dti_ratio > 0.60:
        risk_score += 30
        reasons.append(f"Total debt obligations ({dti_ratio:.0%}) exceed 60% of income.")
    elif dti_ratio > 0.40:
        risk_score += 10
        reasons.append("Moderate debt-to-income ratio.")
    else:
        risk_score -= 10
        reasons.append("Healthy disposable income.")

    # --- 3. Employment & Age factors ---
    if app.employment_type == "unemployed":
        return LoanDecision(
            approval="Rejected",
            risk_score=100.0,
            reasons=["Cannot lend to unemployed applicants."]
        )
    elif app.employment_type == "student":
        risk_score += 10
        reasons.append("Student status increases risk profile.")

    if app.age < 23 and app.loan_amount > 1000000:
        risk_score += 10
        reasons.append("High loan amount for age group.")

    # --- 4. Final Decision Logic ---
    # Clamp score 0-100
    risk_score = max(0.0, min(100.0, risk_score))

    if risk_score > 75:
        decision = "Rejected"
    elif risk_score > 40:
        decision = "Needs Manual Review"
    else:
        decision = "Approved"

    return LoanDecision(
        approval=decision,
        risk_score=risk_score,
        reasons=reasons
    )