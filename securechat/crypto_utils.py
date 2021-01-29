from Crypto.PublicKey import RSA
from Crypto import Random
from Crypto.Cipher import PKCS1_OAEP
import os


class crypto_utils():
    PRIV_KEY = ""
    PUB_KEY = ""
    PRIV_KEY_FILE = "/priv.key"
    PUB_KEY_FILE = "/pub.key"
    DEBUG = True

    def generateKeyPair(self):
        key = RSA.generate(2048)
        cwd = os.getcwd()
        
        self.PUB_KEY = key.publickey().exportKey()
        self.PRIV_KEY = key.exportKey()
        
        return self.PUB_KEY, self.PRIV_KEY
        
    def encrypt_message(self, message, key):
        rsa_key = RSA.importKey(key)
        encryptor = PKCS1_OAEP.new(rsa_key)
        encrypted_msg = encryptor.encrypt(message)
        return encrypted_msg
    
    def decrypt_message(self, message, key):
        if len(self.PRIV_KEY) > 0:
            key = self.PRIV_KEY
        rsa_key = RSA.importKey(key)
        decriptor = PKCS1_OAEP.new(rsa_key)
        decripted_message = decriptor.decrypt(message)
        return decripted_message
    
    