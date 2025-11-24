# src/application/use_cases/history.py
from datetime import datetime, timedelta

def query_history(history_repo, attr: str, minutes: int = 10):
    # adjust retention if necessary (optional)
    history_repo.set_retention(minutes)
    return history_repo.get_history(attr)
