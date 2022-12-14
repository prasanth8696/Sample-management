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
  print('5 -> Get your password(this feature will deprecate in future ')
  print('6 -> Exit ')

  choice = int(input('Enter '))

  if choice == 1:
     sms.register()

  elif choice == 2 :
     sms.employeeLogin()
  elif choice == 3 :
     sms.adminLogin()
  elif choice == 4 :
     sms.resetPassword()
  elif choice == 5 :
     sms.getPassword()
  elif choice == 6 :
     exit()

  else :
    print('Invalid Input')



if __name__ == '__main__' :
  while(True) :
     main()
