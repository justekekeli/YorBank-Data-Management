
import time
from datetime import datetime, timedelta
from data_faker import *



def insert_advisor(conn):
    cursor = conn.cursor()

    advisor  = generate_advisor()

    cursor.execute("""
        INSERT INTO banking.advisors
        (advisor_id, first_name, last_name, email)
        VALUES (%s, %s, %s, %s) ON CONFLICT (advisor_id) DO NOTHING;
    """, advisor)

    conn.commit()
    cursor.close()
    
    print(f"[{datetime.now()}] Created advisor {advisor[1]} {advisor[2]}.")

    return advisor[0]

def insert_profiles(conn):
    cursor = conn.cursor()
    profiles = generate_profiles()
    for profile in profiles:
        cursor.execute("""
        INSERT INTO banking.profiles
        (profile_id, profile_type, max_withdrawal, max_loan, maintenance_fee,created_at )
        VALUES (%s, %s, %s, %s,%s, %s) ON CONFLICT (profile_id) DO NOTHING;
    """, profile)
        print(f"[{datetime.now()}] Created advisor {profile[1]}.")
        
    conn.commit()
    cursor.close()


def insert_customer_and_account(conn,advisor_id,profile_id):
    
    cursor = conn.cursor()
    customer = generate_customer(advisor_id,profile_id)
    erp_res_partner = generate_res_partner(customer)
    
    cursor.execute("""
        INSERT INTO banking.customers
        (customer_id,advisor_id,profile_id, first_name, last_name, email, created_at)
        VALUES (%s, %s, %s, %s, %s, %s, %s) ON CONFLICT (customer_id) DO NOTHING;
    """, customer)

    cursor.execute("""
        INSERT INTO erp.res_partner
        (id,first_name,last_name, email, external_id)
        VALUES (%s, %s, %s, %s, %s) ON CONFLICT (id) DO NOTHING;
    """, erp_res_partner)

    account = generate_account(customer[0],'normal')
    cursor.execute("""
        INSERT INTO banking.accounts
        (account_id, customer_id, account_type,balance, created_at)
        VALUES (%s, %s, %s, %s, %s) ON CONFLICT (account_id) DO NOTHING;
    """, account)
    accounts_ids= []
    accounts_ids.append(account[0])
    additionnal_account = random.randint(0,2)
    if additionnal_account > 1:
        account2 = generate_account(customer[0],'savings')
        cursor.execute("""
        INSERT INTO banking.accounts
        (account_id, customer_id, account_type,balance, created_at)
        VALUES (%s, %s, %s, %s, %s) ON CONFLICT (account_id) DO NOTHING;
    """, account2)
        accounts_ids.append(account2[0])
        if additionnal_account==2:
            account3 = generate_account(customer[0],'investment')
            cursor.execute("""
        INSERT INTO banking.accounts
        (account_id, customer_id, account_type,balance, created_at)
        VALUES (%s, %s, %s, %s, %s) ON CONFLICT (account_id) DO NOTHING;
    """, account3)
            accounts_ids.append(account3[0])

    conn.commit()
    cursor.close()
    
    print(f"[{datetime.now()}] Created customer {customer[1]} {customer[2]} ")

    return customer[0],accounts_ids
    

def insert_loan(conn,customer_id):
    
    cursor = conn.cursor()
    loan = generate_loan(customer_id)
    cursor.execute("""
        INSERT INTO banking.loans
        (loan_id,customer_id, principal, outstanding_balance, interest_rate,start_date,end_date,status)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s) ON CONFLICT (loan_id) DO NOTHING;
    """, loan)
    conn.commit()
    cursor.close()
    

def insert_erp_accounts(conn):
    cursor = conn.cursor()
    erp_accounts = generate_erp_accounts()
    for erp_account in erp_accounts:
        cursor.execute("""
        INSERT INTO erp.account
        (id, code, name, type )
        VALUES (%s, %s, %s, %s) ON CONFLICT (id) DO NOTHING;
    """, erp_account)
        print(f"[{datetime.now()}] Created advisor {erp_account[1]}.")
        
    conn.commit()
    cursor.close()
    

def insert_account_move(conn,transaction,account_id):
    
    cursor = conn.cursor()
    account_move = generate_account_move(transaction,account_id)
    cursor.execute("""
        INSERT INTO erp.account_move
        (id,name,partner_id,external_txn_id,date)
        VALUES (%s, %s, %s, %s, %s) ON CONFLICT (id) DO NOTHING;
    """, account_move)
    conn.commit()
    cursor.close()
    
    return account_move[0]

def insert_account_move_line(conn,move_id,account_ids,partner_id):
    
    cursor = conn.cursor()
    for account_id in account_ids:
        account_move_line = generate_account_move_line(move_id,account_id,partner_id)
        cursor.execute("""
        INSERT INTO erp.account_move_line
        (id,move_id,account_id,debit,credit,partner_id)
        VALUES (%s, %s, %s, %s, %s, %s) ON CONFLICT (id) DO NOTHING;
    """, account_move_line)
    conn.commit()
    cursor.close()
    


