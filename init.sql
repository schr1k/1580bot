CREATE TABLE users (
    id SERIAL,
    tg VARCHAR,
    username VARCHAR,
    class VARCHAR,
    building VARCHAR
);

CREATE TABLE staff (
    id SERIAL,
    tg VARCHAR,
    username VARCHAR,
    role VARCHAR
);