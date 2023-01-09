import smtplib
from Database import session, Admin,Users

sender = "massprasanth959@gmail.com"
server = smtplib.SMTP("smtp.gmail.com", 587)

server.starttls()
server.login(sender, "gyzcqjloixrrybta")


def signUpIndicate(user_id):
    user = session.query(Users).filter(Users.id == user_id).first()
    admin = session.query(Admin).filter(Admin.id == "shan").first()

    sub = f"Hey {admin.name} New User Arrived!!!"

    body = f"user_id : {user.id}\nemployee_id  : {user.employee.id}\nusername :{user.employee.name}\nuser_role : {user.role}"

    msg = f"Subject : {sub}\n\n{body}"
    try :

        server.sendmail(sender, admin.email,msg)
    except :
      pass

def approveIndicate(user_id):
     user = session.query(Users).filter(Users.id == user_id).first()

     sub = f"Hey {user.employee.name} GoodNews!!!"

     body = "you are now authorized by you administrator so let's add your sample Now!!!"

     msg = f"Subject : {sub}\n\n{body}"
     try :

        server.sendmail(sender, user.employee.email,msg)
     except :
      pass


def disapproveIndicate(user_id):

     user = session.query(Users).filter(Users.id == user_id).first()

     sub = f"Hey {user.employee.name} BadNews!!!"

     body = "oops!!! now you have no rights to login our Sample management system ,Plese contact your adminstartor..."


     msg = f"Subject : {sub}\n\n{body}"
     try :

        server.sendmail(sender, user.employee.email,msg)
     except :
      pass

