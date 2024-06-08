import socket
import rsa
import base64
import time
from cryptographic_elements import hash_md5, hash_sha256, loadTgsKey, loadServiceKey

TGS_HOST = '127.0.0.1'
TGS_PORT = 9001

tgs_private_key, tgs_public_key = loadTgsKey()
pri_key, pub_key = loadServiceKey()

with open("as_public_Key_Server.pem", "rb") as p:
    as_pub = rsa.PublicKey.load_pkcs1(p.read())


def validate_ticket_granting_ticket(ticket, hashed_ticket):
    ticket = base64.b64decode(ticket)
    hashed_ticket = base64.b64decode(hashed_ticket)
    decrypted_ticket = rsa.decrypt(ticket, tgs_private_key).decode('ascii')
    if rsa.verify(decrypted_ticket.encode('ascii'), hashed_ticket, as_pub):
        username, nid, password, timestamp = decrypted_ticket.split(':')
        return username, nid
    else:
        print("Ticket is not valid")
        return None, None


def generate_service_ticket(user, nid, service):
    st = f"{user}:{nid}:{service}:{time.time()}"
    return st


def signServiceTicket(ticket):
    return rsa.sign(ticket.encode('ascii'), tgs_private_key, 'SHA-256')


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.bind((TGS_HOST, TGS_PORT))
    sock.listen()
    print(f"Ticket Granting Server running on {TGS_HOST}:{TGS_PORT}")
    while True:
        con, addr = sock.accept()
        with con:
            print(f"Connected by {addr}")
            data = con.recv(1024).decode()
            if data:
                parts = data.split(',')
                ticket_id, hashed_ticket_id, service_name = parts
                validation = validate_ticket_granting_ticket(ticket_id, hashed_ticket_id)
                if validation:
                    service_ticket = generate_service_ticket(validation[0], validation[1], service_name)
                    service_ticket_hashed = signServiceTicket(service_ticket)
                    service_ticket = rsa.encrypt(service_ticket.encode('ascii'), pub_key)
                    service_ticket = base64.b64encode(service_ticket).decode()
                    service_ticket_hashed = base64.b64encode(service_ticket_hashed).decode()
                    msg = service_ticket + ',' + service_ticket_hashed
                    con.send(msg.encode())
                else:
                    con.send(b"Invalid Ticket")
