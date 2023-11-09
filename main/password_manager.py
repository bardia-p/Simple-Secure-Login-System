import hashlib
import uuid

SALT_SIZE = 32

class PasswordManager:
    def __init__(self, salt_size = SALT_SIZE):
        self.salt_size = salt_size

    def generate_salted_password_hash(self, password, salt = uuid.uuid4().hex):
        return salt + hashlib.sha256(salt.encode() + password.encode()).hexdigest()
    
    def verify_user_hash(self, old_hash, password):
        salt = old_hash[:self.salt_size]
        return self.generate_salted_password_hash(password, salt) == old_hash