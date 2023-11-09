import json
from datetime import datetime

POLICY_FILE = "policy.json"

class AccessController():
    def __init__(self, policy_filename = POLICY_FILE):
        self.policy_filename = policy_filename
        self.policy = dict()
        self.currentHour = datetime.now().hour
        self.parse_policy_file()

    def parse_policy_file(self):
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
        if role not in self.policy:
            return dict()
        
        r = self.policy[role]

        if len(r["restrictions"]) == 0:
            return r["permissions"]
        else:
            if self.verify_restrictions(r["restrictions"]):
                return r["permissions"]
            else:
                return dict()
                
    def verify_restrictions(self, restrictions):
        res = True
        for r in restrictions.keys():
            if r == "time":
                res &= self.verify_time_restriction(restrictions["time"])
        return res
    
    def verify_time_restriction(self, time_restriction):
        return time_restriction[0] <= self.currentHour < time_restriction[1]
                
    def print_policy(self):
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