from datetime import datetime, timedelta


def last_n_dates(n: int = 7) -> list[str]:
    """Return a list of the last n dates (oldest first) as ISO strings."""
    today = datetime.now().date()
    return [(today - timedelta(days=i)).isoformat() for i in range(n - 1, -1, -1)]
