from flask import Blueprint,render_template,redirect
from http import HTTPStatus
from flask import request
from dao.connection import *
from werkzeug.security import generate_password_hash,check_password_hash
from werkzeug.utils import secure_filename
import os

#/Guide
bp=Blueprint("Guide",__name__,url_prefix="/Guide")

url="http://127.0.0.1:3001/static/image/"

@bp.route("/",methods=["GET"])
def guide():
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
    return render_template("Administrator/Guide.html", guide_list=now_guide_list, page="guide")

@bp.route("/<name>", methods=["GET"])
def getName(name):
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
    return render_template("Administrator/Guide.html", guide_list=now_guide_list, page="guide")

@bp.route("/",methods=["POST"])
def addguide():
    connection = getCursor()
    type = request.form.get("type")
    exist = request.form.get("exist")
    commonName = request.form.get("commonName")
    scientificName = request.form.get("scientificName")
    mainFeatures = request.form.get("mainFeatures")
    description = request.form.get("description")
    symptoms = request.form.get("symptoms")
    images = request.files["images"]
    if images.filename == '':
        return {"status_code": HTTPStatus.BAD_REQUEST,"message":"No selected file."}
    try:
        if images:
            basepath = os.path.dirname(__file__)  # 当前文件所在路径
            filename = secure_filename(images.filename)
            images.save(os.path.join(basepath, 'static/image', filename))
            now_path = url+filename
            connection.execute(f"""insert into guide(type,exist,`commonName`,`scientificName`,`mainFeatures`,`description`,`symptoms`,`images`)values('{type}','{exist}','{commonName}','{scientificName}','{mainFeatures}','{description}','{symptoms}','{now_path}')""")
    except :
        return {"status_code": HTTPStatus.BAD_REQUEST,"message":"Error Add guide."}
    return {"status_code": HTTPStatus.OK,"message":"Add guide Successfully!"}


@bp.route("/",methods=["PUT"])
def updateguide():
    connection = getCursor()
    gid = request.form.get("gid")
    type = request.form.get("type")
    exist = request.form.get("exist")
    commonName = request.form.get("commonName")
    scientificName = request.form.get("scientificName")
    mainFeatures = request.form.get("mainFeatures")
    description = request.form.get("description")
    symptoms = request.form.get("symptoms")
    images = request.files["images"]
    if images.filename == '':
        return {"status_code": HTTPStatus.BAD_REQUEST,"message":"No selected file."}
    try:
        if images:
            basepath = os.path.dirname(__file__)  # 当前文件所在路径
            filename = secure_filename(images.filename)
            images.save(os.path.join(basepath, 'static/image', filename))
            now_path = url+filename
            connection.execute(f"""UPDATE guide SET type='{type}',exist='{exist}',commonName='{commonName}',scientificName='{scientificName}',mainFeatures='{mainFeatures}',`description`='{description}',`symptoms`='{symptoms}',`images`='{now_path}' where gid='{gid}' """)
    except:
        return {"status_code": HTTPStatus.BAD_REQUEST, "message": "Error Update guide."}
    return {"status_code": HTTPStatus.OK, "message": "Update guide Successfully!"}

@bp.route("/",methods=["DELETE"])
def deleteguide():
    connection = getCursor()
    gid = request.form.get("gid")
    try:
        connection.execute(f"""DELETE FROM guide WHERE gid='{gid}' """)
    except:
        return {"status_code": HTTPStatus.BAD_REQUEST, "message": "Error DELETE guide."}
    return {"status_code": HTTPStatus.OK, "message": "DELETE guide Successfully!"}

