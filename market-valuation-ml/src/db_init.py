import sqlite3
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))
import config

"""Setting up the data base to the schema explain in the proposal"""


def initialize_db():
    print(f"Connecting DB @: {config.DB_PATH}")

    with sqlite3.connect(config.DB_PATH) as conn:
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Companies (
                ticker TEXT PRIMARY KEY,
                sector TEXT,
                industry_group TEXT
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Daily_Prices (
                ticker TEXT,
                date TEXT,
                close REAL,
                volume INTEGER,
                hl_pct_change REAL,
                PRIMARY KEY (ticker, date),
                FOREIGN KEY (ticker) REFERENCES Companies (ticker)
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Fundamentals (
                ticker TEXT,
                report_date TEXT,
                net_income REAL,
                total_assets REAL,
                shares_out INTEGER,
                PRIMARY KEY (ticker, report_date),
                FOREIGN KEY (ticker) REFERENCES Companies (ticker)
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Macro (
                date TEXT PRIMARY KEY,
                unemployment_rate REAL,
                cpi_yoy REAL,
                fed_rate REAL
            )
        """)

        conn.commit()
        print("Schema initialize successfully")


if __name__ == "__main__":
    initialize_db()
