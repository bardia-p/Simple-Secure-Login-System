import sys

sys.path.insert(0, './main')
import password_manager

class TestPasswordManager():
    def __init__(self):
        self.pm = password_manager.PasswordManager()
    
    def runTests(self):
        self.test_generated_hash()
        self.test_verify_user_hash()

    def test_generated_hash(self):
        print("\n----------\nRunning " + self.test_generated_hash.__name__ + "\n")

        salt = "2e30bc257707421d9880d2eac4ffd75e"
        password = "password"
        expected_hash = "2e30bc257707421d9880d2eac4ffd75eb5418169de7cbe67fc477b545b1c5cabc12a423d2c5d9d4fa341df72af9a3429"

        assert self.pm.generate_salted_password_hash(password, salt) == expected_hash, "The produced hash was incorrect."

        print("PASS")

    def test_verify_user_hash(self):
        print("\n----------\nRunning " + self.test_verify_user_hash.__name__ + "\n")

        password = "password"
        generated_hash = self.pm.generate_password_hash(password)

        assert self.pm.verify_user_hash(generated_hash, password) == True, "Hash verification failed"

        print("PASS")       


if __name__ == "__main__":
    print("\n==========\nTESTING PASSWORD MANAGER\n")
    tpm = TestPasswordManager()
    tpm.runTests()