from sqlite3 import Cursor

def select_all(cursor: Cursor, table: str):
    cursor.execute(f'SELECT * FROM {table};')
    print(cursor.fetchall())