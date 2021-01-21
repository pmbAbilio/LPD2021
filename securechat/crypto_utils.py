from Crypto.PublicKey import RSA
from Crypto import Random

class crypto_utils():
    
    def __init__(self)

    def generateKeyPair(self):
        random_generator = Random.new().read
        #Gerar par de chaves a 2048 bits
        key = RSA.generate(2048, random_generator)
        #Extrair chave publica
        public_key = key.publickey().exportKey()
        pubkey = open("keys/key.pub", 'a')
        pubkey.write(str(public_key))
        pubkey.close()
        #Extrair chave privada
        private_key = key.exportKey()
        privkey = open("keys/key.priv",'a')
        privkey.write(str(private_key))
        privkey.close()
    def encrypt_message(self, message):

        encripted_message = public_key.encrypt('Texto Importante', 32)
        return encripted_message
    #Encriptar com chave publica
    #
    #print encriptado_data
    #Desencriptar com chave privada
    #original_data = key.decrypt(encriptado_data)
    #print original_data