from typing import List, Union


def copy_nested_list(lst: List[List[str]]) -> List[List[str]]:
    """Return a copy of list l to one level of nesting"""
    return [list(i) for i in lst]


def column_widths(table: List[List[str]]) -> List[int]:
    """Get the maximum size for each column in table"""
    return [max(map(len, col)) for col in zip(*table)]


def align_table(table: List[List[str]]) -> List[List[str]]:
    """Return table justified according to align"""
    widths = column_widths(table)
    new_table = copy_nested_list(table)
    align = "<"
    for row in new_table:
        for cell_num, cell in enumerate(row):
            row[cell_num] = "{:{align}{width}}".format(cell, align=align, width=widths[cell_num])
    return new_table


def stringify_table(table: List[List[Union[int, str]]]) -> List[List[str]]:
    new_table = []
    for row in table:
        new_row = [str(i) for i in row]
        new_table.append(new_row)
    return new_table


def print_selection(table: List[List[Union[int, str]]]) -> None:
    for row in align_table(stringify_table(table)):
        print(" ".join(row))
