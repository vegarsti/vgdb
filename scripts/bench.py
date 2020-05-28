import argparse
import sqlite3
import sys
import time
from pathlib import Path
from typing import List, Union

from vgdb import VGDB_FILE_SUFFIX
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


def time_command_sqlite(c: sqlite3.Cursor, sql_string: str) -> None:
    start = time.time()
    results = c.execute(sql_string)
    list(results)
    elapsed = time.time() - start
    print(f"{sql_string:<70}{elapsed:>10.5f} seconds")


def delete_db(db_name: str) -> None:
    (Path(__file__).parent.parent / db_name).unlink()


def create_table(table: str) -> None:
    evaluator = Evaluator(tables={})
    create_command = f"CREATE TABLE {table} (number int, words text)"
    print(run_command(evaluator, create_command))


def read_words() -> List[str]:
    word_file = "/usr/share/dict/words"
    with open(word_file, "rb") as f:
        words = [s.decode("utf-8") for s in (f.read().splitlines())]
    return words


def insert_words(evaluator: Evaluator, table: str, words: List[str]) -> None:
    for i, word in enumerate(words):
        command = f"INSERT INTO {table} VALUES ({i}, '{word}')"
        run_command(evaluator, command)


def run_insert_benchmark(table: str) -> None:
    create_table(table)
    evaluator = Evaluator(tables=get_tables())
    words = read_words()
    n = len(words)
    insert_printout = f"Inserting {n} records..."
    print(f"{insert_printout:<70}", end="")
    sys.stdout.flush()
    start = time.time()
    insert_words(evaluator, table, words)
    elapsed = time.time() - start
    print(f"{elapsed:>10.5f} seconds")


def run_select_benchmark(table: str) -> None:
    time_command(f"SELECT * FROM {table}")
    time_command(f"SELECT * FROM {table} LIMIT 1")
    time_command(f"SELECT * FROM {table} WHERE words LIKE 'a%'")
    time_command(f"SELECT * FROM {table} WHERE words LIKE 'a%' ORDER BY number")


def get_words() -> List[str]:
    word_file = "/usr/share/dict/words"
    with open(word_file, "rb") as f:
        words = [s.decode("utf-8") for s in (f.read().splitlines())]
    return words


def run_insert_benchmark_sqlite(c: sqlite3.Cursor, table: str) -> None:
    words = get_words()
    n = len(words)
    create_command = f"CREATE TABLE {table} (number int, words text)"
    c.execute(create_command)
    insert_printout = f"Inserting {n} records..."
    print(f"{insert_printout:<70}", end="")
    sys.stdout.flush()
    start = time.time()
    for i in range(n):
        command = f"INSERT INTO {table} VALUES ({i}, '{words[i]}')"
        c.execute(command)
    elapsed = time.time() - start
    print(f"{elapsed:>10.5f} seconds")


def run_select_benchmark_sqlite(c: sqlite3.Cursor, table: str) -> None:
    time_command_sqlite(c, f"SELECT * FROM {table}")
    time_command_sqlite(c, f"SELECT * FROM {table} LIMIT 1")
    time_command_sqlite(c, f"SELECT * FROM {table} WHERE words LIKE 'a%'")
    time_command_sqlite(c, f"SELECT * FROM {table} WHERE words LIKE 'a%' ORDER BY number")


def sqlite_bench() -> None:
    db_name = "sqlite-bench.db"
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    table_name = "benchmark"
    run_insert_benchmark_sqlite(c, table_name)
    print()
    run_select_benchmark_sqlite(c, table_name)
    delete_db(db_name)


def insert() -> None:
    insert_db_name = "bench_insert"
    try:
        run_insert_benchmark(insert_db_name)
    except Exception as e:
        print(e)
    finally:
        delete_db(f"{insert_db_name}.{VGDB_FILE_SUFFIX}")


def select() -> None:
    table_name = "bench_select"
    if not (Path(__file__).parent.parent / f"{table_name}.{VGDB_FILE_SUFFIX}").exists():
        print("Creating table...")
        create_table(table_name)
        evaluator = Evaluator(tables=get_tables())
        words = read_words()
        insert_words(evaluator, table_name, words)
    run_select_benchmark(table_name)


def main() -> None:
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--insert", action="store_true")
    group.add_argument("--select", action="store_true")
    group.add_argument("--sqlite", action="store_true")
    args = parser.parse_args()
    if args.insert:
        insert()
    elif args.select:
        select()
    elif args.sqlite:
        sqlite_bench()
    else:
        print()
        print("VGDB")
        print()
        insert()
        print()
        select()
        print()
        print("SQLITE")
        print()
        sqlite_bench()


if __name__ == "__main__":
    main()
