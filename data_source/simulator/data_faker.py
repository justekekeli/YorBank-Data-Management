
from faker import Faker
from datetime import datetime, timedelta,timezone
import random
import time

fake = Faker()

#############################################################
#                            Banking DB                    #
#############################################################

def generate_advisor():
    return (
        fake.uuid4(),
        fake.first_name(),
        fake.last_name(),
        fake.email()
)

def generate_profiles():
    yield (1,"standard",round(random.uniform(500, 1000), 2),round(random.uniform(1000, 10000), 2),round(random.uniform(4, 10), 2),datetime.now().date())
    yield (2,"premium",round(random.uniform(1000, 10000), 2),round(random.uniform(10000, 100000), 2),round(random.uniform(15, 30), 2),datetime.now().date())
    yield (3,"golden",round(random.uniform(20000, 1000000), 2),round(random.uniform(10000, 10000000), 2),round(random.uniform(35, 50), 2),datetime.now().date())
    

def generate_customer(advisor_id,profile_id):
    return (
        fake.uuid4(),
        advisor_id,
        profile_id,
        fake.first_name(),
        fake.last_name(),
        fake.email(),
        datetime.now().date()
    )


def generate_account(customer_id,account_type):
    return (
        fake.uuid4(),
        customer_id,
        account_type,
        #random.choice(['normal','savings','investment']),
        round(random.uniform(-1000, 10000), 2),
        datetime.now().date()
    )

def generate_loan(customer_id):
    return (
        fake.uuid4(),
        customer_id,
        random.randrange(3000, 500000),
        random.randrange(0, 500000),
        round(random.uniform(0.02, 0.08),2),
        datetime.now().date(),
        datetime.now() + timedelta(weeks=random.randrange(52, 156)) ,
        'active'
    )

#############################################################
#                        Transaction API                    #
#############################################################

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

def generate_transaction(account_id) -> dict:
    """Generate a random transaction"""
    txn_type = random.choice(transaction_types)
    amount = round(random.uniform(10, 1000), 2)
    current_status = random.choice(status)

    # Outflows should be negative
    if txn_type in ["withdrawal", "transfer_out", "card_payment", "bill_payment",
                    "loan_repayment", "maintenance_fee"] and current_status !="cancelled":
        amount = -amount

    transaction = {
        "transaction_id": int(time.time() * 1000),
        "account_id": account_id,
        "amount": amount,
        "balance_after": round(random.uniform(-1000, 10000), 2),
        "transaction_type": txn_type,
        "description": descriptions[txn_type],
        "status": current_status,
        "occurred_at": str(datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"))
    }
    return transaction

#############################################################
#                        ERP Data                           #
#############################################################

def generate_res_partner(customer):
    return (
        customer[0],
        customer[1],
        customer[2],
        fake.email(),
        customer[0]
    )

def generate_erp_accounts():
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