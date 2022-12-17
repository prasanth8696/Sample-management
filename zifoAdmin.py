from zifoDatabase import Admin,Users,Employee
from zifoDatabase import session
import os
from style import *
from colorama import init
init(autoreset=True)

class ZifoAdmin :
  #console refresh
  def clear(self):
    clear_val = 'cls' if os.name == 'nt' else 'clear'
    os.system(clear_val)
  #print unapproved users
  def unApprovedList(self):
      users = session.query(Users).filter(Users.status == False).all()
      if users == [] :
        self.clear()
        print(red + "Currently no unapproved users")
        return
      self.clear()
      print(sky_blue + '_____________unapproved list______________')
      print()
      print('User_Id     Employee_Id     Name      role    status ')
      print()
      for user in users :
          print((user.id).ljust(14) ,end='')
          print((user.employee.id).ljust(14),end='')
          print((user.employee.name).ljust(14),end='')
          print((user.role).ljust(14),end='')
          print(red + 'Unapproved'.ljust(14),end='')
          print()
      print()
      print()
      session.close()
  #print all unapproved and approved users
  def allUsersList(self):
      approvedUsers = 0;unapprovedUsers = 0
      users = session.query(Users).all()
      if users :
        self.clear()
        print(sky_blue + '___________________Users list_____________________')
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
            status = green+'Approved' if user.status else red+'Unapproved'
            print((status).ljust(14),end='')
            print()
        print()
        print()
        totalUsers = len(users)
        print(f'Total Users = {totalUsers}')
        print(f'Approved Users = {approvedUsers}')
        print(f'unApproved Users = {unapprovedUsers}')
        session.close()

      else :
       self.clear()
       print(green + 'Currently No users...')


  # add employee in database
  def addEmployee(self):
     self.clear()
     emp_id = input(yellow + 'Enter Emoloyee id '+ normal)
     emps = session.query(Employee).filter(Employee.id == emp_id).first()
     if emps is not None :
       self.clear()
       print(green + 'Employee Already Exists...')
       return
     name = input(yellow + 'Enter name '+ normal)
     email = input(yellow + 'Enter your Email ' + normal)
     dob = input(yellow + 'Enter Date Of Birth '+ normal)
     role = input(yellow + 'Enter Role ' + normal).upper()
     emp = Employee(
           id = emp_id,
           name = name,
           email = email,
           dob = dob,
           role = role
      )
     session.add(emp)
     session.commit()
     session.close()
     print(green + 'Employee added sucessfully... ')





  # Approve users
  def approve(self,id):
    self.clear()
    user =  session.query(Users).filter(Users.id == id).first()
    if user is None:
     print(red + 'User Not Found...')
     return
    if user.status :
       print(red + 'User is Already in Approved List... ')
    else :
       user.status = True
       session.commit()
       session.close()
       print(green + 'User approved sucessfully... ')
       return

  # Disapprove users
  def disApprove(self,id):
    self.clear()
    user =  session.query(Users).filter(Users.id == id).first()
    if user is None:  
      print(red + 'User Not Found...')  
      return
    if user.status:
        user.status = False
        session.commit()
        session.close()
        print(green + 'User disapproved Successfully')
       
    else :
       print(red + 'User Already no Access...')
       return



  # Delete users
  def deleteUser(self,id):
   self.clear()
   user = session.query(Users).filter(Users.id == id).first()
   if user is not None :
     emp = session.query(Employee).filter(Employee.id == user.employee.id).first()
     emp.isAproved = False
     session.delete(user)
     session.commit()
     session.close()
     print(green + 'User Sucessfully deleted.... ')
     return
   else :
     print(red + 'User Not Found...')
     return

  #Block specified employee
  def blockEmp(self,id) :
     self.clear()
     emp = session.query(Employee).filter(Employee.id == id).first()
     if emp is None :
       print(red + 'Invalid Employee id...')
       return
     elif not emp.isAproved :
       print(red + 'Already blocked user...')
       return
     else :
       emp.isAproved = False
       if emp.user :
         emp.user[0].status = False
       session.commit()
       session.close()
       print(green + 'Employee blocked sucessfully...')
  #Unblock Specified Emoloyee
  def unblockEmp(self,id) :
     self.clear()
     emp = session.query(Employee).filter(Employee.id == id ).first()
     if emp is None :
       print(red + 'Invalid Employee id...')
       return
     elif emp.isAproved :
       print(red + 'Already Normal user...')
       return
     else :
       emp.isAproved = True
       if emp.user :
         emp.user[0].status = True
       session.commit()
       session.close()
       print(green + 'Employee unblocked sucessfully...')


  #Show Employee nessesary details
  def showEmployee(self) :
     self.clear()
     emps = session.query(Employee).all()
     if emps is None :
        print(green + 'No employee available in our database...')
        return
     print(sky_blue + '______________Employee List________________\n')
     print('Emp_id       name        status         user_id'  )
     for emp in emps :
         print(emp.id.ljust(9),end='')
         print(emp.name.ljust(15),end='')
         status = green + 'Normal' if emp.isAproved else red + 'Blocked'
         print(status.ljust(18),end='')
         if emp.user :
            print(emp.user[0].id.ljust(15),end='')
         else :
           print('None'.ljust(15),end='')
         print('\n')
     print('\n')







