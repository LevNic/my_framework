import sqlite3


def create_sql():
    con = sqlite3.connect('patterns.sqlite')
    cur = con.cursor()
    with open('create_db.sql', 'r') as f:
        text = f.read()
    cur.executescript(text)
    cur.close()
    con.close()


if __name__ == '__main__':
    create_sql()
