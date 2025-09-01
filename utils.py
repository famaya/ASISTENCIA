from datetime import datetime
def month_key(date: datetime) -> str:
    return date.strftime("%Y-%m")

def calcular_categoria(fecha_nac):
    hoy = datetime.today()
    fecha_nac_dt = datetime.strptime(fecha_nac, "%Y-%m-%d")
    edad = hoy.year - fecha_nac_dt.year - ((hoy.month, hoy.day) < (fecha_nac_dt.month, fecha_nac_dt.day))

    if edad <= 10:
        return "Sub10"
    elif edad <= 12:
        return "Sub12"
    elif edad <= 14:
        return "Sub14"
    elif edad <= 16:
        return "Sub16"
    elif edad <= 18:
        return "Jóvenes"
    else:
        return "Adultos"