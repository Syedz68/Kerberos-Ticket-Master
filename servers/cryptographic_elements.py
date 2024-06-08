import rsa
import hashlib


def generateAuthenticationKey():
    (as_public_key, as_private_key) = rsa.newkeys(2048)
    with open('as_public_Key_Server.pem', 'wb') as p:
        p.write(as_public_key.save_pkcs1('PEM'))
    with open('as_private_Key_Server.pem', 'wb') as p:
        p.write(as_private_key.save_pkcs1('PEM'))


def generateServiceKey():
    (public_key, private_key) = rsa.newkeys(2048)
    with open('public_Key_Server.pem', 'wb') as p:
        p.write(public_key.save_pkcs1('PEM'))
    with open('private_Key_Server.pem', 'wb') as p:
        p.write(private_key.save_pkcs1('PEM'))


def generateTgsKey():
    (tgs_public_key, tgs_private_key) = rsa.newkeys(2048)
    with open('tgs_public_Key_Server.pem', 'wb') as p:
        p.write(tgs_public_key.save_pkcs1('PEM'))
    with open('tgs_private_Key_Server.pem', 'wb') as p:
        p.write(tgs_private_key.save_pkcs1('PEM'))


def loadServiceKey():
    with open('public_Key_Server.pem', 'rb') as p:
        publicKey = rsa.PublicKey.load_pkcs1(p.read())
    with open('private_Key_Server.pem', 'rb') as p:
        privateKey = rsa.PrivateKey.load_pkcs1(p.read())
    return privateKey, publicKey


def loadTgsKey():
    with open('tgs_public_Key_Server.pem', 'rb') as p:
        publicKey = rsa.PublicKey.load_pkcs1(p.read())
    with open('tgs_private_Key_Server.pem', 'rb') as p:
        privateKey = rsa.PrivateKey.load_pkcs1(p.read())
    return privateKey, publicKey


def hash_sha256(d):
    return hashlib.sha256(d).hexdigest()


def hash_md5(d):
    return hashlib.md5(d).hexdigest()


"""
generateAuthenticationKey()
generateServiceKey()
generateTgsKey()
"""
