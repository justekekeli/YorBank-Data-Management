from fastapi import FastAPI
import random
import time
import uuid
from fastapi.responses import StreamingResponse
from faker import Faker
import json

app = FastAPI(title="YorBank Transaction API")
fake = Faker()

# Possible values
transaction_types = [
    "deposit", "withdrawal", "transfer_in", "transfer_out",
    "card_payment", "bill_payment", "loan_disbursement",
    "loan_repayment", "savings_interest", "maintenance_fee"
]

descriptions = {
    "deposit": "Salary Deposit",
    "withdrawal": "ATM Cash Withdrawal",
    "transfer_in": "Incoming Transfer",
    "transfer_out": "Outgoing Transfer",
    "card_payment": "Card Payment at Merchant",
    "bill_payment": "Utility Bill Payment",
    "loan_disbursement": "Loan Granted",
    "loan_repayment": "Loan Repayment",
    "savings_interest": "Interest Credited",
    "maintenance_fee": "Account Maintenance Fee"
}
status = ["completed","cancelled","initiated"]

def generate_transaction() -> dict:
    """Generate a random transaction"""
    txn_type = random.choice(transaction_types)
    amount = round(random.uniform(10, 1000), 2)
    current_status = random.choice(status)

    # Outflows should be negative
    if txn_type in ["withdrawal", "transfer_out", "card_payment", "bill_payment",
                    "loan_repayment", "maintenance_fee"] and current_status !="cancelled":
        amount = -amount

    transaction = {
        "transaction_id": str(uuid.uuid4()),
        "account_id": random.randint(1, 30),
        "amount": amount,
        "balance_after": round(random.uniform(-1000, 10000), 2),
        "transaction_type": txn_type,
        "description": descriptions[txn_type],
        "status": current_status,
        "occurred_at": time.strftime("%Y-%m-%dT%H:%M:%SZ")
    }
    return transaction

def generate_res_partner(customer):
    return (
        fake.uuid4(),
        customer[1],
        customer[2],
        fake.email(),
        customer[0]
    )

def generate_account():
    yield (1,'4000','Commission Revenue','revenue')
    yield (2,'4100','Loan Interest Income','revenue')
    yield (3,'2100','Loan Loss Provisions','expense')
    yield (4,'1100','Accounts Receivable','asset')
    yield (5,'1000','Bank Cash','asset')

def generate_account_move(transaction,customer_id):
    return (
        fake.uuid4(),
        transaction["description"],
        customer_id,
        transaction["transaction_id"],
        transaction["occurred_at"]
    )

def generate_account_move_line(move_id,account_id,partner_id):
    return (
        fake.uuid4(),
        move_id,
        account_id,
        round(random.uniform(0, 1000), 2),
        round(random.uniform(10, 1000), 2),
        partner_id
    )

@app.get("/stream")
def stream_transactions():
    """Stream transactions endlessly, one per second"""

    def event_stream():
        while True:
            txn = generate_transaction()
            yield json.dumps(txn)
            time.sleep(1)

    return StreamingResponse(event_stream(), media_type="application/json")
