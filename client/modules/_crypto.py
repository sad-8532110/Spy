from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding

#-------------------------------------- CLASS AND FUNCTIONS

class symetric_key:
    def __init__(self, key:bytes):
        self.key = None
        self.key_bytes = key
        self.generate()
    
    def generate(self):
        """
        Try to prepare key
        """
        if self.key_bytes is None:
            self.key_bytes = Fernet.generate_key()
        self.key = Fernet(self.key_bytes)
    
    def return_key_bytes(self) -> bytes:
        """
        return the key bytes
        """
        return self.key_bytes
    
    def encrypt(self, data:bytes) -> bytes:
        """
        Try to encrypt the given data
        """
        return self.key.encrypt(data)
    
    def decrypt(self, data:bytes) -> bytes:
        """
        Try to decrypt the given data
        """
        return self.key.decrypt(data)

class asymetric_key:
    def __init__(self, key:bytes):
        self.private_key = None
        self.public_key = None
        self.public_key_bytes = key
        self.generate()
    
    def generate(self):
        """
        Try to prepare public key or private key
        """
        if self.public_key_bytes is None:
            self.private_key = rsa.generate_private_key(
                                public_exponent=65537,
                                key_size=2048)
            self.public_key = self.private_key.public_key()
            self.public_key_bytes = self.public_key.public_bytes(
                                    encoding=serialization.Encoding.PEM,
                                    format=serialization.PublicFormat.SubjectPublicKeyInfo)
        else:
            self.public_key = serialization.load_pem_public_key(self.public_key_bytes)
    
    def return_key_bytes(self) -> bytes:
        """
        return the public key bytes
        """
        return self.public_key_bytes
    
    def encrypt(self, data:bytes) -> bytes:
        """
        Try to encrypt the given data by public key
        """
        data = self.public_key.encrypt(data,
                padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None))
        return data
    
    def decrypt(self, data:bytes) -> bytes:
        """
        Try to decrypt the given data by private key
        """
        if self.private_key is not None:
            data = self.private_key.decrypt(data,
                    padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None))
            return data

class cryptor:
    def __init__(self):
        self.keys = {}
    
    def register_key(self, key_id, key_type, key:bytes=None):
        """
        Try to save a key to be used in the future
        """
        if key_type == 'symetric':
            self.keys[key_id] = symetric_key(key)
        
        elif key_type == 'asymetric':
            self.keys[key_id] = asymetric_key(key)
    
    def return_key_bytes(self, key_id) -> bytes:
        """
        return the key bytes by given key id
        """
        return self.keys[key_id].return_key_bytes()
    
    def remove_key(self, key_id):
        """
        Remove a key
        """
        del self.keys[key_id]
    
    def encrypt(self, key_id, data:bytes) -> bytes:
        """
        Try to encrypt the given data by specified key
        """
        return self.keys[key_id].encrypt(data)
    
    def decrypt(self, key_id, data:bytes) -> bytes:
        """
        Try to decrypt the given data by specified key
        """
        return self.keys[key_id].decrypt(data)

