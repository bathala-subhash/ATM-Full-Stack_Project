from flask import Flask, render_template, request, session, redirect, url_for
import smtplib
import pymysql
import random
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import pymysql

app = Flask(__name__)


db_config = {
    "host": "localhost",
    "user": "root",
    "password": "root",
    "database": "atm"
}

@app.route("/")
def landing():
    return render_template("home.html")

@app.route("/create")
def create():
    return render_template("create.html")

@app.route("/withdraw")
def withdraw():
    return render_template("withdraw1.html")

@app.route("/withdraw1", methods=["POST","GET"])
def withdraw1():
    accno = request.form["account-number"]
    pin = request.form["pin"]

    conn = pymysql.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM ACCOUNTS WHERE USER_ACCNO = %s", (accno,))
    data = cursor.fetchone()
    conn.close()

    if data is None:
        return render_template("withdraw1.html", msg="account does not exist")
    elif data[3] is None:
        return render_template("withdraw1.html", msg="PIN not set")
    elif data[3] != int(pin):
        return render_template("withdraw1.html", msg="Invalid PIN")
    else:
        
        return render_template("withdraw.html", accno=accno, user=data[1])

@app.route("/withdraw3", methods=["POST","GET"])
def withdraw3():
    accno = request.form["accno"]
    amount = request.form["amount"]

    conn = pymysql.connect(**db_config)
    cursor = conn.cursor()
    query = "SELECT USER_BALANCE,USER_NAME FROM ACCOUNTS WHERE USER_ACCNO = %s"
    cursor.execute(query,(accno))
    data = cursor.fetchone()
    conn.close()
    print(data)

    if int(amount) <= int(data[0]):
        balance = int(data[0]) - int(amount)
        conn = pymysql.connect(**db_config)
        cursor = conn.cursor()
        query = "UPDATE ACCOUNTS SET USER_BALANCE = %s WHERE USER_ACCNO = %s"
        cursor.execute(query,(balance,accno))
        conn.commit()
        conn.close()
        return render_template("home.html",msg="balance",accno=accno,user_name=data[1])
    else:
        return render_template("home.html",msg="nobalance",accno=accno,user_name=data[1])


@app.route("/deposite")
def deposite():
    return render_template("deposite.html")

@app.route("/deposit1", methods=["POST"])
def deposit1():
    accno = request.form["account-number"]
    amount = int(request.form["amount"])

    conn = pymysql.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM ACCOUNTS WHERE USER_ACCNO = %s", (accno,))
    data = cursor.fetchone()
    conn.commit()
    conn.close()

    if data is None:
        return render_template("deposite.html", msg="Account does not exist")
    
    else:
        conn = pymysql.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute("update accounts set user_balance=user_balance + %s where user_accno=%s", (amount,accno))
        data = cursor.fetchone()
        conn.commit()
        conn.close()

        return render_template("deposite.html",msg="deposited successfully")
   

@app.route("/mini")
def mini():
    return render_template("mini.html")

@app.route("/mini2", methods=["POST"])
def mini2():
    accno = request.form["account-number"]
    pin = request.form["pin"]

    conn = pymysql.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM ACCOUNTS WHERE USER_ACCNO = %s", (accno,))
    data = cursor.fetchone()
    conn.close()

    if data is None:
        return render_template("mini.html", msg="Account does not exist")
    elif data[3] != int(pin):
        return render_template("mini.html", msg="Invalid PIN")

    name = data[1]
    email = data[2]
    # email=data[3]
    balance = data[4]

    return render_template("mini1.html", accno=accno, name=name, email=email, balance=balance)

@app.route("/pingeneration1")
def pingeneration1():
    return render_template("pingeneration1.html")
@app.route("/pingeneration2",methods=["POST","GET"])
def pingeneration2():
    accno = request.form["accno"]

    conn = pymysql.connect(**db_config)
    cursor = conn.cursor()
    query = "SELECT * FROM ACCOUNTS WHERE USER_ACCNO = %s"
    cursor.execute(query,(accno))
    data = cursor.fetchone()
    conn.close()
    print(data)
    if data is None:
        return render_template("pingeneration1.html",msg="noaccount")
    elif data[-2] != None:
        return render_template("pingeneration1.html",msg="account")
    else:
        return render_template("pingeneration2.html",accno=accno)
@app.route("/pingeneration3",methods=["POST","GET"])
def pingeneration3():
    accno = request.form["accno"]
    pin = request.form["pin"]
    cpin = request.form["cpin"]
    if pin != cpin:
        return render_template("pingeneration2.html",accno=accno,msg="wrongpin")
    else:
        conn = pymysql.connect(**db_config)
        cursor = conn.cursor()
        query = "UPDATE ACCOUNTS SET USER_PIN = %s WHERE USER_ACCNO = %s"
        cursor.execute(query,(pin,accno))
        conn.commit()
        conn.close()
        return render_template("pingeneration2.html",msg="ok")
app.run(port=5001)
