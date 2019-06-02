import getpass

def greet():
    print("\n\nWelecome to myVault an app to securely store and manage passwords\n\n")

def welcome_options():
    while True:
        print("(e)xisting user  (n)ew user  (q)uit\n")
        s = input(' $ ')
        if s == 'q' or s == 'e' or s == 'n':
            return s

def new_user():
    print("\nWelcome please enter your username :", end=" ")
    username = input()
    print()
    password = getpass.getpass(prompt='Enter a master key : ')
    print()
    return [username, password]

    