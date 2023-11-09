import access_controller
import account_manager
import getpass
import re

COMMON_PASSWORDS_FILE = "common_passwords.txt"

class UserInterface:
    def __init__(self, common_passwords_filename = COMMON_PASSWORDS_FILE):
        self.ac = access_controller.AccessController()
        self.am = account_manager.AccountManager()
        self.common_passwords_filename = common_passwords_filename

    def load_user(self, username, role):
        print("\n----------\nWelcome " + username + "!\n")
        print("Role: " + role + "\n")
        permissions = self.ac.get_permissions(role)
        if len(permissions) == 0:
            print("You are not allowed to use the system at this time!")
        else:
            res = ""
            for p in permissions.keys():
                res += permissions[p] + ":" + p +",\t"

            print(res)

    def load_login(self):
        username = input("Enter your username: ")
        password = getpass.getpass()

        res = self.am.login_user(username, password)
        if res in self.ac.policy:
            print("ACCESS GRANTED")
            self.load_user(username, res)
        else:
            print("INVALID LOGIN")
            self.start()

    def validate_username(self, username):
        return not self.am.username_exists(username)
    
    def validate_password(self, username, password):
        # Verifying the password requirements.
        # - length 8 to 12
        # - at least one upper case letter.
        # - at least one lower case letter.
        # - at least one digit
        # - at least one character from {!@#$%?*}
        # - length of between 8 and 12
        if not re.match("^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[!@#$%?*]).{8,12}$", password):
            return False
        
        # Looking for common passwords.
        common_passwords_file = open(self.common_passwords_filename, "r")
        lines = common_passwords_file.readlines()
        common_passwords_file.close()

        for p in lines:
            if re.search(p.strip().upper(), password.upper()):
                return False

        # Looking for calendar dates
        # - Checking for YYYY-MM-DD, YYYY/MM/DD, and YYY MM DD
        if re.search("^(?:19|20)\d{2}[- /.](?:0[1-9]|1[0-2])[- /.](?:0[1-9]|[12][0-9]|3[01])$", password):
            return False 
              
        # Looking for license plate numbers
        # - Checking for Canadian license plates: (4 letters followed by 3 numbers)
        if re.match("^(?:[a-zA-Z]{4}\d{3})$", password):
            return False 

        # Looking for telephone numbers
        # - Checking for consecutive numbers.
        if re.search("(?:\d{10,12})", password):
            return False

        # Looking for common numbers
        # - Checking years from 1900 to 2099
        if re.search("(?:19|20)\d{2}", password):
            return False
        
        # Checking to see if the user name appears in the password
        if re.search(username.upper(), password.upper()):
            return False
        
        return True
    
    def validate_role(self, role):
        return self.ac.has_role(role)
    
    def load_register(self):
        print("New user:")
        username = input("Username: ")
        while (not self.validate_username(username)):
            print("Error! username has been taken")
            username = input("Username: ")

        password = getpass.getpass()
        while (not self.validate_password(username, password)):
            print("Error! Invalid password")
            password = getpass.getpass()

        role = input("Role: ")
        while (not self.validate_role(role)):
            print("Error! Invalid role")
            role = input("Role: ")

        if self.am.enrol_user(username, password, role):
            print("User enrolled successfully!")
            self.start()
        else:
            print("Failed to register the user!")


    def start(self):
        print("\n==========\nFinvest Holdings\nClient Holdings and Information Systems\n----------")
        c = input("Enter L(l) to login and R(r) to register: ")

        if c.upper() == "L":
            self.load_login()
        elif c.upper() == "R":
            self.load_register()
        else:
            print("INVALID command")


if __name__ == "__main__":
    UserInterface().start()