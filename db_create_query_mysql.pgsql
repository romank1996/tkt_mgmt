
create table status(
    status_id integer PRIMARY KEY AUTO_INCREMENT,
    Status varchar(15)
);
INSERT into status(status_id,status) VALUES(1,'Assigned');
INSERT into status(status_id,status) VALUES(2,'Inprogress');
INSERT into status(status_id,status) VALUES(3,'Complete');
INSERT into status(status_id,status) VALUES(4,'Re-opened');
INSERT into status(status_id,status) VALUES(5,'Cancelled');

create table tickets(
    ticket_id integer primary key AUTO_INCREMENT,
issue_type varchar(25),
description varchar(255),
finish_date date,
priority varchar(10),
user_id integer,
created_at timestamp,
assigned_to integer,
assigned_at timestamp,
status_id integer,
is_closed boolean,
FOREIGN KEY (user_id)
REFERENCES auth_user(id),
FOREIGN KEY (status_id)
REFERENCES status(status_id)

);

create table ticket_assign_history(
    id integer PRIMARY KEY AUTO_INCREMENT,
    ticket_id integer,
    assigned_to integer,
    assigned_time timestamp,
    assigned_by integer
);
create table ticket_status_history(
    id integer PRIMARY KEY AUTO_INCREMENT,
    ticket_id integer,
    status_id integer,
    change_time timestamp,
    modified_by integer,
    comment varchar(255)
);
create table faqs(
    id integer PRIMARY KEY AUTO_INCREMENT,
    question varchar(255),
answer varchar(255),
    created_at timestamp,
    is_deleted boolean,
    sort_order integer
);