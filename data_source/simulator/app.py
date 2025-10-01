from fastapi import FastAPI
import time
from fastapi.responses import JSONResponse
import json
import os.path

from insert import *
from data_faker import generate_transaction
from get_db_connection import connect_to_source_db

app = FastAPI(title="YorBank Transaction API")


def generate_data(conn,nb_advisor,nb_customer):
    insert_profiles(conn)
    insert_erp_accounts(conn)
    advisors_ids = []
    customers = {}
    file_name = "../customer.json"
    if os.path.exists(file_name):
        with open(file_name, "r") as f:
            customers = json.load(f)
            
    while nb_advisor!=0:
        id = insert_advisor(conn)
        advisors_ids.append(id)
        nb_advisor -=1
    
    while nb_customer!=0:
        customer_id, accounts = insert_customer_and_account(conn,random.choice(advisors_ids),random.randint(1,3))
        customers[customer_id] = accounts
        if nb_customer % 2 == 0:
            insert_loan(conn,customer_id)
        nb_customer -=1
    with open("../customer.json", "w") as f:
        json.dump(customers, f)

def generate_transaction_and_moves(customers_dict):
    
    accounts = [v for sublist in customers_dict.values() for v in sublist]
    customers = list(customers_dict.keys())
    account_choice = random.choice(accounts)
    customer_choice = random.choice(customers)
    transaction = generate_transaction(account_choice)
    conn = connect_to_source_db()
    move_id = insert_account_move(conn,transaction,customer_choice)
    """
    yield (1,'4000','Commission Revenue','revenue')
    yield (2,'4100','Loan Interest Income','revenue')
    yield (3,'2100','Loan Loss Provisions','expense')
    yield (4,'1100','Accounts Receivable','asset')
    yield (5,'1000','Bank Cash','asset')

    """
    match transaction["transaction_type"]:
        case "deposit":
            insert_account_move_line(conn,move_id,[5,4],customer_choice)
        case "withdrawal":
            insert_account_move_line(conn,move_id,[5,4],customer_choice)
        case "transfer_in":
            insert_account_move_line(conn,move_id,[5,4],customer_choice)
        case "transfer_out":
            insert_account_move_line(conn,move_id,[5,4],customer_choice)
        case "card_payment":
            insert_account_move_line(conn,move_id,[5,4],customer_choice)
        case "bill_payment":
            insert_account_move_line(conn,move_id,[5,4],customer_choice)
        case "loan_disbursement":
            insert_account_move_line(conn,move_id,[5,4],customer_choice)
        case "loan_repayment":
            insert_account_move_line(conn,move_id,[5,4,2],customer_choice)
        case "savings_interest":
            insert_account_move_line(conn,move_id,[3,5],customer_choice)
        case "maintenance_fee":
            insert_account_move_line(conn,move_id,[4,1],customer_choice)

    conn.close()
    return transaction

@app.post("/seed/")
async def seed_data(n_customers:int, n_advisors:int):
    conn = connect_to_source_db()
    try:
        generate_data(conn,n_advisors,n_customers)
        return {
            "status": "success",
            "advisors_created": n_advisors,
            "customers_created": n_customers,
        }
    except Exception as e: 
        return {"status": "error", "detail": str(e)}
    finally:
        conn.close()

@app.get("/transaction_stream")
def stream_transactions():
    """Stream transactions endlessly, one per second"""
    customers_dict = {}
    with open("../customer.json", "r") as f:
        customers_dict = json.load(f)
    events = []
    for _ in range(5):
        txn = generate_transaction_and_moves(customers_dict)
        events.append(txn)
        time.sleep(0.4)  # spread them out a little (5 * 0.4s = ~2s total)
    return JSONResponse(content=events)
