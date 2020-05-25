import sys
import time
from pathlib import Path
from typing import List, Union

from vgdb.evaluator import Evaluator
from vgdb.get_tables import get_tables
from vgdb.lexer import Lexer
from vgdb.parser import Parser


def run_command(evaluator: Evaluator, sql_string: str) -> Union[str, List[List[Union[str, int]]]]:
    lexer = Lexer(program=sql_string)
    parser = Parser(lexer=lexer)
    command = parser.parse()
    return evaluator.handle_command(command)


def time_command(sql_string: str) -> None:
    evaluator = Evaluator(tables=get_tables())
    start = time.time()
    run_command(evaluator, sql_string)
    elapsed = time.time() - start
    print(f"{sql_string:<70}{elapsed:>10.5f} seconds")


def delete_db(db_name: str) -> None:
    (Path(__file__).parent.parent / f"{db_name}.db").unlink()


def run_insert_benchmark(db_name: str) -> None:
    word_file = "/usr/share/dict/words"
    with open(word_file, "rb") as f:
        words = [s.decode("utf-8") for s in (f.read().splitlines())]
    n = len(words)
    evaluator = Evaluator(tables={})
    create_command = f"CREATE TABLE {db_name} (number int, words text)"
    print(run_command(evaluator, create_command))
    insert_printout = f"Inserting {n} records..."
    print(f"{insert_printout:<70}", end="")
    sys.stdout.flush()
    evaluator = Evaluator(tables=get_tables())
    start = time.time()
    for i in range(n):
        command = f"INSERT INTO {db_name} VALUES ({i}, '{words[i]}')"
        run_command(evaluator, command)
    elapsed = time.time() - start
    print(f"{elapsed:>10.5f} seconds")
    sys.exit()


def run_select_benchmark(db_name: str) -> None:
    time_command(f"SELECT * FROM {db_name}")
    time_command(f"SELECT * FROM {db_name} LIMIT 1")
    time_command(f"SELECT * FROM {db_name} WHERE words LIKE 'a%'")
    time_command(f"SELECT * FROM {db_name} WHERE words LIKE 'a%' order by number")


def insert() -> None:
    insert_db = "bench_insert"
    try:
        run_insert_benchmark(insert_db)
    except Exception as e:
        print(e)
    finally:
        delete_db(insert_db)


def select() -> None:
    select_db = "bench_select"
    run_select_benchmark(select_db)


def main() -> None:
    insert()
    select()


if __name__ == "__main__":
    main()
