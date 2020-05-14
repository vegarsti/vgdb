# toydb

An RDBMS, written as a learning project.
Inspired by [Erik Grinaker's toydb](https://github.com/erikgrinaker/toydb).

To try,
- make sure [poetry](https://github.com/python-poetry/poetry) is installed
- ``poetry install``
- ``poetry run python toydb/repl.py``


## Project Outline

- [x] **REPL:** Basic REPL in place, with full-screen terminal, using Blessings (full screen and location) and Python Prompt Toolkit (history and colors).

- [x] **Storage:** Some storage scheme. Stores each table in a separate file, using bytes.

- [x] **Redundancy:** Store the table when program finishes.

- [x] **Data Types:** Some data types. Str and int for now.

- [ ] **Schemas:** Compulsory singular primary keys, unique and foreign key constraints, indexes.

- [ ] **Transactions:** ?

- [ ] **Query Engine:** Query execution engine. Optimize.

- [x] **Query Language:** Support for some SQL statements: `CREATE TABLE`, `SELECT` with `WHERE`, `INSERT`.

- [x] **Query Parser:** Hand-written lexer and parser.
