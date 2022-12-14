import random

def userIdGenerate(role):
    temp_range = range(1000,9999)
    if role ==  'SCI' :
      return 'SCI' + addList(random.sample(temp_range,2))

    if role == 'LAB' :
      return 'LAB' + addList(random.sample(temp_range,2))


def passwordGenerate():
   upper = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

   lower = 'abcdefghijklmnopqrstuvwxyz'

   number = '0123456789'

   symbol = '@#$_&-+!?*/|€¥¢£'

   all = upper + lower + number + symbol

   return ''.join(random.sample(all,9))


def addList(list):
   temp = ''
   for item in list :
      temp += str(item)
   return temp
