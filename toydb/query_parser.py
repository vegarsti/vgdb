import re
from typing import List, Match, Optional, Union

from toydb.parse_schema import parse_schema
from toydb.statement import Commands, CreateTable, Exit, Insert, Select, Statement
from toydb.where import Predicate, Where


def parse_create_table(command: str) -> Optional[Statement]:
    args = command.split()
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


def parse_insert(command: str) -> Optional[Statement]:
    args = command.split()
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
    parsed_values: List[Union[int, str]] = []
    for value in values:
        if value.startswith("'"):
            if not value.endswith("'"):
                return None
            parsed_values.append(value[1:-1])
        else:
            try:
                int(value)
            except ValueError:
                return None
            parsed_values.append(int(value))
    return Insert(values=parsed_values, table_name=table_name)


def parse_command(command: str) -> Optional[Statement]:
    args = command.split()
    if len(args) == 0:
        return None
    c = args[0]
    if c == Commands.EXIT.value:
        return Exit()
    elif c == Commands.CREATE.value:
        return parse_create_table(command)
    elif c == Commands.INSERT.value:
        return parse_insert(command)
    elif c == Commands.SELECT.value:
        return parse_select(command)
    return None


def parse_select(command: str) -> Optional[Statement]:
    select_pattern = r"(select|SELECT) (((\w+)+(, \w+)*)|\*) from (\w+)( where ((\w+) = (\w+)))*"
    select_match = re.search(pattern=select_pattern, string=command)
    if select_match is None:
        return None
    column_start, column_end = select_match.regs[2]
    columns__ = command[column_start:column_end]
    columns___ = [c.strip().replace("*", "all") for c in columns__.split(",")]
    table_start, table_end = select_match.regs[6]
    table_name = command[table_start:table_end]
    where_start, where_end = select_match.regs[7]
    where_ = command[where_start:where_end]
    if where_ != "":
        where = parse_where(command, select_match)
    return Select(columns=columns___, where=where if where_ != "" else None, table_name=table_name)


def parse_where(command: str, select_match: Match[str]) -> Where:
    column_start, column_end = select_match.regs[9]
    column_name = command[column_start:column_end]
    predicate = "="
    value_start, value_end = select_match.regs[10]
    value = command[value_start:value_end]
    where = Where(column=column_name, predicate=Predicate(predicate), value=value)
    return where
