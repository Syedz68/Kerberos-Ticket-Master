from login_register import login, register
import socket

AS_HOST = '127.0.0.1'
TGS_HOST = '127.0.0.1'
S_HOST = '127.0.0.1'
AS_PORT = 9000
TGS_PORT = 9001
S_PORT = 9002


def request_ticket_granting_ticket(user_name, user_nid, user_pass):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((AS_HOST, AS_PORT))
        sock.send(f"{user_name},{user_nid},{user_pass}".encode())
        data = sock.recv(1024).decode()
        ticket, hashed_ticket = data.split(',')
        return ticket, hashed_ticket


def request_service_ticket(ticket, hashed_ticket, service_name):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((TGS_HOST, TGS_PORT))
        sock.send(f"{ticket},{hashed_ticket},{service_name}".encode())
        data = sock.recv(1024).decode()
        ticket, hashed_ticket = data.split(',')
        return ticket, hashed_ticket


def request_service(ticket, hashed_ticket):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((S_HOST, S_PORT))
        sock.send(f"{ticket},{hashed_ticket}".encode())
        data = sock.recv(1024).decode()
        return data


u_name = None
u_nid = None
u_pass = None
f1 = True
f2 = True
status = False
acc = input("Do you have any account? (y/n): ")
if acc == 'y' or acc == 'Y':
    while f1:
        print("------------------Login------------------")
        u_name = input("Enter user name: ")
        u_pass = input("Enter password: ")
        l = login(u_name, u_pass)
        if l[0]:
            print("Logged in successfully !!!")
            status = True
            f1 = False
            u_nid = l[1]
        else:
            print("Invalid user name or password")
else:
    while f2:
        print("------------------Register------------------")
        u_name = input("Enter user name: ")
        u_email = input("Enter your email: ")
        u_nid = input("Enter your NID number: ")
        u_pass = input("Set password: ")
        r = register(u_name, u_email, u_nid, u_pass)
        if r:
            print("Registration done successfully !!!")
            status = True
            f2 = False
        else:
            print("User Already exists")

if status:
    tgt_data = request_ticket_granting_ticket(u_name, u_nid, u_pass)
    if "Authentication Failed" in tgt_data:
        print("Authentication Failed")
    else:
        tgt, hashed_tgt = tgt_data
        sname = input("Enter service name: ")
        st_data = request_service_ticket(tgt, hashed_tgt, sname)
        if "Invalid Ticket" in st_data:
            print("Invalid Ticket")
        else:
            st, hashed_st = st_data
            s_data = request_service(st, hashed_st)
            if "Access Granted" in s_data:
                print("Access Granted")
            elif "Access Denied" in s_data:
                print("Access Denied")
