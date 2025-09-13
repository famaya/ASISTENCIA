from flask import Blueprint, render_template, request, redirect, url_for
from db import db
from bson.objectid import ObjectId
from datetime import datetime
from utils import calcular_categoria

students_bp = Blueprint("students", __name__, url_prefix="/students")

# LISTAR
@students_bp.route("/")
def lista_students():
    # Obtener filtros desde el query string
    filtro_grupo = request.args.get("grupo")
    filtro_categoria = request.args.get("categoria")
    query = {}
    if filtro_grupo:
        query["group"] = filtro_grupo  # suponiendo que guardas el grupo en cada alumno
    if filtro_categoria:
        query["category"] = filtro_categoria

    # Obtener alumnos filtrados

    # Traemos todas las alumnas de MongoDB
    students_cursor = db["students"].find(query)

# Obtener lista única de categorías y grupos para los filtros
    categorias = db["students"].distinct("category")
    grupos = db["students"].distinct("group")
    students_list = []

    for s in students_cursor:
        students_list.append({
            "_id": str(s["_id"]),
            "first_name": s.get("first_name", ""),
            "last_name": s.get("last_name", ""),
            "category": s.get("category", ""),
            "plan_days": s.get("plan_days", 0),
	    "birth_date": s.get("birth_date",""),
            "plan_fee": s.get("plan_fee", 0),
            "start_date": s.get("start_date", ""),
            "phone": s.get("phone", ""),
            "guardian": s.get("guardian", ""),
            "notes": s.get("notes", "")
        })

    return render_template("students/lista.html", students=students_list, categorias=categorias, 
                           grupos=grupos)


# AGREGAR
@students_bp.route("/agregar", methods=["GET", "POST"])
def agregar_students():
    if request.method == "POST":
        fecha_nac = request.form["birth_date"]  # input type="date"
        nueva = {
            "first_name": request.form["first_name"],
            "last_name": request.form["last_name"],
            "birth_date": fecha_nac,
            "category": calcular_categoria(fecha_nac),
            "plan_days": int(request.form.get("plan_days", 0)),
            "plan_fee": float(request.form.get("plan_fee", 0)),
            "start_date": request.form.get("start_date", ""),
            "phone": request.form.get("phone", ""),
            "guardian": request.form.get("guardian", ""),
            "notes": request.form.get("notes", ""),
            "deleted": False,
            "created_at": datetime.utcnow()
        }
        db["students"].insert_one(nueva)
        return redirect(url_for("students.lista_students"))

    return render_template("students/agregar.html")

# EDITAR
@students_bp.route("/editar/<id>", methods=["GET", "POST"])
def editar_students(id):
    student = db["students"].find_one({"_id": ObjectId(id)})

    if request.method == "POST":
        fecha_nac = request.form["birth_date"]
        db["students"].update_one(
            {"_id": ObjectId(id)},
            {"$set": {
                "first_name": request.form["first_name"],
                "last_name": request.form["last_name"],
                "category": calcular_categoria(fecha_nac),
		"birth_date": request.form["birth_date"],
                "plan_days": int(request.form.get("plan_days", 0)),
                "plan_fee": int(request.form.get("plan_fee", 0)),
                "start_date": request.form["start_date"],
                "phone": request.form.get("phone", ""),
                "guardian": request.form.get("guardian", ""),
                "notes": request.form.get("notes", "")
            }}
        )
        return redirect(url_for("students.lista_students"))

    return render_template("students/editar.html", student=student)

# ----------------------------
# ELIMINAR ALUMNA
# ----------------------------
@students_bp.route("/eliminar/<id>")
def eliminar_students(id):
    db["students"].delete_one({"_id": ObjectId(id)})
    return redirect(url_for("students.lista_students"))