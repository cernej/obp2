import sqlite3
from datetime import date, timedelta
from pathlib import Path

# Simple deterministic test dataset for the last 7 days.
TEST_RATES = {
    "EUR": (1, 24.80),
    "USD": (1, 22.90),
    "GBP": (1, 29.20),
    "PLN": (1, 5.75),
}


def _db_path() -> Path:
    return Path(__file__).resolve().parent / "instance" / "sqlite.db"


def seed_last_week() -> tuple[int, int, str]:
    """Insert or update test rates for the last 7 days (including today)."""
    db_path = _db_path()
    db_path.parent.mkdir(parents=True, exist_ok=True)

    inserted = 0
    updated = 0

    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    # Keep schema aligned with SQLAlchemy model in cviceni3/models.py.
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS rate (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date VARCHAR(10) NOT NULL,
            code VARCHAR(3) NOT NULL,
            amount INTEGER NOT NULL,
            rate FLOAT NOT NULL
        )
        """
    )

    for offset in range(7):
        day = date.today() - timedelta(days=offset)
        day_str = day.isoformat()

        for code, (amount, base_rate) in TEST_RATES.items():
            # Slight day-based variation to make test data realistic.
            rate_value = round(base_rate + (offset * 0.03), 4)
            cur.execute(
                "SELECT id FROM rate WHERE date = ? AND code = ? LIMIT 1",
                (day_str, code),
            )
            row = cur.fetchone()

            if row:
                cur.execute(
                    "UPDATE rate SET amount = ?, rate = ? WHERE id = ?",
                    (amount, rate_value, row[0]),
                )
                updated += 1
            else:
                cur.execute(
                    "INSERT INTO rate (date, code, amount, rate) VALUES (?, ?, ?, ?)",
                    (day_str, code, amount, rate_value),
                )
                inserted += 1

    conn.commit()
    conn.close()

    return inserted, updated, str(db_path)


if __name__ == "__main__":
    inserted_count, updated_count, database_path = seed_last_week()
    print(
        "Seed completed for last 7 days: "
        f"inserted={inserted_count}, updated={updated_count}, db='{database_path}'"
    )
