from flask import Blueprint, render_template, request, redirect, url_for, flash
from db import db
from datetime import datetime
from bson.objectid import ObjectId

payments_bp = Blueprint("payments", __name__, url_prefix="/payments")

# 📌 Listar pagos por mes
@payments_bp.route("/")
def list_payments():
    meses_disponibles = sorted(
        list({p["month"] for p in db.payments.find({"month": {"$exists": True}})}),
        reverse=True
    )

    month = request.args.get("month", datetime.now().strftime("%Y-%m"))

    now = datetime.now()
    confirmados = list(db.confirmations.find({"month": now.month, "year": now.year}))

    confirmed_students = {}
    for c in confirmados:
        student = db.students.find_one({"_id": ObjectId(c["student_id"])})
        if student:
            confirmed_students[str(student["_id"])] = {
                "name": f'{student["first_name"]} {student["last_name"]}',
                "category": student.get("category", "Sin categoría")
            }

    payments = list(db.payments.find({"month": month}))
    for p in payments:
        student = db.students.find_one({"_id": ObjectId(p["student_id"])})
        if student:
            p["student_name"] = f'{student["first_name"]} {student["last_name"]}'
            p["category"] = student.get("category", "Sin categoría")
        else:
            p["student_name"] = "Alumno eliminado"
            p["category"] = "N/A"

    paid_ids = {p["student_id"] for p in payments}

    pendientes = []
    for sid, info in confirmed_students.items():
        if sid not in paid_ids:
            pendientes.append({
                "student_id": sid,
                "student_name": info["name"],
                "category": info["category"]
            })

    payments.sort(key=lambda x: (x["category"], x["student_name"]))
    pendientes.sort(key=lambda x: (x["category"], x["student_name"]))

    # 👉 Totales para resumen
    total_confirmados = len(confirmed_students)
    total_pagaron = len(payments)
    total_pendientes = len(pendientes)

    return render_template(
        "payments/list.html",
        payments=payments,
        pendientes=pendientes,
        meses_disponibles=meses_disponibles,
        month=month,
        total_confirmados=total_confirmados,
        total_pagaron=total_pagaron,
        total_pendientes=total_pendientes
    )


@payments_bp.route("/agregar", methods=["GET", "POST"])
def add_payment():
    if request.method == "POST":
        student_id = request.form.get("student_id")
        amount = float(request.form.get("amount", 0))
        method = request.form.get("method")
        note = request.form.get("note", "")

        month_str = datetime.now().strftime("%Y-%m")

        nuevo_pago = {
            "student_id": student_id,
            "month": month_str,
            "amount": amount,
            "method": method,
            "note": note,
            "paid_at": datetime.now()
        }

        db.payments.insert_one(nuevo_pago)
        return redirect(url_for("payments.list_payments"))

    students = list(db.students.find().sort("first_name", 1))
    preselect_id = request.args.get("student_id")  # 🔹 capturar el alumno desde la URL
    return render_template("payments/add.html", students=students, preselect_id=preselect_id)


# 📌 Eliminar pago
@payments_bp.route("/delete/<id>")
def delete_payment(id):
    db.payments.delete_one({"_id": ObjectId(id)})
    flash("❌ Pago eliminado", "danger")
    return redirect(url_for("payments.list_payments"))