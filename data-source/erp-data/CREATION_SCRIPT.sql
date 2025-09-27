-- ERP schema
create schema if not exists erp;

-- Partners (customers)
create table erp.res_partner (
    id serial primary key,
    first_name text not null,
    last_name text not null,
    email text,
    external_id text  -- link to banking.customers.customer_id
);

-- Chart of Accounts
create table erp.account (
    id serial primary key,
    code text,
    name text,
    type text
);

-- Journal entries (header)
create table erp.account_move (
    id serial primary key,
    name text,
    partner_id int references erp.res_partner(id),
    external_txn_id serial
    date date
);

-- Journal lines (detail)
create table erp.account_move_line (
    id serial primary key,
    move_id int references erp.account_move(id) on delete cascade,
    account_id int references erp.account_account(id),
    debit numeric,
    credit numeric,
    partner_id int references erp.res_partner(id)
);