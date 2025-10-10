import random
import uuid
from datetime import date, timedelta
from faker import Faker

fake = Faker()

# ========== CONFIG ==========
OUTPUT_FILE = "../dbs_models/bigquery_gold/INSERT_FAKE_DATA.sql"
START_DATE = date.today() - timedelta(days=180)
END_DATE = date.today()

# Rows per table per day (realistic relative scale)
ROWS_PER_DAY = {
    "transaction_mart": 10,
    "customer_overdraft_mart": 20,
    "customer_withdrawal_reached_mart": 15,
    "customer_mart": 4
}

# ========== HELPERS ==========
def daterange(start_date, end_date):
    for n in range((end_date - start_date).days + 1):
        yield start_date + timedelta(days=n)

# ========== TABLE 1: transaction_mart ==========
def generate_transaction_mart():
    rows = []
    transaction_types = [
    "deposit", "withdrawal", "transfer_in", "transfer_out",
    "card_payment", "bill_payment", "loan_disbursement",
    "loan_repayment", "savings_interest", "maintenance_fee"
]
    status_list = ["completed","cancelled","initiated"]

    for current_date in daterange(START_DATE, END_DATE):
        for _ in range(ROWS_PER_DAY["transaction_mart"]):
            ttype = random.choice(transaction_types)
            status = random.choice(status_list)
            revenue = round(random.uniform(1000, 50000), 2)
            nb_transaction = random.randint(10, 500)
            total_amount = round(revenue * random.uniform(0.9, 1.1), 2)

            rows.append(
                f"('{current_date}', '{ttype}', '{status}', {revenue}, {nb_transaction}, {total_amount})"
            )

    values = ",\n".join(rows)
    return f"""INSERT INTO `gold.transaction_mart`
(reference_date, transaction_type, status, revenue, nb_transaction, total_amount)
VALUES
{values};
"""

# ========== TABLE 2: customer_overdraft_mart ==========
def generate_customer_overdraft_mart():
    rows = []
    for current_date in daterange(START_DATE, END_DATE):
        for _ in range(ROWS_PER_DAY["customer_overdraft_mart"]):
            id_ = str(uuid.uuid4())
            customer_id = str(uuid.uuid4())[:8]
            first_name = fake.first_name()
            last_name = fake.last_name()
            customer_email = fake.email()
            advisor_email = fake.email()

            rows.append(
                f"('{id_}', '{current_date}', '{customer_id}', '{first_name}', '{last_name}', '{customer_email}', '{advisor_email}')"
            )

    values = ",\n".join(rows)
    return f"""INSERT INTO `gold.customer_overdraft_mart`
(id, reference_date, customer_id, customer_first_name, customer_last_name, customer_email, advisor_email)
VALUES
{values};
"""

# ========== TABLE 3: customer_withdrawal_reached_mart ==========
def generate_customer_withdrawal_reached_mart():
    rows = []
    for current_date in daterange(START_DATE, END_DATE):
        for _ in range(ROWS_PER_DAY["customer_withdrawal_reached_mart"]):
            cust_email = fake.email()
            cust_last = fake.last_name()
            adv_first = fake.first_name()
            adv_last = fake.last_name()
            adv_email = fake.email()
            cust_first = fake.first_name()
            profile_id = str(uuid.uuid4())[:8]
            max_withdrawal = round(random.uniform(1000, 10000), 2)
            customer_id = str(uuid.uuid4())[:8]

            rows.append(
                f"('{current_date}', '{cust_email}', '{cust_last}', '{adv_first}', '{adv_last}', '{adv_email}', '{cust_first}', '{profile_id}', {max_withdrawal}, '{customer_id}')"
            )

    values = ",\n".join(rows)
    return f"""INSERT INTO `gold.customer_withdrawal_reached_mart`
(reference_date, customer_email, customer_last_name, advisor_first_name, advisor_last_name, advisor_email, customer_first_name, profile_id, max_withdrawal, customer_id)
VALUES
{values};
"""

# ========== TABLE 4: customer_mart ==========
def generate_customer_mart():
    rows = []
    profile_types = ["standard", "premium", "gold", "vip"]

    for current_date in daterange(START_DATE, END_DATE):
        for _ in range(ROWS_PER_DAY["customer_mart"]):
            adv_email = fake.email()
            profile_type = random.choice(profile_types)
            total_number = random.randint(10, 1000)

            rows.append(f"('{current_date}', '{adv_email}', '{profile_type}', {total_number})")

    values = ",\n".join(rows)
    return f"""INSERT INTO `gold.customer_mart`
(reference_date, advisor_email, profile_type, total_number)
VALUES
{values};
"""

# ========== MAIN ==========
def main():
    sql_content = ""
    sql_content += "-- Fake data generation for transaction_mart\n" + generate_transaction_mart() + "\n\n"
    sql_content += "-- Fake data generation for customer_overdraft_mart\n" + generate_customer_overdraft_mart() + "\n\n"
    sql_content += "-- Fake data generation for customer_withdrawal_reached_mart\n" + generate_customer_withdrawal_reached_mart() + "\n\n"
    sql_content += "-- Fake data generation for customer_mart\n" + generate_customer_mart() + "\n"

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(sql_content)

    print(f"---- Fake daily insert SQL file generated: {OUTPUT_FILE}")
    print(f"   - transaction_mart: {ROWS_PER_DAY['transaction_mart']} rows/day")
    print(f"   - customer_overdraft_mart: {ROWS_PER_DAY['customer_overdraft_mart']} rows/day")
    print(f"   - customer_withdrawal_reached_mart: {ROWS_PER_DAY['customer_withdrawal_reached_mart']} rows/day")
    print(f"   - customer_mart: {ROWS_PER_DAY['customer_mart']} rows/day")

if __name__ == "__main__":
    main()
