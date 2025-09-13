from flask import Blueprint, render_template, request, redirect, url_for
from bson.objectid import ObjectId
from db import db
from datetime import datetime

sedes_bp = Blueprint("sedes", __name__, url_prefix="/sedes")

# LISTAR
@sedes_bp.route("/")
def lista_sedes():
    sedes = list(db["sedes"].find())
    return render_template('sedes/lista.html', sedes=sedes)

# AGREGAR
@sedes_bp.route("/agregar", methods=["GET", "POST"])
def agregar_sedes():
    if request.method == "POST":
        nueva_sede = {
            "direccion": request.form["direccion"],
            "costo_horario": float(request.form["costo_horario"]),
             "created_at": datetime.utcnow()
        }
        db["sedes"].insert_one(nueva_sede)
        return redirect(url_for("sedes.lista_sedes"))
    return render_template('sedes/agregar.html')

# EDITAR
@sedes_bp.route("/editar/<id>", methods=["GET", "POST"])
def editar_sedes(id):
    sedes = db["sedes"].find_one({"_id": ObjectId(id)})
    if request.method == "POST":
        db["sedes"].update_one(
            {"_id": ObjectId(id)},
            {"$set": {
                "direccion": request.form["direccion"],
                "costo_horario": float(request.form["costo_horario"])
            }}
        )
        return redirect(url_for("sedes.lista_sedes"))
    return render_template('sedes/editar.html', sedes=sedes)

# ELIMINAR
@sedes_bp.route("/eliminar/<id>")
def eliminar_sedes(id):
    db["sedes"].delete_one({"_id": ObjectId(id)})
    return redirect(url_for("sedes.lista_sedes"))