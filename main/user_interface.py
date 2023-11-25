import access_controller
import account_manager
import getpass
import re

COMMON_PASSWORDS_FILE = "common_passwords.txt"

class UserInterface:
    '''
    Handles the UI for the system.
    '''
    def __init__(self, common_passwords_filename = COMMON_PASSWORDS_FILE):
        '''
        Constructor for the user interface.

        @param common_passwords_filename: The filename for the list of the common passwords.
        '''
        self.ac = access_controller.AccessController()
        self.am = account_manager.AccountManager()
        self.common_passwords_filename = common_passwords_filename
    
    def validate_password(self, username, password):
        '''
        Validates the given password based on the password rules.

        @param username: the username for the user.
        @param password: the proposed password.
        '''
        # Verifying the password requirements.
        # - length 8 to 12
        # - at least one upper case letter.
        # - at least one lower case letter.
        # - at least one digit
        # - at least one character from {!@#$%?*}
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
        # - Checking for YYYYMMDD
        if re.search("(?:19|20)\d{2}(?:0[1-9]|1[0-2])(?:0[1-9]|[12][0-9]|3[01])", password):
            return False 
              
        # Looking for license plate numbers
        # - Checking for Canadian license plates: (4 letters followed by 3 numbers)
        if re.search("(?:[A-Z]{4}\d{3})", password):
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
        '''
        Validates the given role.

        @param role: the role to valdiate.
        '''
        return self.ac.has_role(role)
    
    def display_perms(self, permissions):
        '''
        Displays the permissions

        @param permissions: the dictionary of all the user permissions.
        '''
        perms = []
        for p in permissions.keys():
            perms.append(permissions[p] + ":" + p)
        print("\t\t".join(perms))

    def take_commands(self, username, role, permissions):
        '''
        Takes in a command and verifies it against the permissions.

        @param username: The username for the user.
        @param role: The user role.
        @param permissions: The permissions for the user.
        '''
        command = input("\nEnter a command: Enter x to exit: ")

        while (command != "x"):
            if command not in permissions:
                print("INVALID COMMAND")
            elif command == "Request Client Account" and permissions[command] == "Execute":
                print("Client Access Granted")
                new_permissions = self.ac.get_permissions("Regular Client")
                for p in new_permissions.keys():
                    permissions[p] = new_permissions[p]

            self.display_perms(permissions)
            command = input("\nEnter a command: Enter x to exit: ")

    def load_user(self, username, role):
        '''
        Displays the window for loading the user information.

        @param username: The username of the user to load.
        @param role: The role for the user to load.
        '''
        print("\n----------\nWelcome " + username + "!\n")
        print("Role: " + role + "\n")
        permissions = self.ac.get_permissions(role)
        if len(permissions) == 0:
            print("You are not allowed to use the system at this time!")
        else:
            self.display_perms(permissions)
            self.take_commands(username, role, permissions)

    def load_login(self):
        '''
        Displays the login screen.
        '''
        username = input("Enter your username: ")
        password = getpass.getpass()

        res = self.am.login_user(username, password)
        if res in self.ac.policy:
            print("ACCESS GRANTED")
            self.load_user(username, res)
        else:
            print("INVALID LOGIN")
            self.start()

    def load_register(self):
        '''
        Loads the registeration windwo.
        '''
        print("New user:")
        username = input("Username: ")
        password = getpass.getpass()
        while (not self.validate_password(username, password)):
            print("Error! Invalid password")
            password = getpass.getpass()

        print("Select from one of the available roles:\n" + "\t".join(self.ac.policy))
        role = input("Role: ")
        while (not self.validate_role(role)):
            print("Error! Invalid role")
            print("Select from one of the available roles:\n" + "\t".join(self.ac.policy))
            role = input("Role: ")

        email = input("Email Address: ")

        if self.am.enrol_user(username, password, role, email):
            print("User enrolled successfully!")
            self.start()
        else:
            print("Failed to register the user! Username already exists")


    def start(self):
        '''
        The start menu. Loading the application.
        '''
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