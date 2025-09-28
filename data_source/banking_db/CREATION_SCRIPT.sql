-- Banking schema
create schema if not exists banking;

-- Advisors
create table banking.advisors (
    advisor_id varchar(40) primary key,
    first_name varchar(50) not null,
    last_name varchar(50) not null,
    email varchar(60) not null
);

-- Profiles
create table banking.profiles (
    profile_id varchar(40) primary key,
    profile_type varchar(10) not null,
    max_withdrawal numeric not null,
    max_loan numeric not null,
    maintenance_fee numeric not null,
    created_at timestamp(3)
);

-- Customers
create table banking.customers (
    customer_id varchar(40) primary key,
    advisor_id varchar(40) references banking.advisors(advisor_id),
    profile_id varchar(40) references banking.profiles(profile_id),
    first_name varchar(50) not null,
    last_name varchar(50) not null,
    email varchar(60) not null,
    created_at timestamp not null
);

-- Accounts
create table banking.accounts (
    account_id varchar(40) primary key,
    customer_id varchar(40) references banking.customers(customer_id),
    account_type varchar(10) check (account_type in ('normal','savings','investment')),
    balance numeric not null,
    created_at timestamp(3) not null
);

-- Loans
create table banking.loans (
    loan_id varchar(40) primary key,
    customer_id varchar(40) references banking.customers(customer_id),
    principal numeric not null,
    outstanding_balance numeric not null,
    interest_rate numeric not null,
    start_date date not null,
    end_date date,
    status varchar(10) not null
);
