import access_controller
import account_manager
import getpass

class UserInterface:
    def __init__(self):
        self.ac = access_controller.AccessController()
        self.am = account_manager.AccountManager()

    def load_user(self, role):
        print("\n----------\nWelcome!\n")
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
            self.load_user(res)
        else:
            print("INVALID LOGIN")
            self.start()

    def validate_username(self, username):
        return not self.am.username_exists(username)
    
    def validate_password(self, password):
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
        while (not self.validate_password(password)):
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