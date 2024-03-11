from flask import Blueprint,render_template,redirect
from http import HTTPStatus
from flask import request
from dao.connection import *
from werkzeug.security import generate_password_hash,check_password_hash


#/Employee
bp=Blueprint("Employee",__name__,url_prefix="/Employee")

@bp.route("/",methods=["GET"])
def employee():
    connection = getCursor()
    connection.execute("SELECT eid,firstName,lastName,userName,password,email,phone,position,department,state,date,role  FROM employee where role=0 ORDER BY date DESC")
    employee_list = connection.fetchall()
    now_employee_list=[]
    for employee in employee_list:
        now_employee_list.append({
            "eid": employee[0],
            "firstName": employee[1],
            "lastName": employee[2],
            "userName": employee[3],
            "password": employee[4],
            "email": employee[5],
            "phone": employee[6],
            "position": employee[7],
            "department": employee[8],
            "state": employee[9],
            "date": employee[10],
            "role": employee[11],
        })
    return render_template("Administrator/Employee.html", employee_list=now_employee_list, page="employee")

@bp.route("/<name>", methods=["GET"])
def getName(name):
    connection = getCursor()
    connection.execute(f"SELECT eid,firstName,lastName,userName,password,email,phone,position,department,state,date,role  FROM employee where role=0 and firstName LIKE '%{name}%' OR role=0 and lastName LIKE '%{name}%' ORDER BY date DESC")
    employee_list = connection.fetchall()
    now_employee_list = []
    for employee in employee_list:
        now_employee_list.append({
            "eid": employee[0],
            "firstName": employee[1],
            "lastName": employee[2],
            "userName": employee[3],
            "password": employee[4],
            "email": employee[5],
            "phone": employee[6],
            "position": employee[7],
            "department": employee[8],
            "state": employee[9],
            "date": employee[10],
            "role": employee[11],
        })
    return render_template("Administrator/Employee.html", employee_list=now_employee_list, page="employee")

@bp.route("/",methods=["POST"])
def addemployee():
    connection = getCursor()
    firstName = request.form.get("firstName")
    lastName = request.form.get("lastName")
    email = request.form.get("email")
    phone = request.form.get("phone")
    date = request.form.get("date")
    position = request.form.get("position")
    department = request.form.get("department")
    state = request.form.get("state")
    userName = request.form.get("userName")
    password = request.form.get("password")
    gener_password = generate_password_hash(password)

    connection.execute(f"SELECT * FROM employee where userName='{userName}';")
    employee = connection.fetchone()
    if employee:
        return {"status_code": HTTPStatus.BAD_REQUEST, "code": 500,
                "message": "This username has already been registered!"}
    try:
        connection.execute(f"""insert into employee(firstName,lastName,`email`,`phone`,`position`,`department`,`state`,`date`,`userName`,`password`,`role`)values('{firstName}','{lastName}','{email}','{phone}','{position}','{department}','{state}','{date}','{userName}','{gener_password}',0)""")
    except :
        return {"status_code": HTTPStatus.BAD_REQUEST,"message":"Error Add employee.Incomplete data!"}
    return {"status_code": HTTPStatus.OK,"message":"Add employee Successfully!"}


@bp.route("/",methods=["PUT"])
def updateemployee():
    connection = getCursor()
    eid = request.form.get("eid")
    firstName = request.form.get("firstName")
    lastName = request.form.get("lastName")
    email = request.form.get("email")
    phone = request.form.get("phone")
    date = request.form.get("date")
    position = request.form.get("position")
    department = request.form.get("department")
    state = request.form.get("state")
    userName = request.form.get("userName")
    password = request.form.get("password")
    gener_password = generate_password_hash(password)

    try:
        connection.execute(f"""UPDATE employee SET firstName='{firstName}',lastName='{lastName}',date='{date}',position='{position}',department='{department}',`email`='{email}',`phone`='{phone}',`state`='{state}',`userName`='{userName}',`password`='{gener_password}' where eid='{eid}' """)
    except:
        return {"status_code": HTTPStatus.BAD_REQUEST, "message": "Error Update employee."}
    return {"status_code": HTTPStatus.OK, "message": "Update employee Successfully!"}

@bp.route("/",methods=["DELETE"])
def deleteemployee():
    connection = getCursor()
    eid = request.form.get("eid")
    try:
        connection.execute(f"""DELETE FROM employee WHERE eid='{eid}' """)
    except:
        return {"status_code": HTTPStatus.BAD_REQUEST, "message": "Error DELETE employee."}
    return {"status_code": HTTPStatus.OK, "message": "DELETE employee Successfully!"}

