from flask import Blueprint,render_template,redirect
from http import HTTPStatus
from flask import request
from dao.connection import *
from werkzeug.security import generate_password_hash,check_password_hash


#/Apiarist
bp=Blueprint("Apiarist",__name__,url_prefix="/Apiarist")

@bp.route("/",methods=["GET"])
def apiarist():
    connection = getCursor()
    connection.execute("SELECT aid,firstName,lastName,addRess,email,phone,state,date,userName,password FROM apiarist ORDER BY date DESC")
    apiarist_list = connection.fetchall()
    now_apiarist_list=[]
    for apiaris in apiarist_list:
        now_apiarist_list.append({
            "aid": apiaris[0],
            "firstName": apiaris[1],
            "lastName": apiaris[2],
            "addRess": apiaris[3],
            "email": apiaris[4],
            "phone": apiaris[5],
            "state": apiaris[6],
            "date": apiaris[7],
            "userName": apiaris[8],
            "password": apiaris[9],
        })
    return render_template("Administrator/Apiarist.html", apiarist_list=now_apiarist_list, page="apiarist")

@bp.route("/<name>", methods=["GET"])
def getName(name):
    connection = getCursor()
    connection.execute(f"SELECT aid,firstName,lastName,addRess,email,phone,state,date,userName,password  FROM apiarist WHERE firstName LIKE '%{name}%' OR lastName LIKE '%{name}%' ORDER BY date DESC")
    apiarist_list = connection.fetchall()
    now_apiarist_list = []
    for apiaris in apiarist_list:
        now_apiarist_list.append({
            "aid": apiaris[0],
            "firstName": apiaris[1],
            "lastName": apiaris[2],
            "addRess": apiaris[3],
            "email": apiaris[4],
            "phone": apiaris[5],
            "state": apiaris[6],
            "date": apiaris[7],
            "userName": apiaris[8],
            "password": apiaris[9],
        })
    return render_template("Administrator/Apiarist.html", apiarist_list=now_apiarist_list, page="apiarist")

@bp.route("/",methods=["POST"])
def addApiarist():
    connection = getCursor()
    firstName = request.form.get("firstName")
    lastName = request.form.get("lastName")
    addRess = request.form.get("addRess")
    email = request.form.get("email")
    phone = request.form.get("phone")
    state = request.form.get("state")
    userName = request.form.get("userName")
    password = request.form.get("password")
    gener_password = generate_password_hash(password)

    connection.execute(f"SELECT * FROM apiarist where userName='{userName}';")
    apiarist = connection.fetchone()
    if apiarist:
        return {"status_code": HTTPStatus.BAD_REQUEST, "code": 500,
                "message": "This username has already been registered!"}
    try:
        connection.execute(f"""insert into apiarist(firstName,lastName,addRess,`email`,`phone`,`state`,`userName`,`password`)values('{firstName}','{lastName}','{addRess}','{email}','{phone}','{state}','{userName}','{gener_password}')""")
    except:
        return {"status_code": HTTPStatus.BAD_REQUEST,"message":"Error Add Apiarist."}
    return {"status_code": HTTPStatus.OK,"message":"Add Apiarist Successfully!"}


@bp.route("/",methods=["PUT"])
def updateApiarist():
    connection = getCursor()
    aid = request.form.get("aid")
    firstName = request.form.get("firstName")
    lastName = request.form.get("lastName")
    addRess = request.form.get("addRess")
    email = request.form.get("email")
    phone = request.form.get("phone")
    state = request.form.get("state")
    userName = request.form.get("userName")
    password = request.form.get("password")
    gener_password = generate_password_hash(password)

    try:
        connection.execute(f"""UPDATE apiarist SET firstName='{firstName}',lastName='{lastName}',addRess='{addRess}',`email`='{email}',`phone`='{phone}',`state`='{state}',`userName`='{userName}',`password`='{gener_password}' where aid='{aid}' """)
    except:
        return {"status_code": HTTPStatus.BAD_REQUEST, "message": "Error Update Apiarist."}
    return {"status_code": HTTPStatus.OK, "message": "Update Apiarist Successfully!"}

@bp.route("/",methods=["DELETE"])
def deleteApiarist():
    connection = getCursor()
    aid = request.form.get("aid")
    try:
        connection.execute(f"""DELETE FROM apiarist WHERE aid='{aid}' """)
    except:
        return {"status_code": HTTPStatus.BAD_REQUEST, "message": "Error DELETE Apiarist."}
    return {"status_code": HTTPStatus.OK, "message": "DELETE Apiarist Successfully!"}

