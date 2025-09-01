from flask_sqlalchemy import SQLAlchemy
from datetime import date

db = SQLAlchemy()

# Tabla Profesores
class Profesor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    apellido = db.Column(db.String(100), nullable=False)
    dni = db.Column(db.String(20))
    telefono = db.Column(db.String(20))
    email = db.Column(db.String(120))

# Tabla Sedes
class Sede(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    direccion = db.Column(db.String(200), nullable=False)
    costo_horario = db.Column(db.Float)

# Tabla Alumnas
class Alumna(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    apellido = db.Column(db.String(100), nullable=False)
    fecha_nacimiento = db.Column(db.Date, nullable=False)
    apoderado = db.Column(db.String(100))
    telefono = db.Column(db.String(20))
    nota = db.Column(db.Text)
    fecha_ingreso = db.Column(db.Date, default=date.today)

    @property
    def edad(self):
        hoy = date.today()
        return hoy.year - self.fecha_nacimiento.year - (
            (hoy.month, hoy.day) < (self.fecha_nacimiento.month, self.fecha_nacimiento.day)
        )

    @property
    def categoria(self):
        if self.edad <= 11:
            return "Sub11"
        elif self.edad <= 12:
            return "Sub12"
        elif self.edad <= 14:
            return "Sub14"
        elif self.edad <= 16:
            return "Sub16"
        else:
            return "Jóvenes/Adultos"

# Tabla Grupos
class Grupo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    horario = db.Column(db.String(100))
    profesor_id = db.Column(db.Integer, db.ForeignKey('profesor.id'))
    sede_id = db.Column(db.Integer, db.ForeignKey('sede.id'))

    profesor = db.relationship("Profesor", backref="grupos")
    sede = db.relationship("Sede", backref="grupos")
    alumnas = db.relationship("Alumna", secondary="grupo_alumna", backref="grupos")

# Relación muchos a muchos Grupo ↔ Alumnas
grupo_alumna = db.Table(
    "grupo_alumna",
    db.Column("grupo_id", db.Integer, db.ForeignKey("grupo.id")),
    db.Column("alumna_id", db.Integer, db.ForeignKey("alumna.id"))
)

# Tabla Asistencia
class Asistencia(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    alumna_id = db.Column(db.Integer, db.ForeignKey('alumna.id'))
    grupo_id = db.Column(db.Integer, db.ForeignKey('grupo.id'))
    fecha = db.Column(db.Date, nullable=False)
    presente = db.Column(db.Boolean, default=False)

    alumna = db.relationship("Alumna", backref="asistencias")
    grupo = db.relationship("Grupo", backref="asistencias")
