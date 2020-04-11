from typing import List, Optional, Sequence, Tuple, Type

from toydb.command import Command, Commands, CreateTable, Exit, Insert, Select
from toydb.where import Predicate, Where


def parse_schema(columns_: List[str]) -> Optional[Sequence[Tuple[str, Type]]]:
    columns = []
    for column_schema in columns_:
        column_str = column_schema.split(" ")
        if len(column_str) != 2:
            return None
        column_name, column_type_str = column_str
        column_type = {"str": str, "int": int}.get(column_type_str)
        if column_type is None:
            return None
        else:
            columns.append((column_name, column_type))
    return columns


def parse_command(command: str) -> Optional[Command]:
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
        values = args[1:]
        return Insert(values=values)
    elif c == Commands.SELECT.value:
        if len(args) == 1:
            return None
        if "where" not in args:
            columns_str = " ".join(args[1:])
            columns_ = [c.strip().replace("*", "all") for c in columns_str.split(",")]
            if len(columns_) == len(args) - 1:
                return Select(columns=columns_)
        else:
            split_index = args.index("where")
            args_ = args[1:split_index]
            columns_str = " ".join(args_)
            columns_ = [c.strip().replace("*", "all") for c in columns_str.split(",")]
            if not len(columns_) == len(args_):
                return None
            where_ = args[split_index + 1 :]
            if len(where_) != 3:
                return None
            column_name, predicate, value = where_
            predicate_ = Predicate(predicate)
            return Select(columns=columns_, where=Where(column=column_name, predicate=predicate_, value=value))
    return None
