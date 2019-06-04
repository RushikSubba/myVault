import getpass

def greet():
    print("\n\nWelecome to myVault an app to securely store and manage passwords\n\n")

def welcome_options():
    while True:
        print("(e)xisting user  (n)ew user  (q)uit\n")
        s = input(' $ ')
        if s == 'q' or s == 'e' or s == 'n':
            return s
        else :
            print('\n $ Invalid option\n')

def user():
    print("\n $ Please enter your username :", end=" ")
    username = input()
    print()
    password = getpass.getpass(prompt=' $ Enter master key : ')
    print()
    return [username, password]

def options():
    while True:
        print("\n (a)dd    (r)emove    show(all)    (show)    (s)arch    (q)uit\n")
        s = input(' $ ')
        if s == 'a' or s == 'r' or s == 'all' or s == 's' or s == 'q' or s == 'show':
            return s
        else :
            print('\n $ Invalid option\n')

def add():
    details = []
    print('\n $ Name :', end=" ")
    n = input()
    details.append(n)
    print(' $ URL :', end=" ")
    n = input()
    details.append(n)
    print(' $ Login :', end=" ")
    n = input()
    details.append(n)
    n = getpass.getpass(' $ Password : ')
    details.append(n)
    print(' $ Notes :', end=" ")
    n = input()
    details.append(n)

    return details
    