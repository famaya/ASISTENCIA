from flask import Flask, render_template

from routes.students import students_bp
from routes.professors import professors_bp
from routes.groups import groups_bp
from routes.sedes import sedes_bp

app = Flask(__name__)

# Registrar Blueprints
app.register_blueprint(students_bp, url_prefix="/students")
app.register_blueprint(professors_bp, url_prefix="/professors")
app.register_blueprint(groups_bp, url_prefix="/groups")
app.register_blueprint(sedes_bp, url_prefix="/sedes")

@app.route("/")
def inicio():
    return render_template("index.html")


# ----- PWA -----
@app.get('/manifest.json')
def manifest():
    return app.send_static_file('manifest.json')

@app.get('/service-worker.js')
def sw():
    return app.send_static_file('service-worker.js')
if __name__ == "__main__":
    app.run(debug=True)
