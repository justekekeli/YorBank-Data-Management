

from datetime import datetime
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
    
    
    cursor.execute("""
        INSERT INTO banking.customers
        (customer_id,advisor_id,profile_id, first_name, last_name, email, created_at)
        VALUES (%s, %s, %s, %s, %s, %s, %s) ON CONFLICT (customer_id) DO NOTHING;
    """, customer)

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
    

