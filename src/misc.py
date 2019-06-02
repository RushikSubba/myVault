def greet():
    print("\n\nWelecome to myVault an app to securely store and manage passwords\n\n")

def welcome_options():
    while True:
        print("(e)xisting user  (n)ew user  (q)uit\n")
        s = input(' $ ')
        if s == 'q' or s == 'e' or s == 'n':
            return s

    