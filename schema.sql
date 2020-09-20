CREATE TABLE books (id SERIAL PRIMARY KEY, name TEXT, lenght INTEGER, publication_date INTEGER, author TEXT);
CREATE TABLE users (id SERIAL PRIMARY KEY, username TEXT, password TEXT);
CREATE TABLE rewiews (id SERIAL PRIMARY KEY, text TEXT, book_id INTEGER REFERENCES books, time TIMESTAMP DEFAULT NOW(), score INTEGER);
