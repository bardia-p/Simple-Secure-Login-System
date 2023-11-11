import hashlib
import uuid

SALT_SIZE = 32

class PasswordManager:
    '''
    The class in charge of encrypting and verifying the passwords.
    '''
    def __init__(self, salt_size = SALT_SIZE):
        '''
        The constructor for the password manager class.

        @param salt_size: The required salt size for the passwords (cannot be more than 32 characters)
        '''
        self.salt_size = salt_size

    def generate_salted_password_hash(self, password, salt):
        '''
        Generates salted hash for the given password and salt.

        @param password: The password to hash.
        @param salt: The salt to add to the password.
        '''
        # Returns the salt along side the encrypted version of the password and the salt.
        return salt + hashlib.sha256(salt.encode() + password.encode()).hexdigest()
    
    def generate_password_hash(self, password):
        '''
        Generates a salted hash for the given password.

        @param password: The password to ahsh.
        '''
        salt = uuid.uuid4().hex[:self.salt_size] #generates a unique salt of length salt_size.
        return self.generate_salted_password_hash(password, salt)
    
    def verify_user_hash(self, old_hash, password):
        '''
        Verifies if the password matches the given hash.

        @param old_hash: The hash to verify the passwor with.
        @param password: The new password to verify.
        '''
        salt = old_hash[:self.salt_size] #retrieves the salt from the old hash.

        # Recreate the hash to compare.
        return self.generate_salted_password_hash(password, salt) == old_hash