# vgdb

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
![lint_test_build](https://github.com/vegarsti/vgdb/workflows/lint_test_build/badge.svg)

A relational database management system (RDBMS) in Python.

![demo](https://user-images.githubusercontent.com/5699893/83227329-3549b780-a184-11ea-819a-afa4c61d5cb2.gif)

Inspirations:
- [Erik Grinaker's toydb in Rust](https://github.com/erikgrinaker/toydb)
- [Phil Eaton's gosql in Go](https://notes.eatonphil.com/database-basics.html)
- [cstack's sqlite clone in C](https://cstack.github.io/db_tutorial/)

## Instructions
You should not actually use this, you should use sqlite instead! But if you want to try it,

- make sure [poetry](https://github.com/python-poetry/poetry) and Python >= 3.7 is installed.
- Run `poetry install` to install
- Run `poetry run vgdb` to launch a command line REPL (or `poetry shell` and then `vgdb`)
- Run `poetry run vgdb-bench` to run a benchmark of `INSERT` and `SELECT` performance compared to sqlite (warning: vgdb is crushed)


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
