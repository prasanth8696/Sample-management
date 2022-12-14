from zifoDatabase import Admin,Users,Employee
from zifoDatabase import session
import os

class ZifoAdmin :
  def clear(self):
    clear_val = 'cls' if os.name == 'nt' else 'clear'
    os.system(clear_val)
  def unApprovedList(self):
      users = session.query(Users).filter(Users.status == False).all()
      if users == [] :
        self.clear()
        print("Currently no unapproved users")
        return
      self.clear()
      print('__________unapproved list______________')
      print()
      print('User_Id     Employee_Id     Name      role    status ')
      print()
      for user in users :
          print((user.id).ljust(14) ,end='')
          print((user.employee.id).ljust(14),end='')
          print((user.employee.name).ljust(14),end='')
          print((user.role).ljust(14),end='')
          status = 'Approved' if user.status else 'Unapproved'
          print((status).ljust(14),end='')
          print()
      print()
      print()

  def allUsersList(self):
      approvedUsers = 0;unapprovedUsers = 0
      users = session.query(Users).all()
      if users :
        self.clear()
        print('__________Users list______________')
        print()
        print('User_Id     Employee_Id     Name      role    status ')
        print()
        for user in users :
            if user.status == True :
               approvedUsers += 1
            else :
               unapprovedUsers += 1

            print((user.id).ljust(14) ,end='')
            print((user.employee.id).ljust(14),end='')
            print((user.employee.name).ljust(14),end='')
            print((user.role).ljust(14),end='')
            status = 'Approved' if user.status else 'Unapproved'
            print((status).ljust(14),end='')
            print()
        print()
        print()
        totalUsers = len(users)
        print(f'Total Users = {totalUsers}')
        print(f'Approved Users = {approvedUsers}')
        print(f'unApproved Users = {unapprovedUsers}')

      else :
       self.clear()
       print('Currently No users...')



  def addEmployee(self):
     self.clear()
     emp_id = input('Enter Emoloyee id ')
     emps = session.query(Employee).filter(Employee.id == emp_id).first()
     if emps is not None :
       self.clear()
       print('Employee Already Exists...')
       return
     name = input('Enter name ')
     email = input('Enter your Email ')
     dob = input('Enter Date Of Birth ')
     role = input('Enter Role ').upper()
     emp = Employee(
           id = emp_id,
           name = name,
           email = email,
           dob = dob,
           role = role,
           isAproved = False
      )
     session.add(emp)
     session.commit()
     print('Employee added sucessfully... ')






  def approve(self,id):
    self.clear()
    user =  session.query(Users).filter(Users.id == id).first()
    if user is None:
     print('User Not Found...')
     return
    if user.status :
       print('User is Already in Approved List... ')
    else :
       user.status = True
       session.commit()
       print('User approved sucessfully... ')
       return


  def disApprove(self,id):
    self.clear()
    user =  session.query(Users).filter(Users.id == id).first()
    if user is None:  
      print('User Not Found...')  
      return
    if user.status:
        user.status = False
        session.commit()
        print('User disapproved Successfully')
       
    else :
       print('User Already no Access...')
       return




  def deleteUser(self,id):
   self.clear()
   user = session.query(Users).filter(Users.id == id).first()
   if user is not None :
     session.delete(user)
     session.commit()
     print('User Sucessfully deleted.... ')
     return
   else :
     print('User Not Found...')
     return
