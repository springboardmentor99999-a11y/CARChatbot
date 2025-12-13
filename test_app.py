from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# Example request model
class LoanRequest(BaseModel):
    name: str
    amount: float

# Root route
@app.get("/")
def read_root():
    return {"message": "Hello World"}

# Example endpoint for your CAR LOAN BOT
@app.post("/apply-loan")
def apply_loan(request: LoanRequest):
    return {"message": f"Loan request received for {request.name} of amount {request.amount}"}
