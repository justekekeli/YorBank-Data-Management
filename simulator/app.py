from fastapi import FastAPI
from datetime import datetime, timedelta
import calendar
import time
from fastapi.responses import JSONResponse
import json
import os.path

from insert import *
from data_faker import generate_transaction
from get_db_connection import connect_to_source_db

app = FastAPI(title="YorBank Transaction API")


def generate_data(conn,nb_advisor,nb_customer,date_choice=None):
    insert_profiles(conn)
    advisors_ids = []
    customers = {}
    file_name = "customer.json"
    if os.path.exists(file_name):
        with open(file_name, "r") as f:
            customers = json.load(f)
            
    while nb_advisor!=0:
        id = insert_advisor(conn)
        advisors_ids.append(id)
        nb_advisor -=1
    
    while nb_customer!=0:
        customer_id, accounts = insert_customer_and_account(conn,random.choice(advisors_ids),random.randint(1,3),date_choice)
        customers[customer_id] = accounts
        if nb_customer % 2 == 0:
            insert_loan(conn,customer_id)
        nb_customer -=1
    with open("customer.json", "w") as f:
        json.dump(customers, f)

def create_transaction(customers_dict,date_choice=None):
    
    accounts = [v for sublist in customers_dict.values() for v in sublist]
    #customers = list(customers_dict.keys())
    sender_account_choice = random.choice(accounts)
    receiver_account_choice = random.choice(accounts)
    transaction = generate_transaction(sender_account_choice,receiver_account_choice,date_choice)
   
    return transaction

def init_dates():
    today = datetime.today()

    # Get the date 3 months ago safely
    month = today.month - 3
    year = today.year
    if month <= 0:
        month += 12
        year -= 1

    # Handle days overflow
    day = min(today.day, calendar.monthrange(year, month)[1])
    start_date = datetime(year, month, day)

    # Generate list of daily datetimes
    date_list = [
        start_date + timedelta(days=i)
        for i in range((today - start_date).days + 1)]
    
    return date_list


    


@app.post("/customer_details_daily/")
def seed_data(n_customers:int, n_advisors:int):
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
    with open("customer.json", "r") as f:
        customers_dict = json.load(f)
    events = []
    for _ in range(5):
        txn = create_transaction(customers_dict)
        events.append(txn)
        time.sleep(0.4)  # spread them out a little (5 * 0.4s = ~2s total)
    return JSONResponse(content=events)
