#!/usr/bin/python3
import sqlite3
import getpass
from encrypt import caesar


# Connects to db. Creates file if it doesn't exist.
userList = sqlite3.connect('../userList.db')
cursor = userList.cursor()
cursor.execute(
    """create table if not exists users (
        userName text PRIMARY KEY NOT NULL, 
        password text NOT NULL,
        lastLogin text,
        previousLogin text)""")

def insertUser(name, passwd):
    cursor.execute(
        """
        INSERT INTO users
        (userName, password, lastLogin, previousLogin)
        VALUES ('{0}', '{1}', 'NULL', 'NULL')
        """.format(name.title(),passwd))

    userList.commit()

# cursor.execute("""SELECT a FROM users WHERE id = '1'""")
# row = cursor.fetchall()
# print(str(row).strip('[]()\','))

def cleanReturn(value):
    val2 = str(value).strip('[]()\',')
    return val2

def queryUser(name):
    cursor.execute(
        """SELECT userName FROM users WHERE userName = '{}'""".format(name)
    )
    uName = cursor.fetchall()
    return cleanReturn(uName)
def queryPass(name, passw):
    cursor.execute(
        """SELECT password FROM users WHERE userName = '{}'""".format(name)
    )
    uPass = cursor.fetchall()
    return cleanReturn(uPass)
def queryLogin(name):
    cursor.execute(
        """SELECT previousLogin FROM users WHERE userName = '{}'""".format(name)
    )
    uLogin = cursor.fetchall()
    return cleanReturn(uLogin)
def updateLogin(name):
    cursor.execute(
        """UPDATE users SET previousLogin = (SELECT lastLogin FROM users WHERE userName = '{0}') 
        WHERE userName = '{0}'""".format(name)
    )
    cursor.execute(
        """UPDATE users SET lastLogin = (select DATETIME('now')) 
        WHERE userName = '{0}'""".format(name)
    )
    userList.commit()

def firstLogin(name):
    cursor.execute(
        """SELECT lastLogin FROM users WHERE userName = '{}'""".format(name)
    )
    lastLog = cursor.fetchall()
    return cleanReturn(lastLog)

# expand with other functions
def printUsers():
    cursor.execute("""SELECT userName, lastLogin, previousLogin FROM users""")
    row = cursor.fetchall()

    print("('userName', 'lastLogin', 'previousLogin')")
    for row in row:
        print(row)

def userLogin():
    try:
        userName = input("Login, enter new for account creation:")
    except Exception as e:
        print(str(e))

    if queryUser(userName):
        passwd = getpass.getpass("Password: ")
        if queryPass(userName, passwd) == caesar(passwd,4):
            if firstLogin(userName) == "NULL":
                updateLogin(userName)
                print("Welcome {}. Thank you for joining our hive. \n".format(userName))
            else:
                updateLogin(userName)
                print("Welcome back {}. Your last login date was {}. \n".format(userName, queryLogin(userName)))

            if userName == "Admin":
                command = input("Would you like to view the user list? ")
                if command[0] == 'y':
                    printUsers()
                else:
                    print("Fine, have it your way.")
        else:
            print("Invalid Password")
    else:
        print("Not a valid user.")
        setup(userName)

def newUser(name):
    reading = True
    while reading:
        if name.lower() == "new":
            try:
                userName = input("Enter your new username: ")
            except Exception as e:
                print(str(e))
        else:
            userName = name

        if userName.lower() == "new":
            print("New is not a valid username. Please try another.")
            name = "new"
            continue
        elif queryUser(userName):
            print("That username is already taken. Please try another.")
            name = "new"
            continue
        else:
            newPass = getpass.getpass("That username is available. Please enter your password: ")
            insertUser(userName.title(), caesar(newPass, 4))
            reading = False
            userLogin()

def setup(name):
    try:
        validate = input("Would you like to setup a new account? ")
    except Exception as e:
        print(str(e))

    if validate[0].lower() == 'n':
        print("Good Bye.")
        userList.close()
    else:
        newUser(name)

userLogin()

userList.close()