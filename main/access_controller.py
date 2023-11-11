import json
from datetime import datetime

POLICY_FILE = "policy.json"

class AccessController():
    """
    The class in charge of parsing and maintaining the security policy for the system.
    """

    def __init__(self, policy_filename = POLICY_FILE):
        """
        The constructor for the class.

        @param policy_filename: the filename for the policy file which is to be parsed.
        """
        self.policy_filename = policy_filename
        self.policy = dict()

        # Used to indicate the current time within the system.
        self.currentHour = datetime.now().hour

        # Parse the policy file to start up the system.
        self.parse_policy_file()

    def has_role(self, role):
        """
        Checks to see if the given role exists in the policy.

        @param role: the role to verify 
        """
        return role in self.policy
    
    def parse_policy_file(self):
        """
        Parses the policy JSON file and stores in self.policy.
        """
        policy_file = open(self.policy_filename, "r")
        parsed_obj = json.loads(policy_file.read())
        policy_file.close()

        for r in parsed_obj["roles"]:
            permissions = dict()
            if "parent" in r:
                permissions = self.policy[r["parent"]]["permissions"].copy()

            if "permissions" in r:
                for p in r["permissions"]:
                    if p in permissions:
                        permissions[p] += "/" + r["permissions"][p]
                    else:
                        permissions[p] = r["permissions"][p]

            restrictions = dict()

            if "restrictions" in r:
                restrictions = r["restrictions"]

            self.policy[r["name"]] = {"permissions" : permissions, "restrictions" : restrictions}

    def get_permissions(self, role):
        """
        Returns the permissions for a given role.

        @param role: the role to receive permissions for.
        """
        if role not in self.policy:
            return dict()
        
        r = self.policy[role]

        if len(r["restrictions"]) == 0:
            return r["permissions"]
        else:
            if self.apply_restrictions(r["restrictions"]):
                return r["permissions"]
            else:
                return dict()
                
    def apply_restrictions(self, restrictions):
        """
        Applies the given list of restrictions and verifies if they are true or not.

        @param restrictions: list of restrictions to apply.
        """
        res = True
        for r in restrictions.keys():
            if r == "time":
                res &= self.apply_time_restriction(restrictions["time"])
        return res
    
    def apply_time_restriction(self, time_restriction):
        """
        Applies the given time restriction and verifies if the it is followed or not.

        @param: time_restriction: the time restriction for the system.
        """
        return time_restriction[0] <= self.currentHour < time_restriction[1]
                
    def print_policy(self):
        """
        Displays the policy.
        """
        print("##########\nList of roles:\n")
        print(list(self.policy.keys()))
        print("==========\nDetailed Policy:\n")
        for r in self.policy.keys():
            print("Role: " + r)
            print("Permissions:")
            print(self.policy[r]["permissions"])
            print("Restrictions:")
            print(self.policy[r]["restrictions"])
            print("----------")
        print("##########")