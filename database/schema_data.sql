-- Add optional sample INSERT statements here.


-- DATA INSERTION 


USE SafeHer_AI;
INSERT INTO users (
    name,
    email,
    phone,
    password_hash
)
VALUES (
    'Rahul Sharma',
    'rahul@example.com',
    '9876543210',
    'sample_hash_123'
);
insert into emergency_contacts (
user_id,
contact_name,
phone,
relationship,
is_primary
)
VALUES (
1,
"rohit",
"8930930293",
"Father",
TRUE
);
describe JOURNEY;

insert into JOURNEY (
user_id,
start_location,
expected_arrival,
status
)
values(
1,
"HOME",
'2026-11-11 19:30:00',
"active"
);

INSERT INTO location_history (
    journey_id,
    latitude,
    longitude
)
VALUES
    (1, 28.4595000, 77.0266000),
    (1, 28.4600000, 77.0270000),
    (1, 28.4610000, 77.0280000);
select* from location_history;
