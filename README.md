# vgdb

![test](https://github.com/vegarsti/vgdb/workflows/test/badge.svg)

A relational database management system (RDBMS) in Python.

Inspirations:
- [Erik Grinaker's toydb in Rust](https://github.com/erikgrinaker/toydb)
- [Phil Eaton's gosql in Go](https://notes.eatonphil.com/database-basics.html)
- [cstack's sqlite clone in C](https://cstack.github.io/db_tutorial/)

## Instructions
- make sure [poetry](https://github.com/python-poetry/poetry) and Python >= 3.6 is installed.
- Run `poetry install` to install
- Run `poetry run vgdb` to launch a command line REPL
- Run `poetry run vgdb-bench` to run a benchmark where some lines are inserted and selected from


## Project Outline

- [x] **REPL** 

- [x] **Storage:** Some storage scheme. Stores each table in a separate file.

- [x] **Redundancy:** Persist on write.

- [x] **Data Types:** `TEXT` and `INT` for now.

- [ ] **Schemas** Compulsory singular primary keys, unique and foreign key constraints, indexes.

- [ ] **Transactions**

- [ ] **Query Engine:** Query execution engine.

- [x] **Query Language:** Support for SQL statements: 
    - `CREATE TABLE` with `TEXT` and `INT`, no index
    - `INSERT`
    - `SELECT` with `WHERE`, `ORDER BY` and `LIMIT` (with `OFFSET`)

- [x] **Query Parser:** Hand-written lexer and parser.
