from datetime import datetime
from models import db, Family

# Czas rozpoczęcia i zakończenia gry
GAME_START_TIME = datetime(2024, 7, 18, 21, 53, 30)
GAME_END_TIME = datetime(2024, 7, 18, 21, 55, 30)

def game_in_progress():
    now = datetime.now()
    return GAME_START_TIME <= now <= GAME_END_TIME

def time_left():
    now = datetime.now()
    if now > GAME_END_TIME:
        return 0
    return (GAME_END_TIME - now).total_seconds()