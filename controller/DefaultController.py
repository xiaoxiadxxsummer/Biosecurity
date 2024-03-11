import datetime

from flask import Blueprint,render_template,redirect
from http import HTTPStatus
from flask import request
from dao.connection import *
from werkzeug.security import generate_password_hash,check_password_hash


#/
bp=Blueprint("",__name__,url_prefix="/")

@bp.route("/")
def home():
    return redirect("/login")

@bp.route("/login")
def login():
    return render_template("Login.html")

@bp.route("/login",methods=["POST"])
def openlogin():
    connection = getCursor()
    username = request.form.get("username")
    password = request.form.get("password")
    connection.execute(f"SELECT aid,firstName,lastName,addRess,email,phone,state,date,userName,password FROM apiarist where userName='{username}';")
    apiarist = connection.fetchone()
    if apiarist:
        now_apiarist={
            "aid": apiarist[0],
            "firstName": apiarist[1],
            "lastName": apiarist[2],
            "addRess": apiarist[3],
            "email": apiarist[4],
            "phone": apiarist[5],
            "state": apiarist[6],
            "date": apiarist[7],
            "userName": apiarist[8],
            "password": apiarist[9],
        }
        if check_password_hash(apiarist[9], password):
            return {"message": "Apiarist Login successful!","code":0,"user":now_apiarist}
        else:
            return {"message": "Incorrect password.", "code": 404}
    else:
        connection.execute(f"SELECT eid,firstName,lastName,userName,password,email,phone,position,department,state,date,role FROM employee where userName='{username}';")
        employee = connection.fetchone()
        if employee:
            now_employee = {
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
            }
            if check_password_hash(employee[4], password):
                if employee[11]==0:
                    return {"message": "Employee Login successful!", "code": 1, "user": now_employee}
                elif employee[11]==1:
                    return {"message": "Admin Login successful!", "code": 2, "user": now_employee}
            else:
                return {"message": "Incorrect password.", "code": 404}

    return {"message":"This user is not registered yet!","code":404}

@bp.route("/register",methods=["POST"])
def Addregister():
    connection = getCursor()
    username = request.form.get("username")
    password = request.form.get("password")
    connection.execute(f"SELECT * FROM apiarist where userName='{username}';")
    apiarist = connection.fetchone()
    if apiarist:
        return {"status_code": HTTPStatus.BAD_REQUEST,"code":500,"message": "This username has already been registered!"}
    connection.execute(f"SELECT * FROM employee where userName='{username}';")
    employee = connection.fetchone()
    if employee:
        return {"status_code": HTTPStatus.BAD_REQUEST,"code":500,"message": "This username has already been registered!"}
    gener_password = generate_password_hash(password)
    connection.execute(f"""insert into apiarist(`userName`,`password`)values('{username}','{gener_password}')""")
    return {"status_code": HTTPStatus.OK,"code":200,"message": "Registered successfully!"}

@bp.route("/register")
def register():
    return render_template("register.html")

@bp.route("/guidelist")
def guidelist():
    connection = getCursor()
    connection.execute("SELECT gid,type,exist,commonName,scientificName,mainFeatures,description,symptoms,images FROM guide")
    guide_list = connection.fetchall()
    now_guide_list = []
    for guide in guide_list:
        now_guide_list.append({
            "gid": guide[0],
            "type": guide[1],
            "exist": guide[2],
            "commonName": guide[3],
            "scientificName": guide[4],
            "mainFeatures": guide[5],
            "description": guide[6],
            "symptoms": guide[7],
            "images": guide[8]
        })
    return render_template("guidelist.html", guide_list = now_guide_list)

@bp.route("/stateEmployee/guide",methods=["GET"])
def guidesate():
    connection = getCursor()
    connection.execute("SELECT gid,type,exist,commonName,scientificName,mainFeatures,description,symptoms,images FROM guide")
    guide_list = connection.fetchall()
    now_guide_list=[]
    for guide in guide_list:
        now_guide_list.append({
            "gid": guide[0],
            "type": guide[1],
            "exist": guide[2],
            "commonName": guide[3],
            "scientificName": guide[4],
            "mainFeatures": guide[5],
            "description": guide[6],
            "symptoms": guide[7],
            "images": guide[8]
        })
    return render_template("Employee/Guide.html", guide_list=now_guide_list, page="guide")

@bp.route("/stateEmployee/guide/<name>", methods=["GET"])
def getGuideName(name):
    connection = getCursor()
    connection.execute(f"SELECT gid,type,exist,commonName,scientificName,mainFeatures,description,symptoms,images FROM guide where scientificName LIKE '%{name}%' OR commonName LIKE '%{name}%'")
    guide_list = connection.fetchall()
    now_guide_list = []
    for guide in guide_list:
        now_guide_list.append({
            "gid": guide[0],
            "type": guide[1],
            "exist": guide[2],
            "commonName": guide[3],
            "scientificName": guide[4],
            "mainFeatures": guide[5],
            "description": guide[6],
            "symptoms": guide[7],
            "images": guide[8]
        })
    return render_template("Employee/Guide.html", guide_list=now_guide_list, page="guide")

@bp.route("/stateEmployee/apiaristst",methods=["GET"])
def apiariststate():
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
    return render_template("Employee/Apiarist.html", apiarist_list=now_apiarist_list, page="apiarist")

@bp.route("/stateEmployee/apiaristst/<name>", methods=["GET"])
def getApiaristName(name):
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
    return render_template("Employee/Apiarist.html", apiarist_list=now_apiarist_list, page="apiarist")
