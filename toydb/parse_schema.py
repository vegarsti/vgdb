from typing import List, Optional, Tuple, Type


def parse_schema(columns_: List[str]) -> Optional[List[Tuple[str, Type]]]:
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
