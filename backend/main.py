from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .models import LoanApplication, LoanDecision
from .scoring import score_loan

app = FastAPI(title="Magic Bank Loan Engine")

# Allow Streamlit to talk to FastAPI (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Magic Bank Loan API is running."}

@app.post("/score_loan", response_model=LoanDecision)
def score_loan_endpoint(application: LoanApplication):
    try:
        decision = score_loan(application)
        return decision
    except Exception as e:
        # In a real app, log the error here
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    # Run on port 8000
    uvicorn.run(app, host="0.0.0.0", port=8000)