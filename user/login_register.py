import mysql.connector

conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='',
    database='kerberos'
)
cursor = conn.cursor()


def login(user, psw):
    cursor.execute("SELECT * FROM users where u_name = %s AND u_pass = %s", (user, psw))
    users = cursor.fetchone()
    if users:
        return True, users[3]


def register(user, email, nid, psw):
    cursor.execute("SELECT * FROM users where u_name = %s AND u_pass = %s", (user, psw))
    users = cursor.fetchone()
    if users:
        return False
    else:
        cursor.execute("INSERT INTO users (u_name, u_email, u_nid, u_pass) VALUES (%s, %s, %s, %s)", (user, email, nid, psw))
        conn.commit()
        return True

