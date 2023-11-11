import sys

sys.path.insert(0, './main')
import user_interface

class TestUserInterface():
    '''
    Tests the UserInterface class.
    '''
    def __init__(self):
        '''
        The constructor for the User Interface.
        '''
        self.ui = user_interface.UserInterface()
    
    def runTests(self):
        '''
        Runs all the tests in the test harness.
        '''
        self.test_validate_role()
        self.test_validate_password()

    def test_validate_role(self):
        '''
        Tests the role validation command in the UI.
        '''
        print("\n----------\nRunning " + self.test_validate_role.__name__ + "\n")

        # Testing a valid role.
        assert self.ui.validate_role("Regular Client") == True, "Could not verify valid role."

        # Testing a invalid role.
        assert self.ui.validate_role("client") == False, "Could not reject invalid role."

        print("PASS")   

    def test_validate_password(self):
        '''
        Tests the password validation with different passwords.
        '''
        print("\n----------\nRunning " + self.test_validate_password.__name__ + "\n")

        username = "bardia"

        # Testing a short password.
        assert self.ui.validate_password(username, "Abcd12!") == False, "Error: short password test failed."

        # Testing a long password.
        assert self.ui.validate_password(username, "Abcd12345678!") == False, "Error: long password test failed."

        # Testing an all lower case password.
        assert self.ui.validate_password(username, "abcd1234!") == False, "Error: upper test case test failed."

        # Testing an all upper case password.
        assert self.ui.validate_password(username, "ABCD1234!") == False, "Error: lower test case test failed."

        # Testing a password with no digits.
        assert self.ui.validate_password(username, "abcdefgh!") == False, "Error: digit test case test failed."

        # Testing a password without special characters.
        assert self.ui.validate_password(username, "abcdefgh1") == False, "Error: special character test case test failed."

        # Testing a password with common passwords.
        assert self.ui.validate_password(username, "Password123!") == False, "Error: common password test case test failed."

        # Testing a password with date.
        assert self.ui.validate_password(username, "Aa20231020!") == False, "Error: date password test case test failed."

        # Testing a password with license plate.
        assert self.ui.validate_password(username, "ABCD123!") == False, "Error: license plate test case test failed."

        # Testing a password with phone numbers.
        assert self.ui.validate_password(username, "0123456789") == False, "Error: phone number test case test failed."

        # Testing a password with common numbers.
        assert self.ui.validate_password(username, "Password2023!") == False, "Error: common numbers test case test failed."

        # Testing a password with a username in t.
        assert self.ui.validate_password(username, "Bardia123!") == False, "Error: username test case test failed."

        # Testing a valid password.
        assert self.ui.validate_password(username, "Abard1234!") == True, "Error: valid password test case test failed."

        print("PASS")   


if __name__ == "__main__":
    print("\n==========\nTESTING USER INTERFACE\n")
    tui = TestUserInterface()
    tui.runTests()