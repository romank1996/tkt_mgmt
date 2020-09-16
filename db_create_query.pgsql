create table status(
    status_id serial PRIMARY KEY,
    Status varchar(15)
);
INSERT into status(status) VALUES('Assigned');
INSERT into status(status) VALUES('Inprogress');
INSERT into status(status) VALUES('Complete');
INSERT into status(status) VALUES('Re-opened');
INSERT into status(status) VALUES('Cancelled');

create table tickets(
    ticket_id serial primary KEY,
issue_type varchar(25),
description varchar(255),
finish_date date,
priority varchar(10),
user_id integer,
created_at timestamptz,
assigned_to integer,
assigned_at timestamptz,
status_id integer,
is_closed boolean,
FOREIGN KEY (user_id)
REFERENCES auth_user(id),
FOREIGN KEY (status_id)
REFERENCES status(id)

);

create table ticket_assign_history(
    id serial PRIMARY KEY,
    ticket_id integer,
    assigned_to integer,
    assigned_time timestamptz,
    assigned_by integer
);


create table ticket_status_history(
    id serial PRIMARY KEY,
    ticket_id integer,
    status_id integer,
    change_time timestamptz,
    modified_by integer,
    comment varchar(255)
);
create table faqs(
    id serial PRIMARY KEY,
    question varchar(255),
    answer varchar(255),
    created_at timestamptz,
    is_deleted boolean,
    sort_order integer
);