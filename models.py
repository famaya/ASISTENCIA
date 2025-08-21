from datetime import datetime
from bson import ObjectId
from db import students, attendance, payments
from utils import month_key



def list_students(category: str | None = None):
    q = {"$or": [{"deleted": {"$exists": False}}, {"deleted": False}]}
    if category:
        q["category"] = category
    return list(students.find(q).sort([("last_name", 1), ("first_name", 1)]))

def get_student(student_id: str):
    from bson import ObjectId
    return students.find_one({"_id": ObjectId(student_id), "deleted": {"$ne": True}})

def create_student(data: dict):
    data.update({
        "created_at": datetime.utcnow(),
        "deleted": False
    })
    students.insert_one(data)

def update_student(student_id: str, data: dict):
    students.update_one({"_id": ObjectId(student_id)}, {"$set": data})

def delete_student(student_id: str):
    students.update_one({"_id": ObjectId(student_id)}, {"$set": {"deleted": True}})

# -------- Asistencia --------
def mark_attendance(date_iso: str, marks: list[dict], category: str):
    # date_iso: 'YYYY-MM-DD'
    for m in marks:
        attendance.update_one(
            {"date": date_iso, "student_id": m['student_id']},
            {"$set": {
                "date": date_iso,
                "category": category,
                "present": bool(m.get('present', False)),
                "marked_at": datetime.utcnow(),
            }},
            upsert=True
        )

def list_attendance(date_iso: str | None = None, category: str | None = None):
    q = {}
    if date_iso:
        q["date"] = date_iso
    if category:
        q["category"] = category
    return list(attendance.find(q))

# -------- Pagos --------
def register_payment(student_id: str, month_ym: str, amount: float, method: str, note: str | None = None):
    payments.update_one(
        {"student_id": student_id, "month": month_ym},
        {"$set": {
            "student_id": student_id,
            "month": month_ym,
            "amount": amount,
            "method": method,
            "note": note or "",
            "paid_at": datetime.utcnow(),
        }},
        upsert=True
    )

def payment_map_for_month(month_ym: str):
    return {p['student_id']+p['month']: p for p in payments.find({"month": month_ym})}
