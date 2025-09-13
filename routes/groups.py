from flask import Blueprint, render_template, request, redirect, url_for
from db import db
from bson.objectid import ObjectId
from datetime import datetime

groups_bp = Blueprint('groups', __name__, url_prefix='/groups')

# LISTAR
@groups_bp.route('/')
def lista_grupos():
    groups = list(db['groups'].find())
    for g in groups:
        g["profesor"] = db["professors"].find_one({"_id": g["profesor"]})
        g["sede"] = db["sedes"].find_one({"_id": g["sede"]})
        g["alumnas"] = list(db["students"].find({"_id": {"$in": g.get("alumnas_ids", [])}}))
    return render_template("groups/lista.html", groups=groups)


# AGREGAR
@groups_bp.route("/agregar", methods=["GET", "POST"])
def agregar_grupos():
    if request.method == "POST":
        nombre = request.form["nombre"]
        profesor_id = request.form["profesores"]
        horario = request.form["horario"]
        sede_id = request.form["sede"]
        alumnas_ids = request.form.getlist("alumnas")

        grupo = {
            "nombre": nombre,
            "profesor": ObjectId(profesor_id),
            "horario": horario,
            "sede": ObjectId(sede_id),
            "alumnas": [ObjectId(a) for a in alumnas_ids],
             "created_at": datetime.utcnow()
        }
        db["groups"].insert_one(grupo)
        return redirect(url_for("groups.lista_grupos"))
   
    # Obtener listas de las colecciones relacionadas
    profesores = list(db["professors"].find())
    sedes = list(db["sedes"].find())
    alumnas = list(db["students"].find())

    return render_template("groups/agregar.html", profesores=profesores, sedes=sedes, alumnas=alumnas)




# --- EDITAR GRUPO ---
@groups_bp.route("/editar/<id>", methods=["GET", "POST"])
def editar_grupos(id):
    group = db["groups"].find_one({"_id": ObjectId(id)})
    if request.method == "POST":
        nombre = request.form["nombre"]
        profesor_id = request.form["profesor_id"]
        sede_id = request.form["sede_id"]
        alumnas_ids = request.form.getlist("alumnas")  # lista de checkboxes

        db["groups"].update_one(
            {"_id": ObjectId(id)},
            {"$set": {
                "nombre": nombre,
                "profesor_id": ObjectId(profesor_id),
                "sede_id": ObjectId(sede_id),
                "alumnas_ids": [ObjectId(a) for a in alumnas_ids]
            }}
        )
        
        return redirect(url_for("groups.lista_grupos"))

    
    profesores = list(db["professors"].find())
    sedes = list(db["sedes"].find())
    alumnas = list(db["students"].find())
    return render_template("groups/editar.html", group=group, profesores=profesores, sedes=sedes, alumnas=alumnas)








# ELIMINAR
@groups_bp.route("/eliminar/<id>")
def eliminar_grupos(id):
    db["groups"].delete_one({"_id": ObjectId(id)})
    return redirect(url_for("groups.lista_grupos"))