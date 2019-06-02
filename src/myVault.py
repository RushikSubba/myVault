import os
import sys
import bcrypt
from pathlib import Path

from . import misc

from .models import Base


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

