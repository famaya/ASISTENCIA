from flask import Blueprint, render_template, request, redirect, url_for
from bson.objectid import ObjectId
from db import db

groups_bp = Blueprint('groups', __name__, url_prefix='/groups')

# LISTAR
@groups_bp.route('/')
def lista_grupos():
    grupos1 = list(db['groups'].find())
    return render_template('groups/lista.html', grupos=grupos1)

# AGREGAR
@groups_bp.route("/agregar", methods=["GET", "POST"])
def agregar_grupos():
    if request.method == "POST":
        nuevo = {
            "nombre": request.form["nombre"],
            "horario": request.form["horario"],
            "profesor_id": request.form["profesor_id"],
            "sede_id": request.form["sede_id"],
        }
        db["groups"].insert_one(nuevo)
        return redirect(url_for("groups.lista_grupos"))
    return render_template("groups/agregar.html")

# EDITAR
@groups_bp.route("/editar/<id>", methods=["GET", "POST"])
def editar_grupos(id):
    groups = db["groups"].find_one({"_id": ObjectId(id)})
    if request.method == "POST":
        db["groups"].update_one(
            {"_id": ObjectId(id)},
            {"$set": {
            "nombre": request.form["nombre"],
            "horario": request.form["horario"],
            "profesor_id": request.form["profesor_id"],
            "sede_id": request.form["sede_id"],
            }}
        )
        return redirect(url_for("groups.lista_grupos"))
    return render_template("groups/editar.html", profesor=profesor)

# ELIMINAR
@groups_bp.route("/eliminar/<id>")
def eliminar_grupos(id):
    db["groups"].delete_one({"_id": ObjectId(id)})
    return redirect(url_for("groups.lista_grupos"))