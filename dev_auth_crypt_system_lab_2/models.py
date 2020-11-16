import sqlite3 as sql

def retrieveUsers(username):
    con = sql.connect("database.db")
    cur = con.cursor()
    cur.execute("SELECT username, password, email FROM users WHERE username = '{}'".format(username))
    users = cur.fetchall()
    con.close()
    return users

def insert_temp_code(username, hash_temp_code):
    con = sql.connect("database.db")
    cur = con.cursor()
    sql_query = "UPDATE users SET md5_temp_code = '{}' WHERE username = '{}'".format(hash_temp_code, username)
    cur.execute(sql_query)
    con.commit()
    con.close()

def get_temp_code(username):
    con = sql.connect("database.db")
    cur = con.cursor()
    cur.execute("SELECT md5_temp_code FROM users WHERE username = '{}'".format(username))
    md5_temp_code = cur.fetchall()
    con.close()
    return md5_temp_code