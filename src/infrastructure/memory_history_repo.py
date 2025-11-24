# src/infrastructure/memory_history_repo.py
from collections import defaultdict, deque
from datetime import datetime, timedelta
from typing import Any, Deque, Tuple, Dict, List

class MemoryHistoryRepo:
    def __init__(self, retention_minutes: int = 10):
        self.retention = timedelta(minutes=retention_minutes)
        # attribute -> deque of (timestamp, value)
        self.store: Dict[str, Deque[Tuple[datetime, Any]]] = defaultdict(lambda: deque())

    def append(self, attr: str, value: Any, ts: datetime = None):
        ts = ts or datetime.utcnow()
        q = self.store[attr]
        q.append((ts, value))
        self._prune(attr)

    def _prune(self, attr: str):
        cutoff = datetime.utcnow() - self.retention
        q = self.store[attr]
        while q and q[0][0] < cutoff:
            q.popleft()

    def get_history(self, attr: str) -> List[Tuple[datetime, Any]]:
        self._prune(attr)
        return list(self.store[attr])

    def set_retention(self, minutes: int):
        self.retention = timedelta(minutes=minutes)
        # prune all
        for a in list(self.store.keys()):
            self._prune(a)
