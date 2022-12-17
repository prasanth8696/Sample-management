import os
import time
from zifoDatabase import session
from zifoGenerate import userIdGenerate,passwordGenerate,qnDict
from zifoDatabase import Admin,Employee,Users
from zifoAdmin import ZifoAdmin
from zifoUser import ZifoUser
class ZifoLogin :
  def clear(self):
     val = 'cls' if os.name == 'nt' else 'clear'
     os.system(val)


  def register(self) :
    self.clear()
    id = input('Enter Employee Id... ')
    emp = session.query(Employee).filter(Employee.id == id).first()

    if emp is None :
      self.clear()
      print('Employee id is Not Valid...')
      print()
      return
    elif not  emp.isAproved :
       print('you are Blocked by admin for Some reasons please contact your adminstarator...')
       return
    elif len(emp.user) > 0 :
      print('User Already Exists... ')
    else :
      for id,question in qnDict.items() :
        print(f'{id} - {question}')
      
      print('\nSelect security questions for Authendication...')
      try :
        qn_no = int(input('Enter anyOne scurity qn Id '))
        ans = input('Enter Answer... ')
        if qn_no > 5 and qn_no < 1 :
           raise ValueError
      except ValueError :
        print('Inavlid security question Id')
        return
      user_id = userIdGenerate(emp.role)
      password = passwordGenerate()
      new_user = Users(
            id = user_id,
            password = password,
            role = emp.role,
            qn_no = qn_no,
            answer = ans,
            employee = emp
           )
      session.add(new_user)
      session.commit()
      print(f'Generated User id {user_id}')
      print(f'Generated Password {password}')
      return


  def employeeLogin(self):
     self.clear()
     print('_______________User Login Page_______________')
     print()
     user_id = input('Enter user id ')
     print()
     user = session.query(Users).filter(Users.id == user_id).first()
     if user is None :
       self.clear()
       print('Invalid User ')
       return

     if user.status == False :
        self.clear()
        print('you are not authorized by admin Please contact your Adminstrator...')
        return
     password = input('Enter password... ')

     if password == user.password :
        self.clear()
        print('Successfully Logged...')
        time.sleep(1.5)
        print()
        if user.firstLogin :
          print('Please change your temp password... ')
          print()
          self.resetPassword(user.id)
          time.sleep(1)
          print()



        print(f'Welcome back {user.employee.name}\n')
        userObj = ZifoUser()
        print()
#        printExpireSamples(user)

        while(True) :
         print(
          '''

 1 -> Add Samples(Scientist Only)
 2 -> View My Samples(Scientist Only)
 3 -> View all Samples(Scientist and lab assist)
 4 -> Update Samples(Scientist Only)
 5 -> Delete Samples(Scientist Only)
 6 -> Logout
          '''
          #add doc string
              )
         try :
            choice = int(input('Enter '))
         except ValueError :
             self.clear()
             print('Invalid Input ')
             continue
         except Exception :
             self.clear()
             print('Invalid Input...')
             continue

         if choice == 1 :
           self.clear()
           userObj.addSamples(user)
         elif choice == 2 :
           userObj.getMySamples(user)
         elif choice == 3 :
           userObj.getAllSamples(user)
         elif choice == 4 :
           self.clear()
           userObj.updateSamples(user)
         elif choice == 5 :
           self.clear()
           userObj.deleteSamples(user)
         elif choice == 6 :
           self.clear()
           print('Successfully loggedOut...')
           time.sleep(1)
           return
        else :
           self.clear()
           print('Invalid Choice...')
     else:
        print('Password mismatch...')
        return


  def adminLogin(self):
     self.clear()
     print('______________Adminstrator Login______________')
     print()
     user_id = input('Enter Admin Id ')
     print()
     admin = session.query(Admin).filter(Admin.id == user_id).first()
     if admin is None :
       print('Administrator Not Found...')
       print()
       time.sleep(1.5)
       return
     else :
        password = input('Enter password... ')
        if admin.password == password :
            print('Logging...')
            time.sleep(2)
            self.clear()
            print('sucessfully logged')
            print()
            adminObj = ZifoAdmin()
            print(f'Welcome back Master...{admin.name}')
            print()
            time.sleep(1)
            while(True) :
             print()
             print('1 -> unApproved usersList...')
             print('2 -> All Userslist...')
             print('3 -> Approve user...')
             print('4 -> DisApprove user...')
             print('5 -> Delete user')
             print('6 -> Add Employee ')
             print('7 -> show Employee ')
             print('8 -> Block Employee ')
             print('9 -> Unblock Employee ')
             print('10 -> LogOut...\n')

             try :
                n = int(input('Enter '))
             except ValueError :
               self.clear()
               print('Inavalid Input...')
               continue
             except Exception :
               self.clear()
               print('Something Went Wrong')
               continue

             if n == 1 :
               adminObj.unApprovedList()
             elif n == 2 :
               adminObj.allUsersList()
             elif n == 3 :
                user_id = input('Enter user id ')
                adminObj.approve(user_id)
             elif n == 4 :
                user_id = input('Enter user id ')
                adminObj.disApprove(user_id)
             elif n == 5 :
                 user_id = input('Enter user id ')
                 adminObj.deleteUser(user_id)
             elif n == 6 :
                 adminObj.addEmployee()
             elif n == 7 :
                 adminObj.showEmployee()
             elif n == 8 :
                 emp_id = input('Enter emp id ')
                 adminObj.blockEmp(emp_id)
             elif n == 9 :
                 emp_id = input('Enter emp id ')
                 adminObj.unblockEmp(emp_id)
             elif n == 10 :
                  self.clear()
                  time.sleep(1)
                  print('Sucessfully LoggedOut')
                  print()
                  return
             else :
                print('Invalid Input...')
        else :
           print('password Mismatch...')
           return



  def resetPassword(self,user_id):
      user = session.query(Users).filter(Users.id == user_id).first()
      if user is None :
       print('Invalid User Id')
       return
      password = input('Enter your Old  password  ')
      #check password authendication...
      if user.password == password :
          print(
              ''' * Length must be atleast 8 and maximum 15 
                  * Minimum 1 Capital letter
                  * Minimum 1 Small letter
                  * Minimum 1 numeric and Symbol\n '''
                )
          new_pass = input('Enter New Password  ')
          # check new passowrd is old password or not
          if user.password == new_pass :
            print('It is Old password...')
            self.resetPassword(user_id)
            return
          # check password is valid or not
          res = self.check_pass(new_pass)
          if res :
            user.password = new_pass
            session.commit()
            self.clear()
            print('Password sucessfully Updated')
            if user.firstLogin :
              user.firstLogin = False
              session.commit()
            return
          else :
            self.clear()
            print('Not Valid password...')
            self.resetPassword(user_id)
            return

      else :
          self.clear()
          print('Password Mismatch...')
          self.resetPassword(user_id)
          return
#This method was Deprecated 
  def getPassword(self) :
     self.clear()
     user_id = input('enter user id ')
     user = session.query(Users).filter(Users.id == user_id).first()
     if user is None :
       print('Inavlid user Id')
       return
     else :
        print(f'Your password is {user.password}')



  def forgetPassword(self,user_id,count = 0) :
     count += 1
     user = session.query(Users).filter(Users.id == user_id).first()
     if user is None :
       print('Invalid user...')
       return
     qn_no = str(user.qn_no)
     print(f'your security question is : \n\t{qnDict[qn_no]}')
     answer = input('Enter your Answer... ')
     if answer == user.answer :
          print(
              ''' * Length must be atleast 8 and maximum 15
                  * Minimum 1 Capital letter
                  * Minimum 1 Small letter
                  * Minimum 1 numeric and Symbol\n '''
                )
          new_pass = input('Enter New Password  ')
          # check password is valid or not
          res = self.check_pass(new_pass)
          if res :
            retype_pass = input('Enter your Passoword Again... ')
            if new_pass == retype_pass :
              user.password = new_pass
              session.commit()
              self.clear()
              print('Password sucessfully Updated')
            else :
              if count >= 3 :
                print('Too many attempts...')
                return

              print('New Password Mismatch...')
              self.forgetPassword(user_id,count)
              return
#if user forget password before first login you must change the firstLogin value == False
            if user.firstLogin :
              user.firstLogin = False
              session.commit()
            return
          else :
            self.clear()
            if count >= 3:
              print('Too many attempts...')
              return

            print('Not Valid password...')
            self.forgetPassword(user_id,count)
            return

     else :
          self.clear()
          print('Answer is Wrong...')
          print(f'{3-count} attempts left...')
          if count >= 3 :
            return
          self.forgetPassword(user_id,count)
          return

  def check_pass(self,new_pass):
     upper = 0;lower = 0;number = 0;symbol = 0
     if len(new_pass) < 8 or len(new_pass) > 15 :
       return False

     for char in new_pass:
        if char.isalpha():
          if char.isupper():
            upper += 1
          else :
            lower += 1
        if char in ['0','1','2','3','4','5','6','7','8','9'] :
           number += 1
        if char in ['[','@','_','!','#','$','%','^','&','*','(',')','<','>','?','/','|','}','{','~',':',']'] :
            symbol += 1

     if upper > 0 and lower > 0 and number > 0 and symbol > 0 :
        return True
     else :
        return False
