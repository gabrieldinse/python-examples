import re

pattern = "([a-z]+[a-z0-9._]*)@([a-z]+\.[a-z]*\.*[a-z]*)$"
email = input("Enter the email ('q' to quit): ")

while email != 'q':
    match = re.match(pattern, email)
    if match:
        print("{} is a valid email".format(email))
        domain = match.groups()[1]
        print('Domain: {}'.format(domain))
    else:
        print("{} is a invalid email".format(email))
    email = input("\nEnter the email ('q' to quit): ")