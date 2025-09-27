
from faker import Faker
from datetime import datetime, timedelta
import random

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

def generate_profile():
    return (
        fake.uuid4(),
        random.choice(['standard','premium','golden']),
        round(random.uniform(100, 10000), 2),
        round(random.uniform(100, 100000), 2),
        round(random.uniform(4, 10), 2),
        datetime.now().date()
    )

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


def generate_account(customer_id):
    return (
        fake.uuid4(),
        customer_id,
        random.choice(['normal','savings','investment']),
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
