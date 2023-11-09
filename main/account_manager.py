import os
import password_manager

PASSWORD_FILE = "passwd.txt"

class AccountManager:
    def __init__(self, password_filename = PASSWORD_FILE):
        self.password_filename = password_filename
        self.pm = password_manager.PasswordManager()

    def username_exists(self, user_name):
        if not os.path.isfile(self.password_filename):
            return False
        
        password_file = open(self.password_filename, "r")
        lines = password_file.readlines()
        password_file.close()

        for line in lines:
            split_line = line.strip().split(":")
            if split_line[0] == user_name:
                return True
        return False
    
    def enrol_user(self, user_name, password, role):
        if not self.username_exists(user_name):
            password_file = open(self.password_filename, "a")
            encrypted_pasword = self.pm.generate_salted_password_hash(password)
            password_line = user_name + ":" + encrypted_pasword + ":" + role + "\n"
            password_file.write(password_line)
            password_file.close()
            return True

        return False
    
    def login_user(self, user_name, password):
        if not self.username_exists(user_name):
            return "INVALID"
        
        if not os.path.isfile(self.password_filename):
            return False
        password_file = open(self.password_filename, "r")
        lines = password_file.readlines()
        password_file.close()

        for line in lines:
            split_line = line.strip().split(":")
            if split_line[0] == user_name:
                if self.pm.verify_user_hash(split_line[1], password):
                    return split_line[2]
                else:
                    return "INVALID"