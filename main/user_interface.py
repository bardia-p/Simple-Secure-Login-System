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
        user_name = input("Enter your username: ")
        password = getpass.getpass()

        res = self.am.login_user(user_name, password)
        if res in self.ac.policy:
            print("ACCESS GRANTED")
            self.load_user(res)
        else:
            print("INVALID LOGIN")

    def load_register(self):
        print("Enter your details")
        #user_name = 

    def start(self):
        print("Finvest Holdings\nClient Holdings and Information Systems\n----------")
        c = input("Enter L(l) to login and R(r) to register: ")

        if c.upper() == "L":
            self.load_login()
        elif c.upper() == "R":
            self.load_register()
        else:
            print("INVALID command")


if __name__ == "__main__":
    UserInterface().start()