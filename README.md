# toydb

An RDBMS, written as a learning project.
Inspired/stolen by [Erik Grinaker's toydb](https://github.com/erikgrinaker/toydb).
Should use Python, since that's the language I'm most familiar with.

## Project Outline

- [ ] **Networking:** Some way to communicate between db and client. Could be "networking", i.e. using a file

- [ ] **Client:** Some REPL.

- [ ] **Storage:** Some storage scheme. Key value store?

- [ ] **Data Types:** Some data types.

- [ ] **Schemas:** Compulsory singular primary keys, unique and foreign key constraints, indexes.

- [ ] **Transactions:** ?

- [ ] **Query Engine:** Query execution engine. Optimize.

- [ ] **Query Language:** SQL? Parse it?


## Thoughts

Can the REPL be a function `f: DB -> DB`, in the spirit of Functional Core, Imperative Shell, à la Gary Bernhardt?