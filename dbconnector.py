from flask import flash, session
import mysql.connector
from mysql.connector import Error
import uuid
import re
import hashlib
import binascii
import os
import random
import time
import arrow


class connect:
    def startConnect(self):
        try:
            connection = mysql.connector.connect(
                host="amitoj.net",
                database="amit0j_pytest",
                user="amit0j_pyusr",
                password="PythonTest#",
            )
            if connection.is_connected():
                db_Info = connection.get_server_info()
                print("Connected to MySQL Server version ", db_Info)
                connectioncursor = connection.cursor()
            else:
                connection = "fail"
        except Error as e:
            print("Error while connecting to MySQL", e)
            connection = "fail"
        return connection


class useractions:
    def adduser(self, uname, upwd, umail):
        connection = connect.startConnect("")
        if connection != "fail":
            connectioncursor = connection.cursor()
            usql = f"""SELECT * FROM users WHERE email = '{umail}'"""
            connectioncursor.execute(usql)
            exists = connectioncursor.fetchone()
            if not uname or not upwd:
                flash("Please Fill Out The Form", "warning")
            elif exists:
                flash("Email Already In Use!", "warning")
            elif not re.match(r"[A-Za-z ,.'-]+", uname):
                flash("Invalid Username Format", "warning")
            elif not re.match(
                r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", umail
            ):
                flash("Invalid Email Format", "warning")
            elif not re.match(r"[A-Za-z0-9@#$%^&+=]{8,}", upwd):
                flash("Password Not Strong!", "danger")
            else:
                accno = useractions().makeaccNo(random.randint(9, 18))
                userid = uuid.uuid1()
                hupwd = passwordactions.hash_password("", upwd)
                defaultBal = useractions().makeaccNo(random.randint(1, 5))
                sql = f"INSERT INTO `users` (`username`, `email`, `password`, `accno`, `userid`, `accbalance`, `apiKey`, `role`) VALUES ('{uname}', '{umail}', '{hupwd}', '{accno}', '{userid}', '{defaultBal}', '', 'USER');"
                result = connectioncursor.execute(sql)
                try:
                    result
                    flash("Register Sucessful, Please Log-In", "success")
                except Error as e:
                    print("Error while Saving To MySql", e)
                    flash("Register Failed, Try Again", "danger")

    def deleteUser(self, uid):
        connection = connect.startConnect("")
        if connection != "fail":
            connectioncursor = connection.cursor()
            usql = f"""SELECT apiKey FROM users WHERE userid = '{uid}'"""
            connectioncursor.execute(usql)
            savedKey = connectioncursor.fetchall()
            if savedKey:
                if str(savedKey[0][0]) == str(session["apiKey"]):
                    usql = f"""DELETE FROM users WHERE userid = '{uid}'"""
                    connectioncursor.execute(usql)
                    flash("Account Deleted", "danger")
                    return True
                else:
                    return False
            else:
                flash("User Not Found!", "danger")

    def login(self, umail, upwd):
        connection = connect.startConnect("")
        if connection != "fail":
            connectioncursor = connection.cursor()
            usql = f"""SELECT * FROM users WHERE email = '{umail}'"""
            connectioncursor.execute(usql)
            account = connectioncursor.fetchall()
            if account:
                for row in account:
                    savedname = row[1]
                    savedrole = row[2]
                    savedemail = row[3]
                    savedpwd = row[4]
                    savedaccno = row[5]
                    saveduserid = row[6]
                    savedaccbal = row[7]

                authorised = passwordactions.verify_password("", savedpwd, upwd)
                if authorised:
                    apiKey = uuid.uuid1()
                    sql = (
                        f"UPDATE users SET apiKey = '{apiKey}' WHERE email = '{umail}'"
                    )
                    connectioncursor.execute(sql)
                    session["uid"] = saveduserid
                    session["name"] = savedname
                    session["role"] = savedrole
                    session["email"] = savedemail
                    session["accno"] = savedaccno
                    session["accbal"] = savedaccbal
                    session["apiKey"] = apiKey
                    return True
                else:
                    return False
            else:
                flash("User Not Found!", "danger")

    def getAccDetail(self, apiKey, uid):
        connection = connect.startConnect("")
        if connection != "fail":
            connectioncursor = connection.cursor()
            usql = f"""SELECT apiKey FROM users WHERE userid = '{uid}'"""
            connectioncursor.execute(usql)
            savedKey = connectioncursor.fetchall()
            if savedKey:
                if str(savedKey[0][0]) == str(session["apiKey"]):
                    usql = f"""SELECT * FROM users WHERE userid = '{uid}'"""
                    connectioncursor.execute(usql)
                    account = connectioncursor.fetchall()
                    if account:
                        for row in account:
                            session["uid"] = row[6]
                            session["name"] = row[1]
                            session["email"] = row[3]
                            session["accno"] = row[5]
                            session["accbal"] = row[7]
                    return True
                else:
                    return False
            else:
                flash("User Not Found!", "danger")

    def transfer(self, toaccno, fromaccno, amount, dumpmoney):
        print(1)
        amount = float(amount)
        connection = connect.startConnect("")
        if connection != "fail":
            print(2)
            connectioncursor = connection.cursor()
            print(3)
            usql = f"SELECT accbalance FROM users WHERE accno = '{fromaccno}'"
            print(usql)
            connectioncursor.execute(usql)
            accountbal = connectioncursor.fetchall()
            if accountbal:
                accountbal = float(accountbal[0][0])
                accountbal -= amount
                sendsql = f"UPDATE users SET accbalance = '{str(accountbal)}' WHERE accno = '{fromaccno}'"
                connectioncursor.execute(sendsql)
                session["accbal"] = accountbal

                if not dumpmoney:
                    ssql = f"SELECT accbalance FROM users WHERE accno = '{toaccno}'"
                    connectioncursor.execute(ssql)
                    reciverbal = connectioncursor.fetchall()
                    reciverbal = float(reciverbal[0][0])
                    reciverbal += amount
                    recsql = f"UPDATE users SET accbalance = '{str(reciverbal)}' WHERE accno = '{toaccno}'"
                    connectioncursor.execute(recsql)
                ts = time.time()
                historysql = f"INSERT INTO `transfers` (`toacc`, `fromacc`, `amount`, `timestamp`) VALUES ('{toaccno}', '{fromaccno}', '{str(amount)}', '{str(ts)}');"
                connectioncursor.execute(historysql)
                return True
            else:
                flash("User Not Found!", "danger")

    def addEntry(self, data):
        connection = connect.startConnect("")
        if connection != "fail":
            connectioncursor = connection.cursor()
            sql = f"INSERT INTO `entries` (`name`, `accno`, `type`, `amount`) VALUES ("
            for i in data:
                for item in i:
                    if type(item) == type([]):
                        sql += f"'{item[0]}', "

            sql = sql.rstrip(", ")
            sql += ");"
            connectioncursor.execute(sql)
            return True

    def getLoanRequests(self, accno, apiKey):
        connection = connect.startConnect("")
        if connection != "fail":
            connectioncursor = connection.cursor()
            usql = f"""SELECT apiKey FROM users WHERE accno = '{accno}'"""
            connectioncursor.execute(usql)
            savedKey = connectioncursor.fetchall()
            if savedKey:
                if str(savedKey[0][0]) == str(session["apiKey"]):
                    sql = "SELECT * FROM `entries`"
                    connectioncursor.execute(sql)
                    return connectioncursor.fetchall()

    def approveOrDenyLoan(self, loanId, approved):
        connection = connect.startConnect("")
        if connection != "fail":
            connectioncursor = connection.cursor()
            usql = f"""SELECT apiKey FROM users WHERE accno = '{session["accno"]}'"""
            connectioncursor.execute(usql)
            savedKey = connectioncursor.fetchall()
            if savedKey:
                if str(savedKey[0][0]) == str(session["apiKey"]):
                    sql = f"SELECT * FROM `entries` WHERE id = '{loanId}'"
                    connectioncursor.execute(sql)
                    request = connectioncursor.fetchall()
                    if request:
                        for row in request:
                            loanAmount = row[1]
                            loanerAccno = row[3]

                        if approved:
                            self.transfer(
                                self, loanerAccno, 9999999999, loanAmount, False
                            )
                    sql = f"DELETE FROM `entries` WHERE id = '{loanId}'"
                    connectioncursor.execute(sql)
                    return True

    def getTransferHistory(self, accno, apiKey):
        connection = connect.startConnect("")
        if connection != "fail":
            connectioncursor = connection.cursor()
            usql = f"""SELECT apiKey FROM users WHERE accno = '{accno}'"""
            connectioncursor.execute(usql)
            savedKey = connectioncursor.fetchall()
            if savedKey:
                if str(savedKey[0][0]) == str(session["apiKey"]):
                    usql = f"""SELECT * FROM transfers WHERE toacc = '{accno}' OR fromacc = '{accno}'"""
                    connectioncursor.execute(usql)
                    history = connectioncursor.fetchall()
                    historyJSON = list()
                    if history:
                        for i in history:
                            time = arrow.get(float(i[4])).humanize()
                            historyJSON.append(
                                {
                                    "to": i[1],
                                    "from": i[2],
                                    "amount": i[3],
                                    "time": time,
                                    "timestamp": i[4],
                                    "index": i[0],
                                }
                            )
                        return historyJSON
                    else:
                        return list()
                else:
                    return False
            else:
                flash("User Not Found!", "danger")

    def makeaccNo(self, l):
        accno = ""
        for i in range(0, l):
            accno = accno + str(random.randint(0, 9))
        return accno


class passwordactions:
    def hash_password(self, password):
        salt = hashlib.sha256(os.urandom(60)).hexdigest().encode("ascii")
        pwdhash = hashlib.pbkdf2_hmac("sha512", password.encode("utf-8"), salt, 100000)
        pwdhash = binascii.hexlify(pwdhash)
        return (salt + pwdhash).decode("ascii")

    def verify_password(self, stored_password, provided_password):
        salt = stored_password[:64]
        stored_password = stored_password[64:]
        pwdhash = hashlib.pbkdf2_hmac(
            "sha512", provided_password.encode("utf-8"), salt.encode("ascii"), 100000
        )
        pwdhash = binascii.hexlify(pwdhash).decode("ascii")
        return pwdhash == stored_password
