import sqlite3
from typing import Union, Iterable

from model import Dictionary  # type: ignore


def create_connection(db_file: str):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except sqlite3.OperationalError as e:
        print(e)
    return conn


def create_table(conn) -> None:
    cur = conn.cursor()
    query = '''CREATE TABLE if not exists dictionary
    (
        id      INTEGER primary key,
        uzbek   text,
        russian text,
        english text,
        used integer default 0
    );'''
    cur.execute(query)
    query = '''create table language (id integer primary key autoincrement , source text, target text);'''
    cur.execute(query)
    cur.execute("insert into language (id, source, target) values (null, 'uz', 'en');")
    conn.commit()


def create(conn, new_words: list[Union[str, int]]) -> None:
    cur = conn.cursor()
    query = 'INSERT INTO dictionary VALUES (null, ?, ?, ?)'
    cur.execute(query, new_words)
    conn.commit()


def read_all(conn, column: str = '*') -> list[tuple[Union[int, str]]]:
    cur = conn.cursor()
    query = f'SELECT {column} FROM dictionary;'
    result = cur.execute(query)
    return result.fetchall()


def read_one(conn, word: dict) -> tuple[Union[int, str]]:
    cur = conn.cursor()
    key = list(word.keys())[0]
    value = word[key]
    query = f"SELECT * FROM dictionary WHERE {key}='{value}';"
    result = cur.execute(query)
    return result.fetchone()


def update(conn, word: Dictionary) -> None:
    cur = conn.cursor()
    query = '''
    update dictionary
    set uzbek = :uzbek,
        russian = :russian,
        english = :english
    where id = :id;
    '''
    cur.execute(query, word.dict())
    conn.commit()


def execute(conn, query: str, commitable: bool = False, fetchall: bool = False) -> Union[list[tuple | str]]:
    cur = conn.cursor()
    cur.execute(query)
    if commitable:
        conn.commit()
    elif fetchall:
        return cur.fetchall()
    else:
        return cur.fetchone()


def delete(conn, _id: int) -> None:
    cur = conn.cursor()
    query = 'delete from dictionary where id = ?;'
    cur.execute(query, (_id,))
    conn.commit()


def update_used(conn, _id: int) -> None:
    cur = conn.cursor()
    _used = execute(conn, f'select * from dictionary where id = {_id};')[-1] + 1
    query = '''
    update dictionary
    set used = :used
    where id = :id;
    '''
    cur.execute(query, {'used': _used, 'id': _id})
    conn.commit()
