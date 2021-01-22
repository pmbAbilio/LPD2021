from Crypto.PublicKey import RSA
from Crypto import Random

class crypto_utils():

    def generateKeyPair(self):
        random_generator = Random.new().read
        #Gerar par de chaves a 2048 bits
        key = RSA.generate(2048, random_generator)
        #Extrair chave publica
        public_key = key.publickey().exportKey()
        pubkey = open("key.pub", 'w')
        pubkey.write(str(public_key))
        pubkey.close()
        #Extrair chave privada
        private_key = key.exportKey()
        privkey = open("key.priv",'w')
        privkey.write(str(private_key))
        privkey.close()
        return public_key
        
    def encrypt_message(self, message, key):
        encripted_message = key.encrypt(message, 32)
        return encripted_message
    
    def decrypt_message(self):
        key = open("keys/key.priv", "r")
        decripted_message = key.decrypt(encriptado_data)
        return decripted_message
    
    