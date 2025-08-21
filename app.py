from flask import Flask, render_template, request, redirect, url_for, session, send_file, flash
from datetime import datetime
from io import StringIO
import csv, json

from config import Config, CATEGORIES, PLANS
from auth import bp as auth_bp
import models

app = Flask(__name__)
app.config.from_object(Config)
app.register_blueprint(auth_bp)

# --- Auth middleware ---
@app.before_request
def require_login():
    open_paths = {"/login", "/static/", "/manifest.json", "/service-worker.js"}
    path = request.path
    if path == "/login" or path.startswith("/static/") or path in ("/manifest.json","/service-worker.js"):
        return
    if not session.get('user_id'):
        if path != "/login":
            return redirect(url_for('auth.login_form'))

# --- Home ---
@app.get('/')
def index():
    cats = CATEGORIES
    total_students = len(models.list_students())  # ya filtra activas
    today = datetime.today().strftime('%Y-%m-%d')
    return render_template('index.html', cats=cats, total_students=total_students, today=today)
    

# ----- Alumnas -----
@app.get('/students')
def students_list():
    category = request.args.get('category')
    items = models.list_students(category)
    return render_template('students_list.html', items=items, category=category, categories=CATEGORIES)

@app.get('/students/new')
@app.get('/students/<id>/edit')
def students_form(id=None):
    item = models.get_student(id) if id else None
    return render_template('students_form.html', item=item, categories=CATEGORIES, plans=PLANS, plans_json=json.dumps(PLANS, ensure_ascii=False))

@app.post('/students/save')
def students_save():
    sid = request.form.get('id')
    category = request.form.get('category','').strip()
    days = int(request.form.get('plan_days') or 0)
    fee = PLANS.get(category, {}).get(days, 0)

    data = {
        'first_name': request.form.get('first_name','').strip(),
        'last_name': request.form.get('last_name','').strip(),
        'category': category,
        'plan_days': days,
        'plan_fee': fee,
        'start_date': request.form.get('start_date',''),
        'phone': request.form.get('phone','').strip(),
        'guardian': request.form.get('guardian','').strip(),
        'notes': request.form.get('notes','').strip(),
    }
    if sid:
        models.update_student(sid, data)
        flash('Alumna actualizada', 'success')
    else:
        models.create_student(data)
        flash('Alumna creada', 'success')
    return redirect(url_for('students_list'))

@app.post('/students/<id>/delete')
def students_delete(id):
    models.delete_student(id)
    flash('Alumna eliminada', 'warning')
    return redirect(url_for('students_list'))

# ----- Asistencia -----
@app.get('/attendance')
def attendance_mark():
    category = request.args.get('category','')
    date_str = request.args.get('date', datetime.today().strftime('%Y-%m-%d'))
    items = models.list_students(category) if category else []
    return render_template('attendance_mark.html', items=items, category=category, date_str=date_str, categories=CATEGORIES)

@app.post('/attendance/save')
def attendance_save():
    category = request.form.get('category')
    date_iso = request.form.get('date')
    ids = request.form.getlist('student_id')
    marks = []
    for sid in ids:
        present = request.form.get(f'present_{sid}') == 'on'
        marks.append({'student_id': sid, 'present': present})
    models.mark_attendance(date_iso, marks, category)
    flash('Asistencia guardada', 'success')
    return redirect(url_for('attendance_mark', category=category, date=date_iso))

@app.get('/attendance/list')
def attendance_list():
    category = request.args.get('category')
    date_iso = request.args.get('date')
    items = models.list_attendance(date_iso, category)
    return render_template('attendance_list.html', items=items, category=category, date_str=date_iso)

@app.get('/attendance/export')
def attendance_export_csv():
    category = request.args.get('category')
    date_iso = request.args.get('date')
    items = models.list_attendance(date_iso, category)
    si = StringIO()
    writer = csv.writer(si)
    writer.writerow(["date", "category", "student_id", "present"])
    for it in items:
        writer.writerow([it.get('date'), it.get('category'), it.get('student_id'), it.get('present')])
    si.seek(0)
    return send_file(si, mimetype='text/csv', as_attachment=True, download_name=f"attendance_{date_iso or 'all'}.csv")

# ----- Pagos -----
@app.get('/payments')
def payments_list():
    category = request.args.get('category')
    month = request.args.get('month') or datetime.today().strftime('%Y-%m')
    studs = models.list_students(category)
    pay_map = models.payment_map_for_month(month)
    items = []
    for s in studs:
        sid = str(s['_id'])
        key = sid + month
        p = pay_map.get(key)
        items.append({
            'student': s,
            'month': month,
            'paid': bool(p),
            'amount': p.get('amount', 0) if p else 0,
            'method': p.get('method', '') if p else ''
        })
    return render_template('payments_list.html', items=items, category=category, month=month, categories=CATEGORIES)

@app.get('/payments/new')
def payments_form():
    student_id = request.args.get('student_id')
    month = request.args.get('month') or datetime.today().strftime('%Y-%m')
    # Prefill amount based on student's plan
    s = models.get_student(student_id) if student_id else None
    default_amount = s.get('plan_fee', 0) if s else 0
    return render_template('payments_form.html', student_id=student_id, month=month, default_amount=default_amount)

@app.post('/payments/save')
def payments_save():
    student_id = request.form.get('student_id')
    month = request.form.get('month')
    amount = float(request.form.get('amount') or 0)
    method = request.form.get('method')
    note = request.form.get('note')
    models.register_payment(student_id, month, amount, method, note)
    flash('Pago registrado', 'success')
    return redirect(url_for('payments_list', category=request.args.get('category'), month=month))

# ----- PWA -----
@app.get('/manifest.json')
def manifest():
    return app.send_static_file('manifest.json')

@app.get('/service-worker.js')
def sw():
    return app.send_static_file('service-worker.js')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
