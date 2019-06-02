import os
import sys
import bcrypt
from pathlib import Path
from sqlalchemy.orm import sessionmaker

from . import misc
from .models import Base

Session = sessionmaker()
session = None

def new_user():
    Session.configure(bind=Base.engine)
    session = Session()
    details = misc.new_user()
    salt = bcrypt.gensalt()
    details[1] = bcrypt.hashpw(details[1].encode('utf8'), salt)
    new = Base.User(name=details[0], key=salt, master_pass=details[1])
    session.add(new)
    session.commit()
    session.close()


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
