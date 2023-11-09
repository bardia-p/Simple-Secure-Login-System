import sys
import os

sys.path.insert(0, './main')
import account_manager

TEST_PASSWORD_FILENAME = "test_passwd.txt"

class TestAccountManager():
    def __init__(self):
        self.am = account_manager.AccountManager(TEST_PASSWORD_FILENAME)
        if os.path.isfile(TEST_PASSWORD_FILENAME):
            os.remove(TEST_PASSWORD_FILENAME)

    def runTests(self):
        self.test_enrol_user()
        self.test_save_same_user()
        self.test_invalid_password()

    def test_enrol_user(self):
        print("\n----------\nRunning " + self.test_enrol_user.__name__ + "\n")

        user_name = "bardia"
        password = "password"
        role = "Regular User"

        res = self.am.enrol_user(user_name, password, role)
        
        assert res == True, "The user was not enrolled properly."
        assert self.am.username_exists(user_name) == True, "The user was not recorded properly."
        assert self.am.login_user(user_name, password) == role, "The user was not enrolled properly."

        print("PASS")

    def test_save_same_user(self):
        print("\n----------\nRunning " + self.test_save_same_user.__name__ + "\n")

        user_name = "cassidy"
        password = "password123"
        role = "Regular User"

        res = self.am.enrol_user(user_name, password, role)
        
        assert res == True, "The user was not enrolled properly."
        assert self.am.username_exists(user_name) == True, "The username was not recorded properly."
        assert self.am.enrol_user(user_name, password, role) == False, "The same user was recorded twice."

        print("PASS")

    def test_invalid_password(self):
        print("\n----------\nRunning " + self.test_invalid_password.__name__ + "\n")

        user_name = "doro"
        password = "abcd"
        role = "Regular User"

        res = self.am.enrol_user(user_name, password, role)
        
        assert res == True, "The user was not enrolled properly."
        assert self.am.username_exists(user_name) == True, "The user was not recorded properly."
        assert self.am.login_user(user_name, "password") == "INVALID", "The user was not enrolled properly."

        print("PASS")

if __name__ == "__main__":
    print("\n==========\nTESTING ACCOUNT MANAGER\n")
    tam = TestAccountManager()
    tam.runTests()