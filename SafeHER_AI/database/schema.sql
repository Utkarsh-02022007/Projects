-- Add your CREATE DATABASE and CREATE TABLE statements here.
Create Database SafeHer_AI;
use SafeHer_AI;

Create Table users (
id INT auto_increment PRIMARY key,
name VARCHAR(100) not null,
email VARCHAR(150) UNIQUE not null,
phone VARCHAR(15) not null UNIQUE,
constraint chk_phone
check (phone REGEXP '^\\+?[0-9]{10,15}$'),
password_hash varchar(100) UNIQUE not null,     --here by mistake i have given unique but here unique will not there and to remove we have to remove from index. index is made of unique elelments which value is provided unique 
created_at TIMESTAMP default current_timestamp 
);

alter table users
Modify phone VARCHAR(20) not null unique,
Modify password_hash varchar(255) not null;

show tables;
Describe users

alter table users
drop index password_hash,
drop index phone_2;
create table emergency_contacts (
id INT auto_increment Primary key,
user_id INT NOT null,
contact_name varchar(100) NOT null,
phone varchar (20) not null,
constraint chk_contact_phone
CHECK (phone REGEXP '^\\+?[0-9]{10,15}$'),
relationship varchar(100),
is_primary boolean Default FALSE,
created_at timestamp default current_timestamp,

constraint fk_contact_user
foreign key (user_id)
references  users(id)
on delete cascade ,

constraint unique_user_contact
UNIQUE(user_id,phone)
);

show tables;
Describe emergency_contacts

CREATE table JOURNEY (
id int auto_increment primary key,
user_id INT NOT NULL,
start_location VARCHAR (200) Not null,
start_time TIMESTAMP Default current_timestamp,
expected_arrival timestamp null,
actual_arrival TIMESTAMP null,
status VARCHAR(20) Default 'active',

constraint fk_journey 
foreign key (user_id)
references users(id)
on DELETE cascade
);

create table location_history (
id BIGINT auto_increment primary Key,
journey_id INT NOT NULL,
latitude DECIMAL(10,7) Not null,
longitude DECIMAL(10,7) not null,
recorded_at timestamp default current_timestamp,

constraint fk_location 
foreign key (journey_id)
references journey(id)
on DELETE Cascade,

constraint chk_latitude
check ( latitude between -90 and 90),

constraint chk_longitude
check (longitude between -180 and 180)

);
create table anomaly_event(
id BIGINT auto_increment primary key,
journey_id INT not null,
event_type Varchar(100) not null,
description TEXT,
serverity VARCHAR (20)  DEFAULT 'low',
detected_at Timestamp Default current_timestamp,
status VARCHAR(30) Default 'pending',

constraint fk_anomaly_event 
foreign key (journey_id)
references journey(id)
on delete cascade
);

create table risk_assements(
id bigint auto_increment primary key,
journey_id INT not null,
anomaly_id BIGINT null,
risk_score DECIMAL(5,2) not null,
risk_level VARCHAR(20) not null,
explanation text,
assessed_at timestamp DEFAULT current_timestamp,

constraint fk_risk_journey
foreign key(journey_id)
references journey(id)
ON DELETE CASCADE,

constraint fk_risk_anomaly
foreign key (anomaly_id)
references anomaly_event(id) -- it is calling above table   
on delete set null,

CONSTRAINT chk_risk_score
check(risk_score between 0 and 100)


);
alter table risk_assements
ADD CONSTRAINT chk_risk_level
CHECK (risk_level IN ('low', 'medium', 'high'));
show tables;
describe risk_assements
-- describe anomaly_event

rename table risk_assements to risk_assessment;
rename table anomaly_event to anomaly_events;
SHOW tables;
describe anomaly_events
SHOW CREATE TABLE risk_assessment;
SHOW CREATE TABLE risk_assessment;-- 

create TABLE notifications (
id BIGINT auto_increment primary key,
user_id INT not null,
journey_id INT null,
risk_assessment_id BIGINT null,
recipient_phone varchar(20) not null,
message TEXT not null,
notification_type varchar(30) not null,
delivery_status varchar(30) default 'pending',
sent_at TIMESTAMP null,
created_at timestamp default current_timestamp,

constraint fk_notification_user
foreign key (user_id)
references users(id)
on delete CASCADE,

constraint fk_notification_journey
foreign key (journey_id)
references JOURNEY(id)
on delete set null

);
alter table notifications
add constraint fk_notification_risk
foreign key (risk_assessment_id)
references risk_assessment(id)
on delete set null
