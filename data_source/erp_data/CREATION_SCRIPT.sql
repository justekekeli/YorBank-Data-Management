-- ERP schema
create schema if not exists erp;

-- Partners (customers)
create table erp.res_partner (
    id varchar(40) primary key,
    first_name varchar(50) not null,
    last_name varchar(50) not null,
    email varchar(60),
    external_id varchar(40)  -- link to banking.customers.customer_id
);

-- Chart of Accounts
create table erp.account (
    id varchar(40) primary key,
    code varchar(5),
    name varchar(50),
    type varchar(50)
);

-- Journal entries (header)
create table erp.account_move (
    id varchar(40) primary key,
    name varchar(50),
    partner_receiver_id varchar(40) references erp.res_partner(id),
    partner_sender_id varchar(40) references erp.res_partner(id),
    external_txn_id varchar(40),
    date date
);

-- Journal lines (detail)
create table erp.account_move_line (
    id varchar(40) primary key,
    move_id varchar(40) references erp.account_move(id) on delete cascade,
    account_id varchar(40) references erp.account(id),
    debit numeric,
    credit numeric,
    partner_id varchar(40) references erp.res_partner(id)
);