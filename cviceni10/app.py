import sqlite3

class Payment:
    def __init__(self, db):
        self.db = db
        self.create_table()
    
    def create_table(self):
        cursor = self.db.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS payments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                amount REAL NOT NULL,
                description TEXT NOT NULL
            )
        """)
        self.db.commit()

    def add_payment(self, amount, description):
        cursor = self.db.cursor()
        cursor.execute("INSERT INTO payments (amount, description) VALUES (?, ?)", (amount, description))
        self.db.commit()

    
if __name__ == "__main__":
    db = sqlite3.connect("payments.db")
    payment = Payment(db)
    payment.add_payment(100, "Groceries")