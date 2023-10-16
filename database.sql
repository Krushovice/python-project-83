CREATE TABLE url (
id bigint PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
name varchar(255),
created_at timestamp
);

CREATE TABLE checks (
    id bigint PRIMARY KEY REFERENCES url (id),

    h1 text,
    title text NOT NULL,
    description text NOT NULL,
    created_at timestamp
);

CREATE TABLE urls (
    id bigint PRIMARY KEY REFERENCES url (id),
    name varchar(255),
    created_at timestamp,
    response integer NOT NULL
);
