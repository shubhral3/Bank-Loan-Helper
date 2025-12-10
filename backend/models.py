from typing import List, Optional
from pydantic import BaseModel, Field

class LoanApplication(BaseModel):
    name: Optional[str] = None
    age: int = Field(..., ge=18, le=70, description="Age must be between 18 and 70")
    monthly_income: float = Field(..., gt=0, description="Monthly income must be positive")
    existing_emi: float = Field(..., ge=0, description="Existing monthly obligations")
    loan_amount: float = Field(..., gt=0, description="Requested loan amount")
    tenure_years: float = Field(..., gt=0, le=30, description="Loan tenure in years")
    credit_score: int = Field(..., ge=0, le=900, description="Credit score (0-900)")
    employment_type: str = Field(..., pattern="^(salaried|self-employed|student|unemployed)$")

class LoanDecision(BaseModel):
    approval: str  # "Approved", "Rejected", "Needs Manual Review"
    risk_score: float = Field(..., ge=0, le=100, description="0 is low risk, 100 is high risk")
    reasons: List[str]