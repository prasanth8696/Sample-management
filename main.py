import os
from Login import Login
from style import *
from colorama import init

init(autoreset=True)


clear_val = "cls" if os.name == "nt" else "clear"
clear = lambda: os.system(clear_val)
clear()
sms = Login()


def main():
    print()
    print(sky_blue + "__________Zifo Sample Management System___________")
    print()

    print("1 -> User Registration")
    print("2 -> User Sign in ")
    print("3 -> Admin Signin ")
    print("4 -> reset Password ")
    print("5 -> Forget Password ")
    print("6 -> Forget Username ")
    print("7 -> Exit  ")
    try:
        choice = int(input(yellow + "Enter " + normal).strip())
    except ValueError:
        clear()
        print(red + "Invalid Input...")
        main()
        return
    except KeyboardInterrupt:
        clear()
        print(green + "program sucessfully exited using KeyBoard Interrupt")
        exit()
    except Exception:
        clear()
        print(red + "Something went wrong")
        main()
        return

    if choice == 1:
        sms.register()

    elif choice == 2:
        sms.employeeLogin()
    elif choice == 3:
        sms.adminLogin()
    elif choice == 4:
        user_id = input(yellow + "enter user Id " + normal).strip()
        clear()
        sms.resetPassword(user_id)
    elif choice == 5:
        user_id = input(yellow + "enter user Id " + normal).strip()
        print("1 - OTP Authendication ")
        print("2 - Security question ")
        val = int(input(yellow + "Enter ").strip())
        if val == 2:
            clear()
            sms.forgetPassword(user_id)
        else:
            clear()
            sms.forgetPassOtp(user_id)
    elif choice == 6:
        pass
    elif choice == 7:
        clear()
        print(green + " program Sucessfully terminated...")
        print("                         Developed by" + red + " Shan....")
        exit()

    else:
        print(red + "Invalid Input")


if __name__ == "__main__":
    while True:
        main()
