from flask import Blueprint, render_template, request, redirect, url_for
from bson.objectid import ObjectId
from db import db
from datetime import datetime

professors_bp = Blueprint("professors", __name__, url_prefix="/professors")

# LISTAR
@professors_bp.route("/")
def lista_profesores():
    professors = list(db["professors"].find())
    return render_template("professors/lista.html", professors=professors)

# AGREGAR
@professors_bp.route("/agregar", methods=["GET", "POST"])
def agregar_profesor():
    if request.method == "POST":
        nuevo = {
            "nombre": request.form["nombre"],
            "apellido": request.form["apellido"],
            "dni": request.form["dni"],
            "telefono": request.form["telefono"],
            "email": request.form["email"]
        }
        db["professors"].insert_one(nuevo)
        return redirect(url_for("professors.lista_profesores"))
    return render_template("professors/agregar.html")

# EDITAR
@professors_bp.route("/editar/<id>", methods=["GET", "POST"])
def editar_profesor(id):
    profesor = db["professors"].find_one({"_id": ObjectId(id)})
    if request.method == "POST":
        db["professors"].update_one(
            {"_id": ObjectId(id)},
            {"$set": {
                "nombre": request.form["nombre"],
                "apellido": request.form["apellido"],
                "dni": request.form["dni"],
                "telefono": request.form["telefono"],
                "email": request.form["email"]
            }}
        )
        return redirect(url_for("professors.lista_profesores"))
    return render_template("professors/editar.html", profesor=profesor)

# ELIMINAR
@professors_bp.route("/eliminar/<id>")
def eliminar_profesor(id):
    db["professors"].delete_one({"_id": ObjectId(id)})
    return redirect(url_for("professors.lista_profesores"))