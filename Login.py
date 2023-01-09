import os
import time
from Database import session
from Generate import userIdGenerate, passwordGenerate, qnDict
from Database import Admin, Employee, Users
from Admin import AdminCls
from User import User
from style import *
from colorama import init
from Mail import signUpIndicate

init(autoreset=True)


class Login:
    def clear(self):
        val = "cls" if os.name == "nt" else "clear"
        os.system(val)

    # Register user using Employee id
    def register(self):
        self.clear()
        id = input(yellow + "Enter Employee Id... " + normal).strip()
        emp = session.query(Employee).filter(Employee.id == id).first()

        if emp is None:
            self.clear()
            print(red + "Employee id is Not Valid...")
            print()
            return
        elif not emp.isAproved:
            print(
                red
                + "you are Blocked by admin for Some reasons please contact your adminstarator..."
            )
            return
        elif len(emp.user) > 0:
            print(red + "User Already Exists... ")
        else:
            for id, question in qnDict.items():
                print(f"{id} - {question}")

            print("\nSelect security questions for Authendication...")
            try:
                qn_no = int(
                    input(
                        yellow + "Enter anyOne of the scurity qn Id " + normal
                    ).strip()
                )
                ans = input(yellow + "Enter Answer... " + normal).strip()
                if qn_no > 5 and qn_no < 1:
                    raise ValueError
            except ValueError:
                print(red + "Inavlid security question Id")
                return
            user_id = userIdGenerate(emp.role)
            password = passwordGenerate()
            new_user = Users(
                id=user_id,
                password=password,
                role=emp.role,
                qn_no=qn_no,
                answer=ans,
                employee=emp,
            )
            session.add(new_user)
            session.commit()
            self.clear()
            print(f"Generated User id {pink} {user_id}")
            print(f"Generated Password {pink} {password}")
            signUpIndicate(user_id)
            return

    # Employee Login...
    def employeeLogin(self):
        self.clear()
        print(sky_blue + "_______________User Login Page_______________")
        print()
        user_id = input(yellow + "Enter user id " + normal).strip()
        print()
        user = session.query(Users).filter(Users.id == user_id).first()
        if user is None:
            self.clear()
            print(red + "Invalid User ")
            return

        if user.status == False:
            self.clear()
            print(
                red
                + "you are not authorized by admin Please contact your Adminstrator..."
            )
            return
        password = input(yellow + "Enter password... " + normal).strip()

        if password == user.password:
            self.clear()
            print(green + "Successfully Logged...")
            time.sleep(.5)
            print()
            if user.firstLogin:
                print(yellow + "Please change your temp password... ")
                print()
                self.resetPassword(user.id)
                time.sleep(.5)
                print()

            print(f"Welcome back {pink}{user.employee.name}\n")
            userObj = User()
            print()
            userObj.printExpireSamples(user)

            while True:
                print(
                    """

 1 -> Add Samples(Scientist Only)
 2 -> View My Samples(Scientist Only)
 3 -> View all Samples(Scientist and lab assist)
 4 -> Update Samples(Scientist Only)
 5 -> Delete Samples(Scientist Only)
 6 -> Generate Report (scientist and labtech)
 7 -> Logout
          """
                    # add doc string
                )
                try:
                    choice = int(input(yellow + "Enter " + normal).strip())
                except ValueError:
                    self.clear()
                    print(red + "Invalid Input ")
                    continue
                except KeyboardInterrupt:
                    self.clear()
                    print(green + "program sucessfully exited using KeyBoardInterrupt")
                    exit()
                except Exception:
                    self.clear()
                    print(red + "Invalid Input...")
                    continue

                if choice == 1:
                    self.clear()
                    userObj.addSamples(user)
                elif choice == 2:
                    userObj.getMySamples(user)
                elif choice == 3:
                    userObj.getAllSamples(user)
                elif choice == 4:
                    self.clear()
                    userObj.updateSamples(user)
                elif choice == 5:
                    self.clear()
                    userObj.deleteSamples(user)
                elif choice == 6:
                    self.clear()
                    userObj.generateReport(user.id)
                elif choice == 7:
                    self.clear()
                    print(green + "Successfully loggedOut...")
                    time.sleep(.5)
                    return
            else:
                self.clear()
                print(red + "Invalid Choice...")
        else:
            print(red + "Password mismatch...")
            return

    # Admin login
    def adminLogin(self):
        self.clear()
        print(sky_blue + "______________Adminstrator Login______________\n")
        user_id = input(yellow + "Enter Admin Id " + normal).strip()
        print()
        admin = session.query(Admin).filter(Admin.id == user_id).first()
        if admin is None:
            print(red + "Administrator Not Found...\n")
            time.sleep(.5)
            return
        else:
            password = input(yellow + "Enter password... " + normal).strip()
            if admin.password == password:
                print(yellow + "Logging...")
                time.sleep(1)
                self.clear()
                print(green + "sucessfully logged")
                print()
                adminObj = AdminCls()
                print(f"Welcome back Master...{pink}{admin.name}")
                print()
                time.sleep(.5)
                while True:
                    print()
                    print("1 -> unApproved usersList...")
                    print("2 -> All Userslist...")
                    print("3 -> Approve user...")
                    print("4 -> DisApprove user...")
                    print("5 -> Delete user")
                    print("6 -> Add Employee ")
                    print("7 -> show Employee ")
                    print("8 -> Block Employee ")
                    print("9 -> Unblock Employee ")
                    print("10 -> LogOut...\n")

                    try:
                        n = int(input(yellow + "Enter " + normal).strip())
                    except ValueError:
                        self.clear()
                        print(red + "Invalid Input...")
                        continue
                    except KeyboardInterrupt:
                        self.clear()
                        print(
                            green + "program sucessfully exited using KeyBoardInterrupt"
                        )
                        exit()
                    except Exception:
                        self.clear()
                        print(red + "Something Went Wrong")
                        continue

                    if n == 1:
                        adminObj.unApprovedList()
                    elif n == 2:
                        adminObj.allUsersList()
                    elif n == 3:
                        user_id = input(yellow + "Enter user id " + normal).strip()
                        adminObj.approve(user_id)
                    elif n == 4:
                        user_id = input(yellow + "Enter user id " + normal).strip()
                        adminObj.disApprove(user_id)
                    elif n == 5:
                        user_id = input(yellow + "Enter user id " + normal).strip()
                        adminObj.deleteUser(user_id)
                    elif n == 6:
                        adminObj.addEmployee()
                    elif n == 7:
                        adminObj.showEmployee()
                    elif n == 8:
                        emp_id = input(yellow + "Enter emp id " + normal).strip()
                        adminObj.blockEmp(emp_id)
                    elif n == 9:
                        emp_id = input(yellow + "Enter emp id " + normal).strip()
                        adminObj.unblockEmp(emp_id)
                    elif n == 10:
                        self.clear()
                        time.sleep(1)
                        print(green + "Sucessfully LoggedOut")
                        print()
                        return
                    else:
                        print(red + "Invalid Input...")
            else:
                print(red + "password Mismatch...")
                return

    # reset your password using old password...
    def resetPassword(self, user_id):
        user = session.query(Users).filter(Users.id == user_id).first()
        if user is None:
            print(red + "Invalid User Id")
            return
        password = input(yellow + "Enter your Old  password  " + normal).strip()
        # check password authendication...
        if user.password == password:
            print(
                """ * Length must be atleast 8 and maximum 15 
                  * Minimum 1 Capital letter
                  * Minimum 1 Small letter
                  * Minimum 1 numeric and Symbol\n """
            )
            new_pass = input(yellow + "Enter New Password  " + normal).strip()
            # check new passowrd is old password or not
            if user.password == new_pass:
                print(yellow + "It is Old password...")
                self.resetPassword(user_id)
                return
            # check password is valid or not
            res = self.check_pass(new_pass)
            if res:
                user.password = new_pass
                session.commit()
                self.clear()
                print(green + "Password sucessfully Updated")
                if user.firstLogin:
                    user.firstLogin = False
                    session.commit()
                return
            else:
                self.clear()
                print(red + "Not Valid password...")
                self.resetPassword(user_id)
                return

        else:
            self.clear()
            print(red + "Password Mismatch...")
            self.resetPassword(user_id)
            return

    # This method was Deprecated
    def getPassword(self):
        self.clear()
        user_id = input(yellow + "enter user id " + normal).strip()
        user = session.query(Users).filter(Users.id == user_id).first()
        if user is None:
            print(red + "Invalid user Id")
            return
        else:
            print(f"Your password is {user.password}")

    # Forget user password using security question
    def forgetPassword(self, user_id, count=0):
        count += 1
        user = session.query(Users).filter(Users.id == user_id).first()
        if user is None:
            print(red + "Invalid user...")
            return
        qn_no = str(user.qn_no)
        print(f"your security question is : \n\t{qnDict[qn_no]}")

        answer = input(yellow + "Enter your Answer... " + normal).strip()
        if answer == user.answer:
            print(
                """ * Length must be atleast 8 and maximum 15
                  * Minimum 1 Capital letter
                  * Minimum 1 Small letter
                  * Minimum 1 numeric and Symbol\n """
            )
            new_pass = input(yellow + "Enter New Password  " + normal).strip()
            # check password is valid or not
            res = self.check_pass(new_pass)
            if res:
                retype_pass = input(
                    yellow + "Enter your Passoword Again... " + normal
                ).strip()
                if new_pass == retype_pass:
                    user.password = new_pass
                    session.commit()
                    self.clear()
                    print(green + "Password sucessfully Updated")
                else:
                    if count >= 3:
                        print(red + "Too many attempts...")
                        return

                    print(red + "New Password Mismatch...")
                    self.forgetPassword(user_id, count)
                    return
                # if user forget password before first login you must change the firstLogin value == False
                if user.firstLogin:
                    user.firstLogin = False
                    session.commit()
                return
            else:
                self.clear()
                if count >= 3:
                    print(red + "Too many attempts...")
                    return

                print(red + "Not Valid password...")
                self.forgetPassword(user_id, count)
                return

        else:
            self.clear()
            print(red + "Answer is Wrong...")
            print(f"{3-count} attempts left...")
            if count >= 3:
                return
            self.forgetPassword(user_id, count)
            return

    # Check input password is Valid or not
    def check_pass(self, new_pass):
        upper = 0
        lower = 0
        number = 0
        symbol = 0
        if len(new_pass) < 8 or len(new_pass) > 15:
            return False

        for char in new_pass:
            if char.isalpha():
                if char.isupper():
                    upper += 1
                else:
                    lower += 1
            if char in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]:
                number += 1
            if char in [
                "[",
                "@",
                "_",
                "!",
                "#",
                "$",
                "%",
                "^",
                "&",
                "*",
                "(",
                ")",
                "<",
                ">",
                "?",
                "/",
                "|",
                "}",
                "{",
                "~",
                ":",
                "]",
            ]:
                symbol += 1

        if upper > 0 and lower > 0 and number > 0 and symbol > 0:
            return True
        else:
            return False
        #under construction
        def forgetPassOtp(self, user_id):
            user = session.qyery(Users).filter(Users.id == user_id).first()

            if user is None:
                print(red + "Invalid user id ...")
            phoneNo = user.phone_no
            otp, time = auth.generateOtp(phoneNo)

            verifyed = auth.verifyOtp(otp, time)

            if not verifyed:
                return
            else:
                pass
