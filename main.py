import os
from zifoLogin import ZifoLogin



clear_val = 'cls' if os.name == 'nt' else 'clear'
clear = lambda : os.system(clear_val)
clear()
sms =ZifoLogin()
def main() :
  print()
  print('__________Zifo Sample Management System___________')
  print()

  print('1 -> User Registration')
  print('2 -> User Sign in ')
  print('3 -> Admin Signin ')
  print('4 -> reset Password ')
  print('5 -> Forget Password ')
  print('6 -> Exit ')
  try :
     choice = int(input('Enter '))
  except ValueError :
     clear()
     print('Inavalid Input...')
     main()
     return
  except Exception :
     clear()
     print('Something went wrong')
     main()
     return

  if choice == 1:
     sms.register()

  elif choice == 2 :
     sms.employeeLogin()
  elif choice == 3 :
     sms.adminLogin()
  elif choice == 4 :
     user_id = input('enter user Id ')
     clear()
     sms.resetPassword(user_id)
  elif choice == 5 :
     user_id = input('enter user Id ')
     clear()
     sms.forgetPassword(user_id)
  elif choice == 6 :
     clear()
     print(' program Sucessfully terminated...')
     exit()

  else :
    print('Invalid Input')



if __name__ == '__main__' :
  while(True) :
     main()
