from twilio.rest import  Client
import os
import random
import datetime
from colorama import init
from style import *

init(autoreset=True)

class Auth:

	def __init__(self,account_sid,api_token):
           self.client = Client(account_sid,api_token)
           self.otp = None
	def clear(self):
          clear_val = 'cls' if os.name == 'nt' else 'clear' 
          os.system(clear_val)

	async def generateOtp(self,phoneNo):
             otp = random.randint(1000000,999999)
             try :
               message = self.client.message.create(
                  from = '+15086259864',
                  to = '+91'+ phoneNo,
                  body = f"Your verification Code is : {otp}.\nValid only 10 minutes."
                )
              except :
   	         self.clear()
                 print (red + "Invalid PhoneNo...")
   	         return
              return otp,datetime.datetime.now()

	def verifyOtp(self,otp,time):
            self.clear()
            user_otp = input(yellow + 'Enter verification code... ')
            if(user_otp == str(otp)) :
               if((datetime.datetime.now() - time)< 10) :
                   return True
               else :
                 print(red + 'OTP EXPIRED...')
                 return False
            else :
               print(red + 'Invalid OTP... ')
               self.verifyOtp(otp)
               return True




