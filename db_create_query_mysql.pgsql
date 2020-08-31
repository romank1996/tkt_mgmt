create table tickets(
    ticket_id integer primary KEY,
issue_type varchar(25),
description varchar(255),
finish_date date,
priority varchar(10),
user_id integer,
created_at timestamp,
assigned_to integer,
assigned_at timestamp,
FOREIGN KEY (user_id)
REFERENCES auth_user(id)

);

create table ticket_assign_history(
    id integer PRIMARY KEY,
    ticket_id integer,
    assigned_to integer,
    assigned_time timestamp,
    assigned_by integer
);
create table status(
    status_id integer PRIMARY KEY,
    Status varchar(15)
);
create table ticket_status(
    ticket_id integer,
    status_id integer,
    change_time timestamp,
    comment varchar(255),
    primary KEY (ticket_id, status_id)
);
create table ticket_status_history(
    id integer PRIMARY KEY,
    ticket_id integer,
    status_id integer,
    change_time timestamp,
    modified_by integer,
    comment varchar(255)
);
create table faqs(
    id integer PRIMARY KEY,
    question varchar(255),
answer varchar(255),
    created_at timestamp,
    is_deleted boolean
);