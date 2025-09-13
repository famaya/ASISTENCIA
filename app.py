from flask import Flask, render_template
from db import db
from datetime import datetime, timedelta
from bson.objectid import ObjectId
from config import Config

from routes.students import students_bp
from routes.professors import professors_bp
from routes.groups import groups_bp
from routes.sedes import sedes_bp
from routes.index import index_bp
from routes.confirmations import confirmations_bp
from routes.payments import payments_bp


app = Flask(__name__)
app.config.from_object(Config)

# Registrar Blueprints

app.register_blueprint(index_bp)
app.register_blueprint(students_bp, url_prefix="/students")
app.register_blueprint(professors_bp, url_prefix="/professors")
app.register_blueprint(groups_bp, url_prefix="/groups")
app.register_blueprint(sedes_bp, url_prefix="/sedes")
app.register_blueprint(confirmations_bp, url_prefix="/confirmations")
app.register_blueprint(payments_bp, url_prefix="/payments")


if __name__ == "__main__":
    app.run(debug=True)