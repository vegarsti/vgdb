# vgdb

An RDBMS, written as a learning project.

Inspirations:
- [Erik Grinaker's toydb](https://github.com/erikgrinaker/toydb)
- [Phil Eaton's gosql](https://notes.eatonphil.com/database-basics.html)
- [sqlite clone in C](https://cstack.github.io/db_tutorial/)

To try,
- make sure [poetry](https://github.com/python-poetry/poetry) and Python >= 3.6 is installed.
- ``poetry install``
- ``poetry run repl``


## Project Outline

- [x] **REPL** 

- [x] **Storage:** Some storage scheme. Stores each table in a separate file.

- [x] **Redundancy:** Persist on write.

- [x] **Data Types:** `TEXT` and `INT` for now.

- [ ] **Schemas** Compulsory singular primary keys, unique and foreign key constraints, indexes.

- [ ] **Transactions**

- [ ] **Query Engine:** Query execution engine.

- [x] **Query Language:** Support for SQL statements: `CREATE TABLE` with `TEXT` and `INT`, no index. `INSERT`. `SELECT` with `WHERE`, `ORDER BY`, `LIMIT` (with `OFFSET`).

- [x] **Query Parser:** Hand-written lexer and parser.
