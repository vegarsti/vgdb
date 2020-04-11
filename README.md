# toydb

An RDBMS, written as a learning project.
Inspired by [Erik Grinaker's toydb](https://github.com/erikgrinaker/toydb).

To try,
- ``poetry install``
- ``poetry run python toydb/repl.py``

![toydb](https://user-images.githubusercontent.com/5699893/79045497-bfa57e80-7c0b-11ea-8c71-34d39fc9b7a7.gif)


## Project Outline

- [ ] **Networking:** Some way to communicate between db and client. Could be "networking", i.e. using a file

- [x] **REPL:** Basic REPL in place, with full-screen terminal, using Blessings (full screen and location) and Python Prompt Toolkit (history and colors).

- [ ] **Storage:** Some storage scheme. Just Python dataclasses for now.

- [ ] **Redundancy:** Store the table when program finishes.

- [ ] **Data Types:** Some data types. Str and int for now.

- [ ] **Schemas:** Compulsory singular primary keys, unique and foreign key constraints, indexes.

- [ ] **Transactions:** ?

- [ ] **Query Engine:** Query execution engine. Optimize.

- [x] **Query Language:** Insert, select

- [x] **Query Parser:** Yes, ish


## Thoughts

- Can the REPL be a function `f: DB -> DB`, in the spirit of Functional Core, Imperative Shell, à la Gary Bernhardt?
- REPL with color and history in place. Fun!
- Insert and select for str and int to be supported soon.
