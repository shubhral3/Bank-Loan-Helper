# 🏦 Bank Loan Helper

A full-stack financial demo application that automates loan underwriting using a rule-based risk engine. This project demonstrates a decoupled client-server architecture with a **FastAPI** backend for scoring logic and a **Streamlit** frontend for the user interface.

## 🚀 Key Features

* **Intelligent Risk Scoring:** Calculates a 0-100 risk score based on Credit Score, Debt-to-Income (DTI) ratio, and loan tenure.
* **Real-time Decisioning:** Instant "Approved", "Rejected", or "Manual Review" feedback.
* **Explainable AI:** Returns specific, human-readable reasons for every decision (e.g., "EMI exceeds 40% of income").
* **Data Validation:** Strict input validation using Pydantic models to ensure data integrity.

## 🛠️ Tech Stack

* **Backend:** Python, FastAPI, Uvicorn
* **Frontend:** Streamlit
* **Validation:** Pydantic
* **Client-Server:** HTTP Requests (REST API)

## 📂 Project Structure

```text
bank-loan-helper/
│
├── backend/
│   ├── main.py           # FastAPI entry point
│   ├── models.py         # Pydantic data schemas
│   └── scoring.py        # Business logic & risk rules
│
├── frontend/
│   └── app.py            # Streamlit dashboard
│
├── requirements.txt      # Python dependencies
└── README.md             # Documentation
