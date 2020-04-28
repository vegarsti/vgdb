from pathlib import Path
from typing import Dict

from toydb.table import Table


def get_tables() -> Dict[str, Table]:
    p = Path.cwd()
    d = {}
    for i in p.iterdir():
        if i.suffix == ".db":
            table_name = i.stem
            if table_name == "tbl":
                continue
            table = Table.from_file(table_name)
            d[table_name] = table
    return d
