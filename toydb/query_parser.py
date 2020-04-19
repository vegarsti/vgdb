from typing import Optional

from toydb.parse_schema import parse_schema
from toydb.statement import Commands, CreateTable, Exit, Insert, Select, Statement
from toydb.where import Predicate, Where


def parse_command(command: str) -> Optional[Statement]:
    args = command.split()
    if len(args) == 0:
        return None
    c = args[0]
    if c == Commands.EXIT.value:
        return Exit()
    elif c == Commands.CREATE.value:
        if len(args) < 4:
            return None
        if args[1] != "table":
            return None
        table_name = args[2]
        schema_str = " ".join(args[3:])
        if not (schema_str[0] == "(" and schema_str[-1] == ")"):
            return None
        columns_ = [c.strip() for c in schema_str[1:-1].split(",")]
        columns = parse_schema(columns_)
        if columns is None:
            return None
        return CreateTable(table_name=table_name, columns=columns)
    elif c == Commands.INSERT.value:
        if len(args) == 1:
            return None
        if "into" != args[1]:
            return None
        table_name = args[2]
        if "values" != args[3]:
            return None
        values_str = " ".join(args[4:])
        if not (values_str[0] == "(" and values_str[-1] == ")"):
            return None
        values = [c.strip() for c in values_str[1:-1].split(",")]
        return Insert(values=values, table_name=table_name)
    elif c == Commands.SELECT.value:
        if "from" not in args:
            return None
        from_index = args.index("from")
        table_name = args[from_index + 1]
        columns_str = " ".join(args[1:from_index])
        columns_ = [c.strip().replace("*", "all") for c in columns_str.split(",")]
        if "where" not in args:
            where = None
        else:
            where_index = args.index("where")
            where_ = args[where_index + 1 :]
            if len(where_) != 3:
                return None
            column_name, predicate, value = where_
            predicate_ = Predicate(predicate)
            where = Where(column=column_name, predicate=predicate_, value=value)
        return Select(columns=columns_, where=where, table_name=table_name)
    return None
