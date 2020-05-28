from pathlib import Path
from typing import Dict

from vgdb import VGDB_FILE_SUFFIX
from vgdb.table import Table


def get_tables() -> Dict[str, Table]:
    tables: Dict[str, Table] = {}
    for p in Path.cwd().iterdir():
        if p.suffix == f".{VGDB_FILE_SUFFIX}":
            table_name = p.stem
            table = Table.from_file(table_name)
            tables[table_name] = table
    return tables
