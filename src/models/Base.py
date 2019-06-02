from sqlalchemy import create_engine, Column, String, Integer, BLOB, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///./myVault.db')

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    key = Column(String)
    master_pass = Column(String)

    def __repr__(self):
        return "<User(id='%s', name='%s', key='%s', master_pass='%s')" %(
            self.id, self.name, self.key, self.master_pass)

class passwords(Base):
    __tablename__ = 'passwords'


    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey(User.id))
    name = Column(String)
    url = Column(String)
    login = Column(String)
    password = Column(String)
    notes = Column(BLOB)

    user = relationship('User', foreign_keys='passwords.user_id', lazy='joined')

    def __repr__(self):
        return "<passwords(user_id='%s', name='%s', url='%s', login='%s')>" % (
            self.user_id, self.name, self.url, self.login)

if __name__ == "__main__":
    Base.metadata.create_all(engine)