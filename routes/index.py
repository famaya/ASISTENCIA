from flask import Blueprint, render_template
from db import db
from datetime import datetime, timedelta
from bson.objectid import ObjectId
from collections import defaultdict

index_bp = Blueprint('index', __name__)

@index_bp.route("/")
def dashboard():
    ahora = datetime.utcnow()
    now = datetime.utcnow()
    month_str = now.strftime("%Y-%m")   # ejemplo: "2025-09"
    start_of_month = datetime(now.year, now.month, 1)

    # --- Totales ---
    total_students = db["students"].count_documents({})
    total_professors = db["professors"].count_documents({})
    total_sedes = db["sedes"].count_documents({})
    total_groups = db["groups"].count_documents({})

    # --- Último mes ---
    students_last = db["students"].count_documents({"created_at": {"$gte": start_of_month}})
    professors_last = db["professors"].count_documents({"created_at": {"$gte": start_of_month}})
    sedes_last = db["sedes"].count_documents({"created_at": {"$gte": start_of_month}})
    groups_last = db["groups"].count_documents({"created_at": {"$gte": start_of_month}})

    # Nombre del mes
    #month_name = now.strftime("%B %Y")  # Ej: "Septiembre 2025"
     # Nombre del mes actual
    meses = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
             "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
    month_name= meses[ahora.month - 1]

    # IDs confirmados este mes
    confirmed_ids = [str(c["student_id"]) for c in db.confirmations.find({
        "month": now.month
    })]

    # IDs que pagaron este mes
    paid_ids = [str(p["student_id"]) for p in db.payments.find({
        "month": month_str
    })]

    # Unimos confirmados + pagos (para no duplicar usamos set)
    active_ids = list(set(confirmed_ids + paid_ids))

    # Total del mes (activos)
    total_month = len(active_ids)

    # Listas detalladas
    confirmed_students = list(db.students.find({"_id": {"$in": [ObjectId(sid) for sid in confirmed_ids]}}))
    not_confirmed_students = list(db.students.find({
        "_id": {"$nin": [ObjectId(sid) for sid in confirmed_ids]}
    }))

    payments_done = len(paid_ids)
    # --- Agrupar confirmados y pagos por categoría ---
    categorias = defaultdict(lambda: {"confirmados": 0, "pagaron": 0})

    for student in db.students.find({}):  # todos los alumnos activos
        sid = str(student["_id"])
        cat = student.get("category", "Sin categoría")

        if sid in confirmed_ids:
            categorias[cat]["confirmados"] += 1
        if sid in paid_ids:
            categorias[cat]["pagaron"] += 1



    return render_template(
        "index.html",
        total_students=total_students,
        students_last=students_last,
        total_professors=total_professors,
        professors_last=professors_last,
        total_sedes=total_sedes,
        sedes_last=sedes_last,
        total_groups=total_groups,
        groups_last=groups_last,
        month_name=month_name,
        total_month=total_month,
        confirmed_students=confirmed_students,
        not_confirmed_students=not_confirmed_students,
        categorias=dict(categorias),
        payments_done=payments_done
    )