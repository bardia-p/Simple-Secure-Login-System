import sys

sys.path.insert(0, './main')
import access_controller

class TestAccessController():
    '''
    Tests the AccessContoller class.
    '''
    def __init__(self):
        '''
        Initializes the tests.
        '''
        self.ac = access_controller.AccessController()

    def runTests(self):
        '''
        Runs all the tests in the test harness.
        '''
        self.test_roles()
        self.test_time_restriction()

    def test_roles(self):
        '''
        Tests the permissions for all the roles.
        '''
        print("\n----------\nRunning " + self.test_roles.__name__ + "\n")
        expected_roles = {'Regular Client', 'Premium Client', 'NonTechEmployee', 'Financial Advisor', 'Financial Planner', 'Investment Analyst', 'Technical Support', 'Teller', 'Compliance Officer'}
        assert set(self.ac.policy.keys()) == expected_roles, "The roles did not match"

        for r in self.ac.policy.keys():
            print("Testing " + r)
            if r == "Regular Client":
                expected_permissions = {'Client Information': 'View/Modify', 'Account Balance': 'View', 'Investment Portfolio': 'View', 'Financial Advisor Contacts': 'View'}
            elif r == "Premium Client":
                expected_permissions = {'Client Information': 'View/Modify', 'Account Balance': 'View', 'Investment Portfolio': 'View/Modify', 'Financial Advisor Contacts': 'View', 'Financial Planner Contacts': 'View', 'Investment Analyst Contacts': 'View'}
            elif r == "NonTechEmployee":
                expected_permissions = {'Account Balance': 'View', 'Investment Portfolio': 'View'}
            elif r == "Financial Advisor":
                expected_permissions = {'Account Balance': 'View', 'Investment Portfolio': 'View/Modify', 'Private Consumer Instruments': 'View'}
            elif r == "Financial Planner":
                expected_permissions = {'Account Balance': 'View', 'Investment Portfolio': 'View/Modify', 'Private Consumer Instruments': 'View', 'Money Market Instruments': 'View'}
            elif r == "Investment Analyst":
                expected_permissions = {'Account Balance': 'View', 'Investment Portfolio': 'View/Modify', 'Private Consumer Instruments': 'View', 'Money Market Instruments': 'View', 'Derivatives Trading': 'View', 'Interest Instruments': 'View'}
            elif r == "Technical Support":
                expected_permissions = {'Client Information': 'View', 'Request Client Account': 'Execute'}
            elif r == "Teller":
                expected_permissions = {'Account Balance': 'View', 'Investment Portfolio': 'View'}
            elif r == "Compliance Officer":
                expected_permissions = {'Account Balance': 'View', 'Investment Portfolio': 'View', 'Validate Investment Portfolio': 'Execute'}
            else:
                expected_permissions = {}

            assert self.ac.policy[r]["permissions"] == expected_permissions, f"The permissions for {r} were incorrect"

        print("\nPASSED")

    def test_time_restriction(self):
        '''
        Tests whether the time restriction is properly applied.
        '''
        print("\n----------\nRunning " + self.test_time_restriction.__name__ + "\n")
        
        # Set the clock to 11am
        self.ac.currentHour = 11
        assert self.ac.get_permissions("Teller") == {'Account Balance': 'View', 'Investment Portfolio': 'View'}, "The permissions for Teller were incorrect during work hours."

        # Set the clock to 6pm
        self.ac.currentHour = 18
        assert self.ac.get_permissions("Teller") == {}, "The permissions for Teller were incorrect outside work hours."

        print("PASSED")

if __name__ == "__main__":
    print("\n==========\nTESTING ACCESS CONTROLLER\n")
    tac = TestAccessController()
    tac.runTests()