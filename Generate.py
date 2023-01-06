import random

# automatic user id generation...
def userIdGenerate(role):
    temp_range = range(1000, 9999)
    if role == "SCI":
        return "SCI" + addList(random.sample(temp_range, 2))

    if role == "LAB":
        return "LAB" + addList(random.sample(temp_range, 2))


# automatic temp password generation...
def passwordGenerate():
    upper = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    lower = "abcdefghijklmnopqrstuvwxyz"

    number = "0123456789"

    symbol = "@#$_&-+!?*/|€¥¢£"

    all = upper + lower + number + symbol

    return "".join(random.sample(all, 9))


def addList(list):
    temp = ""
    for item in list:
        temp += str(item)
    return temp


qnDict = {
    "1": "In what city were you born?",
    "2": "What is your favorite movie?",
    "3": "What is your pet name?",
    "4": "What is the first name of your first boyfriend/girlfriend?",
    "5": "What was the name of your first grade teacher?",
}
