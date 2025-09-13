from flask import Blueprint, render_template, request, redirect, url_for, flash
from db import db
from datetime import datetime
from bson.objectid import ObjectId

confirmations_bp = Blueprint("confirmations", __name__, url_prefix="/confirmations")

# 📌 Listar confirmaciones
@confirmations_bp.route("/")
def list_confirmations():

    meses_disponibles = sorted(
        list({p["month"] for p in db.payments.find({"month": {"$exists": True}})}),
        reverse=True
    )


    now = datetime.now()
    month = now.month
    year = now.year

    # Confirmaciones de este mes
    confirmaciones = list(db.confirmations.find({"month": month, "year": year}))
    confirmados_ids = {c["student_id"]: str(c["_id"]) for c in confirmaciones}  # ✅ convertimos _id a string

    # Todos los alumnos
    students = list(db.students.find({"deleted": False}).sort("category", 1))

    # Clasificar alumnos
    confirmados = []
    no_confirmados = []

    for s in students:
        alumno = {
            "id": str(s["_id"]),
            "nombre": f'{s["first_name"]} {s["last_name"]}',
            "categoria": s.get("category", ""),
            "confirmado": False,
            "confirmacion_id": None
        }

        if str(s["_id"]) in confirmados_ids:
            alumno["confirmado"] = True
            alumno["confirmacion_id"] = confirmados_ids[str(s["_id"])]
            confirmados.append(alumno)
        else:
            no_confirmados.append(alumno)

    total_mes = len(confirmados) + len(no_confirmados)

    return render_template(
        "confirmations/list.html",
        month_name=now.strftime("%B %Y"),
        total_mes=total_mes,
        meses_disponibles=meses_disponibles,
        confirmados=confirmados,
        no_confirmados=no_confirmados
    )

# 📌 Agregar confirmación
@confirmations_bp.route("/add/<student_id>")
def add_confirmation(student_id):
    now = datetime.now()

    # Evitar duplicados
    exists = db.confirmations.find_one({
        "student_id": student_id,
        "month": now.month,
        "year": now.year
    })
    if exists:
        flash("El alumno ya está confirmado este mes.", "warning")
        return redirect(url_for("confirmations.list_confirmations"))

    db.confirmations.insert_one({
        "student_id": student_id,
        "month": now.month,
        "year": now.year,
        "confirmed_at": now
    })
    flash("Alumno confirmado correctamente ✅", "success")
    return redirect(url_for("confirmations.list_confirmations"))

# 📌 Eliminar confirmación
@confirmations_bp.route("/delete/<id>")
def delete_confirmation(id):
    db.confirmations.delete_one({"_id": ObjectId(id)})
    flash("Confirmación eliminada ❌", "danger")
    return redirect(url_for("confirmations.list_confirmations"))