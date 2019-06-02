import os
import sys
import bcrypt
from pathlib import Path
from sqlalchemy.orm import sessionmaker
from sqlalchemy import exc

from . import misc
from .models import Base

# session initialization
Session = sessionmaker()
global_var = {'session' : None,
              'user_id' : None
            }

def create_session():
    Session.configure(bind=Base.engine)
    global_var['session'] = Session()

def new_user():
    # create a session and add details to databse
    create_session()

    # does not work perfectly !
    while True:
        try:
            details = misc.new_user()
            salt = bcrypt.gensalt()

            details[1] = bcrypt.hashpw(details[1].encode('utf8'), salt)
            new = Base.User(name=details[0], key=salt, master_pass=details[1])
            
            global_var['session'].add(new)
            break
        except exc.IntegrityError :
            global_var['session'].rollback()
            global_var['session'] = Session()
            print('Username already exists! Please Enter again')
        else :
            global_var['session'].commit()
    


def main():
    # greet 
    os.system('cls' if os.name=='nt' else 'clear')
    misc.greet()
    
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




    if not global_var['session'] == None:
        global_var['session'].close()
