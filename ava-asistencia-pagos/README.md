# AVA – Asistencia & Pagos (Flask + MongoDB + PWA)

Incluye:
- CRUD de alumnas
- Asistencia diaria por categoría
- Pagos mensuales con monto según plan (prellenado)
- PWA instalable
- Deploy en Render + MongoDB Atlas

## Variables de entorno
- `MONGO_URI` (MongoDB Atlas)
- `SECRET_KEY`
- `ADMIN_EMAIL`
- `ADMIN_PASSWORD`

## Local
```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env  # edita MONGO_URI
python app.py
# http://127.0.0.1:5000  (login con ADMIN_EMAIL / ADMIN_PASSWORD)
```

## Deploy en Render (gratis)
1. Crea un repo en GitHub con estos archivos.
2. En Render: **New → Web Service** → conecta el repo.
3. Build Command: `pip install -r requirements.txt`
4. Start Command: `gunicorn app:app`
5. Agrega Environment Variables: `MONGO_URI`, `SECRET_KEY`, `ADMIN_EMAIL`, `ADMIN_PASSWORD`.
6. Deploy. Listo.

## Categorías y planes
- Sub10/Sub12/Sub14/Sub16: 4 días = 90, 8 días = 160, 12 días = 240
- Jóvenes/Adultos: 4 días = 100
