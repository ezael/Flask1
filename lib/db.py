import sqlite3

conn = sqlite3.connect('ga.db', check_same_thread=False)
c = conn.cursor()


def user_exist(username, email):
    t = (
        username,
        email,
    )
    c.execute("SELECT * FROM users WHERE username=? AND email=?", t)

    if c.fetchone():
        return True
    else:
        return False


def user_save(username, email, lang):
    t = (
        username,
        email,
        lang,
    )
    c.execute("INSERT INTO users (username, email, lang) VALUES (?, ?, ?)", t)
    conn.commit()

    return True


def user_get(username, email):
    t = (
        username,
        email,
    )
    c.execute("SELECT * FROM users WHERE username=? AND email=?", t)
    return c.fetchone()
