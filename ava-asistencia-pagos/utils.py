from datetime import datetime
def month_key(date: datetime) -> str:
    return date.strftime("%Y-%m")
