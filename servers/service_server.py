import base64
import socket
import rsa
from cryptographic_elements import hash_sha256, loadServiceKey

S_HOST = '127.0.0.1'
S_PORT = 9002

pri_key, pub_key = loadServiceKey()

with open("tgs_public_Key_Server.pem", "rb") as p:
    tgs_pub = rsa.PublicKey.load_pkcs1(p.read())


def validate_service_ticket(ticket, hashed_ticket):
    try:
        ticket = base64.b64decode(ticket)
        hashed_ticket = base64.b64decode(hashed_ticket)
        decrypted_ticket = rsa.decrypt(ticket, pri_key).decode('ascii')
        if rsa.verify(decrypted_ticket.encode('ascii'), hashed_ticket, tgs_pub):
            username, nid, service, timestamp = decrypted_ticket.split(':')
            return username, service
        else:
            print("Ticket is not valid")
            return None, None
    except Exception as e:
        print(f"Validation error: {e}")
        return None


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.bind((S_HOST, S_PORT))
    sock.listen()
    print(f"Service Server running on {S_HOST}:{S_PORT}")
    while True:
        con, addr = sock.accept()
        with con:
            print(f"Connected by {addr}")
            data = con.recv(1024).decode()
            if data:
                service_ticket, hashed_service_ticket = data.split(',')
                uname, service_name = validate_service_ticket(service_ticket, hashed_service_ticket)
                if service_name == 'kerberos':
                    con.send(b"Access Granted")
                else:
                    con.send(b"Access Denied")
