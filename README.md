# Simple Secure Login System
This application simulates a simple login system for Vinfest Holdings that allows users to register and login based on their various roles. The users are given different permissions based on their role. 

To help secure the login process, the user's credentials are secured and hashed with a 32 byte salt. In addition, the system enforces various password rules that were specified by the company. 

The detailed policy for the system can be found in the policy.json file.

## Using the system
To use the system simply locate the user interface and follow the prompts:

```
$ python3 main/user_interface.py 

==========
Finvest Holdings
Client Holdings and Information Systems
----------
Enter L(l) to login and R(r) to register: l
Enter your username: bardia
Password: 
ACCESS GRANTED

----------
Welcome bardia!

Role: Regular Client

View/Modify:Client Information          View:Account Balance            View:Investment Portfolio               View:Financial Advisor Contacts

Enter a command: Enter x to exit: 
```

# Launching the tests
Extensive testing was conducted to ensure the system is working as expected. To launch the tests simply use the runtests script:

```
$ ./runtests.sh 

==========
TESTING ACCESS CONTROLLER


----------
Running test_roles

Testing Regular Client
Testing Premium Client
Testing NonTechEmployee
Testing Financial Advisor
Testing Financial Planner
Testing Investment Analyst
Testing Technical Support
Testing Teller
Testing Compliance Officer

PASSED

----------
Running test_time_restriction

PASSED

==========
TESTING PASSWORD MANAGER


----------
Running test_generated_hash

PASS

----------
Running test_verify_user_hash

PASS

==========
TESTING ACCOUNT MANAGER


----------
Running test_enrol_user

PASS

----------
Running test_save_same_user

PASS

----------
Running test_invalid_password

PASS

==========
TESTING USER INTERFACE


----------
Running test_validate_role

PASS

----------
Running test_validate_password

PASS
```