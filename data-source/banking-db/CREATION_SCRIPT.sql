-- Banking schema
create schema if not exists banking;

-- Advisors
create table banking.advisors (
    advisor_id serial primary key,
    first_name text not null,
    last_name text not null,
    email text
);

-- Profiles
create table banking.profiles (
    profile_id serial primary key,
    profile_type text,
    max_withdrawal numeric,
    max_loan numeric,
    maintenance_fee numeric,
    created_at date
);

-- Customers
create table banking.customers (
    customer_id serial primary key,
    advisor_id int references banking.advisors(advisor_id),
    profile_id int references banking.profiles(profile_id),
    first_name text not null,
    last_name text not null,
    email text unique,
    created_at date
);

-- Accounts
create table banking.accounts (
    account_id serial primary key,
    customer_id int references banking.customers(customer_id)
    account_type text check (account_type in ('normal','savings','investment')),
    balance numeric,
    created_at date
);

-- Loans
create table banking.loans (
    loan_id serial primary key,
    customer_id int references banking.customers(customer_id),
    principal numeric,
    outstanding_balance numeric,
    interest_rate numeric,
    start_date date,
    end_date date,
    status text
);
