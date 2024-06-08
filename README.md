# Kerberos Ticket Master

Kerberos Ticket Master is a simple implementation of the Kerberos protocol using Python for secure authentication in a distributed network environment. This project demonstrates the interaction between an Authentication Server (AS), a Ticket Granting Server (TGS), and a Service Server (SS) to provide secure authentication and authorization for users accessing network services.

## Features

- **User Authentication**: Users can log in using their credentials (username and password).
- **User Registration**: New users can register by providing their details (username, email, NID, and password).
- **Ticket-granting Ticket (TGT) Issuance**: After successful authentication, the authentication server issues a TGT to the user.
- **Service Ticket Issuance**: The TGS issues a service ticket to the user upon request, allowing access to specific services.
- **Service Access Control**: The service server grants or denies access to services based on the validity of the service ticket.
- **Cryptographic Operations**: RSA key generation, loading, and encryption/decryption functions, as well as hash functions (SHA-256 and MD5) for data integrity and authentication.
- **Signature Verification**: The system supports signature verification to ensure the authenticity of encrypted data.

## Project Structure

- `user.py`: This script handles the user's interaction with the system. It provides functionality for user login, registration, and service requests.
- `login_register.py`: This module contains functions for user login and registration.
- `authentication_server.py`: This script implements the authentication server, which verifies user credentials and issues ticket-granting tickets (TGTs).
- `ticket_granting_server.py`: This script implements the ticket-granting server (TGS), which validates TGTs and issues service tickets.
- `service_server.py`: This script implements the service server, which provides services based on the validation of service tickets.
- `cryptographic_elements.py`: This module contains functions for generating and loading RSA keys, as well as hash functions for cryptographic operations.

## Images of The Project

![k1](https://github.com/Syedz68/Kerberos-Ticket-Master/assets/107263740/2b6e2441-0cfc-4db2-8069-0d7682045993)
![k2](https://github.com/Syedz68/Kerberos-Ticket-Master/assets/107263740/22208241-de21-4087-923b-0aa2748590b1)
