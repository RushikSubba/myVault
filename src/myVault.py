import os
import sys
import bcrypt
import sqlite3
import time
import random

from pathlib import Path
from sqlalchemy.orm import sessionmaker
from sqlalchemy import exc
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from base64 import b64encode, b64decode

from . import misc
from .models import Base

# session initialization
Session = sessionmaker()
global_var = {'session' : None,
              'user_id' : None,
              'key'     : None,
              'salt'    : None
            }

def initialize():
    create_session()

def create_session():
    #initialze engine and a session object
    Session.configure(bind=Base.engine)
    global_var['session'] = Session()

def new_user():

    while True:
        try:
            details = misc.user()

            # create encryption key from master password
            global_var['salt'] = bcrypt.gensalt()
            global_var['key'] = bcrypt.kdf(details[1].encode(), global_var['salt'], 16, 100)
            details[1] = bcrypt.hashpw(details[1].encode('utf8'), global_var['salt'])
            
            new = Base.User(name=details[0], key=global_var['salt'], master_pass=details[1])
            global_var['session'].add(new)
            global_var['session'].commit()

            # get user_id
            for id, in global_var['session'].query(Base.User.id).filter(Base.User.name == details[0]):
                global_var['user_id'] = int(id)
            
            print('\n $ Welcome ' + details[0] + '\n')
            break
        except (exc.IntegrityError, sqlite3.IntegrityError) :
            global_var['session'].rollback()
            global_var['session'] = Session()
            print(' $ Username already exists! Please Enter again')
            
def existing_user():
    while True:
        # get input and verify
        # if verified user then initialze global vasiables
        details = misc.user()
        result = global_var['session'].query(Base.User).filter(Base.User.name == details[0])
        temp = None
        for row in result:
            global_var['user_id'] = int(row.id)
            global_var['salt'] = row.key
            temp = row.master_pass
        if global_var['user_id'] == None:
            print('Username does not exist please create a new account')
            new_user()
            return
        else :
            t = details[1]
            details[1] = bcrypt.hashpw(details[1].encode('utf8'), global_var['salt'])
            if(not temp == details[1]):
                print('Invalid password')
            else :
                global_var['key'] = bcrypt.kdf(t.encode(), global_var['salt'], 16, 100)
                t = None
                os.system('cls' if os.name=='nt' else 'clear')
                print('\n $ Welcome ' + details[0] + '\n')
                break


def quit():
    if not (global_var == None and global_var['session'] == None):
        global_var['session'].close()
        global_var['user_id'] = None
        global_var['key'] = None
        global_var['salt'] = None
    sys.exit()

def add_new():
    # add a new password
    while True:
        try:
            details = misc.add()
            details[3] = encrypt(details[3])
            details[4] = encrypt(details[4])
            new = Base.passwords(user_id=global_var['user_id'], name=details[0], url=details[1], login=details[2], password=details[3], notes=details[4])
            global_var['session'].add(new)
            global_var['session'].commit()
            break
        except (exc.IntegrityError, sqlite3.IntegrityError):
            print('Invalid User id')

def encrypt(pt):
    cipher = AES.new(global_var['key'], AES.MODE_CBC, global_var['key'])
    ct = cipher.encrypt(pad(pt.encode(), AES.block_size))
    
    return ct

def decrypt(ct):
    cipher = AES.new(global_var['key'], AES.MODE_CBC, global_var['key'])
    pt = unpad(cipher.decrypt(ct), AES.block_size)
    
    return pt

def show_all():
    # show all records in passwords table for the user
    result = global_var['session'].query(Base.passwords).filter(Base.passwords.user_id == global_var['user_id'])
    print("  S.No\tName" + " "*11 + "URL" + " "*22 + "Login")
    print("  ____________________________________________________________________________________________________")
    ctr = 1
    for row in result:
        print("  " +str(ctr) + "\t" + row.name + " "*(15 - len(row.name)) + row.url + " "*(25 - len(row.url)) + row.login)
        ctr = ctr + 1
    print()

def search():
    # search according to website names
    print(' $ Enter search : ', end=" ")
    req = input()
    print()
    result = global_var['session'].query(Base.passwords).filter(Base.passwords.user_id == global_var['user_id'], Base.passwords.name.ilike("%" + req + "%"))
    print("  S.No\tName" + " "*11 + "URL" + " "*22 + "Login")
    print("  ____________________________________________________________________________________________________")
    ctr = 1
    for row in result:
        print("  " + str(ctr) + "\t" + row.name + " "*(15 - len(row.name)) + row.url + " "*(25 - len(row.url)) + row.login)
        ctr = ctr + 1
    print()

def remove():
    #remove according to website names
    print(' $ Enter website name to be removed :', end=" ")
    req = input()
    print(' $ Enter login to be removed : ', end=" ")
    login = input()
    global_var['session'].query(Base.passwords).filter(Base.passwords.user_id == global_var['user_id'], Base.passwords.name == req, Base.passwords.login == login).delete()
    global_var['session'].commit()

def show():
    # print password for a given amount of time and then hide
    print(' $ Enter website name :', end=" ")
    name = input()
    print(' $ Enter login :', end=" ")
    login = input()
    decide = None
    while True:
        print(' $ Do you want notes or password[n/p] ? :', end=" ")
        decide = input()
        if decide == 'p' or decide == 'n':
            break
        else :
            print(' $ Invalid option press p for password n for notes')
    result = global_var['session'].query(Base.passwords).filter(Base.passwords.user_id == global_var['user_id'], Base.passwords.name == name, Base.passwords.login == login)
    data = None
    for row in result:
        if decide == 'p':
            data = row.password
        else :
            data = row.notes
    if data == None:
        print('$ No such entry')
    else :
        data = decrypt(data).decode()
        print('$ Password/Notes will be show only for 10 seconds!!!')
        start = time.time()
        while(time.time() - start <= 10):
            time.sleep(0.1)
            print('$ Password/Notes : ' + data, end='\r')
        print('$ Password/Notes : ' +  "*"*(len(data) + random.randint(1, 5)))
        data = None
            

def main():
    # greet 
    os.system('cls' if os.name=='nt' else 'clear')
    misc.greet()
    
    # initialize
    initialize()

    # if db not created created db
    BASE_DIR = os.path.dirname(os.path.realpath(__file__))
    db_file = Path(BASE_DIR + "/myVault.db")
    if not os.path.exists(db_file):
        Base.Base.metadata.create_all(Base.engine)

    # welcome options
    s = misc.welcome_options()
    if s == 'q':
        sys.exit()
    elif s == 'n':
        new_user()
    else :
        existing_user()

    # app 'run' state
    while True:
        s = misc.options()
        if s == 'q':
            quit()
        elif s == 'a':
            add_new()
        elif s == 'all':
            show_all()
        elif s == 's':
            search()
        elif s == 'r':
            remove()
        else :
            show()
