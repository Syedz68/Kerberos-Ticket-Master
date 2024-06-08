import socket
import rsa
import time
import base64
import mysql.connector
from cryptographic_elements import hash_md5, hash_sha256, loadTgsKey

conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='',
    database='kerberos'
)
cursor = conn.cursor()

AS_HOST = '127.0.0.1'
AS_PORT = 9000

private_key, public_key = loadTgsKey()

public_key_bytes = public_key.save_pkcs1(format='PEM')
pub_key = rsa.PublicKey.load_pkcs1(public_key_bytes)

with open("as_private_Key_Server.pem", "rb") as p:
    as_private = rsa.PrivateKey.load_pkcs1(p.read())


def authenticate_user(user, psw):
    cursor.execute("SELECT * FROM users where u_name = %s AND u_pass = %s", (user, psw))
    account = cursor.fetchone()
    if account:
        return True
    else:
        return False


def generate_ticket_granting_ticket(username, nid, psw):
    psw = hash_sha256(psw.encode())
    tgt = f"{username}:{nid}:{psw}:{time.time()}"
    return tgt


def signTheTicket(ticket):
    return rsa.sign(ticket.encode('ascii'), as_private, 'SHA-256')


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.bind((AS_HOST, AS_PORT))
    sock.listen()
    print(f"Authentication Server running on {AS_HOST}:{AS_PORT}")
    while True:
        con, addr = sock.accept()
        with con:
            print(f"Connected by {addr}")
            data = con.recv(1024).decode()
            if data:
                uname, unid, upass = data.split(',')
                if authenticate_user(uname, upass):
                    ticket = generate_ticket_granting_ticket(uname, unid, upass)
                    ticket_signed = signTheTicket(ticket)
                    ticket = rsa.encrypt(ticket.encode('ascii'), pub_key)
                    print(ticket)
                    print(ticket_signed)
                    ticket = base64.b64encode(ticket).decode()
                    ticket_hashed = base64.b64encode(ticket_signed).decode()
                    msg = ticket + ',' + ticket_hashed
                    con.send(msg.encode())
                else:
                    con.send(b"Authentication Failed")
