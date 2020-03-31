# toydb

An RDBMS, written as a learning project.
Inspired by [Erik Grinaker's toydb](https://github.com/erikgrinaker/toydb).

To try,
- Run ``poetry install``
- Run ``poetry run python toydb/repl.py``

[![asciicast](https://asciinema.org/a/l5KyIRseeHWgctUb43a0VkPtI.svg)](https://asciinema.org/a/l5KyIRseeHWgctUb43a0VkPtI)

## Project Outline

- [ ] **Networking:** Some way to communicate between db and client. Could be "networking", i.e. using a file

- [x] **REPL:** Basic REPL in place, with full-screen terminal, using Blessings.

- [ ] **Storage:** Some storage scheme. Key value store?

- [ ] **Redundancy:** Store the table when program finishes.

- [ ] **Data Types:** Some data types.

- [ ] **Schemas:** Compulsory singular primary keys, unique and foreign key constraints, indexes.

- [ ] **Transactions:** ?

- [ ] **Query Engine:** Query execution engine. Optimize.

- [x] **Query Language:** Insert, select, delete key value pairs

- [x] **Query Parser:** Yes


## Thoughts

Can the REPL be a function `f: DB -> DB`, in the spirit of Functional Core, Imperative Shell, à la Gary Bernhardt?

Basic REPL in place.