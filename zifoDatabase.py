from sqlalchemy import create_engine,Column,String,Boolean,ForeignKey,DateTime,Integer

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import sessionmaker,relationship





SQL_ALCHEMY_DATABASE_URL = 'sqlite:///./zifoDatabase.db'

engine = create_engine(SQL_ALCHEMY_DATABASE_URL)

sessionlocal = sessionmaker(autocommit = False,autoflush = False,bind = engine)

Base = declarative_base()


session = sessionlocal()

#Base.metadata.create_all(bind=engine)


class Employee(Base) :
   __tablename__ = 'employee'
   id = Column(String(50),primary_key = True)
   name = Column(String(50),nullable=False)
   email = Column(String(50),nullable=True)
   dob = Column(String(50),nullable=True)
   role = Column(String(50),nullable=False)
   isAproved = Column(Boolean ,default = True)
   user = relationship('Users',back_populates='employee')

class Users(Base) :
  __tablename__ = 'user'
  id = Column(String(50),primary_key = True)
  password = Column(String(50),nullable=False)
  role = Column(String(50))
  status = Column(Boolean,default = False)
  firstLogin = Column(Boolean,default = True)
  employee_id = Column(String(50),ForeignKey('employee.id'))
  employee = relationship('Employee',back_populates='user')
  samples = relationship('Sample',back_populates='author')




class Admin(Base) :
   __tablename__ = 'admin'
   id = Column(String(50),primary_key = True)
   name = Column(String(50),nullable=False)
   password = Column(String(50),nullable=False)

class Sample(Base) :
   __tablename__ = 'sample'
   id = Column(Integer,primary_key = True)
   reactive = Column(Boolean,nullable=False)
   entry_date = Column(DateTime,nullable=False)
   expire_date = Column(DateTime,nullable=False)
   author_id = Column(String(50),ForeignKey('user.id'))
   author = relationship('Users',back_populates='samples')

Base.metadata.create_all(bind=engine)

if __name__ == '__main__' :
  admin = session.query(Admin).all()
  if len(admin) == 0 :
     new_admin = Admin(
               id = 'shan',
               name = 'prashanth',
               password = '12345'
       )
     session.add(new_admin)
     session.commit()
     print('Default admin added...')
