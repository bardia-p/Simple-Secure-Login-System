import sys
import os

sys.path.insert(0, './main')
import account_manager

TEST_PASSWORD_FILENAME = "test_passwd.txt"

class TestAccountManager():
    '''
    Tests the AccountManager class.
    '''
    def __init__(self):
        '''
        Initializes the tests.
        '''
        self.am = account_manager.AccountManager(TEST_PASSWORD_FILENAME)
        if os.path.isfile(TEST_PASSWORD_FILENAME):
            os.remove(TEST_PASSWORD_FILENAME)

    def runTests(self):
        '''
        Runs all the tests in the test harness.
        '''
        self.test_enrol_user()
        self.test_save_same_user()
        self.test_invalid_password()

    def test_enrol_user(self):
        '''
        Tests enrolling a user.
        '''
        print("\n----------\nRunning " + self.test_enrol_user.__name__ + "\n")

        username = "bardia"
        password = "password"
        role = "Regular User"

        res = self.am.enrol_user(username, password, role)
        
        assert res == True, "The user was not enrolled properly."
        assert self.am.username_exists(username) == True, "The user was not recorded properly."
        assert self.am.login_user(username, password) == role, "The user was not enrolled properly."

        print("PASS")

    def test_save_same_user(self):
        '''
        Tests enrolling the same user.
        '''
        print("\n----------\nRunning " + self.test_save_same_user.__name__ + "\n")

        username = "cassidy"
        password = "password123"
        role = "Regular User"

        res = self.am.enrol_user(username, password, role)
        
        assert res == True, "The user was not enrolled properly."
        assert self.am.username_exists(username) == True, "The username was not recorded properly."
        assert self.am.enrol_user(username, password, role) == False, "The same user was recorded twice."

        print("PASS")

    def test_invalid_password(self):
        '''
        Tests logging in with an invalid password.
        '''
        print("\n----------\nRunning " + self.test_invalid_password.__name__ + "\n")

        username = "doro"
        password = "abcd"
        role = "Regular User"

        res = self.am.enrol_user(username, password, role)
        
        assert res == True, "The user was not enrolled properly."
        assert self.am.username_exists(username) == True, "The user was not recorded properly."
        assert self.am.login_user(username, "password") == "INVALID", "The user was not enrolled properly."

        print("PASS")

if __name__ == "__main__":
    print("\n==========\nTESTING ACCOUNT MANAGER\n")
    tam = TestAccountManager()
    tam.runTests()