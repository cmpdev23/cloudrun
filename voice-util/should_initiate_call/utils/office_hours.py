# utils\office_hours.py

from datetime import datetime, time
import pytz

# ⏱️ Heures d'ouverture générales
MIN_HOUR = 9
MAX_HOUR = 18

# ⏱️ Heures spécifiques à l’adjointe (vendredi = plus court)
ADJOINTE_HOURS = {
    # weekday: (start_hour, end_hour)
    0: (9, 17),  # Lundi
    1: (9, 17),
    2: (9, 17),
    3: (9, 17),
    4: (9, 12),  # Vendredi
    # 5, 6 = week-end
}

MONTREAL_TZ = pytz.timezone("America/Toronto")

def is_office_hour() -> bool:
    now = datetime.now(MONTREAL_TZ)
    weekday = now.weekday()
    current_time = now.time()

    # Fermé le week-end
    if weekday not in ADJOINTE_HOURS:
        return False

    start, end = ADJOINTE_HOURS[weekday]
    return time(start, 0) <= current_time <= time(end, 0)
