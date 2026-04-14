import config
import sqlite3


with sqlite3.connect(config.DB_PATH) as conn:
    cursor = conn.cursor()

    cursor.execute("DROP TABLE IF EXISTS Daily_Prices")
    cursor.execute("DROP TABLE IF EXISTS Fundamentals")
    cursor.execute("DROP TABLE IF EXISTS Macro")

    # Daily_Prices table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Daily_Prices (
                ticker TEXT,
                date TEXT,
                open REAL,
                high REAL,
                low REAL,
                close REAL,
                adj_close REAL,
                volume INTEGER,
                hl_pct_change REAL,
                PRIMARY KEY (ticker, date),
                FOREIGN KEY (ticker) REFERENCES Companies (ticker)
            )
        """)

    # Fundamentals table
    cursor.execute("""
            CREATE TABLE IF NOT EXISTS Fundamentals (
                ticker TEXT,
                report_date TEXT,
                effective_date TEXT,
                net_income REAL,
                total_assets REAL,
                total_liabilities REAL,
                total_equity REAL,
                shares_out INTEGER,
                PRIMARY KEY (ticker, report_date),
                FOREIGN KEY (ticker) REFERENCES Companies (ticker)
            )
        """)

    # Macro table
    cursor.execute("""
            CREATE TABLE IF NOT EXISTS Macro (
                date TEXT PRIMARY KEY,
                unemployment_rate REAL,
                cpi_yoy REAL,
                fed_rate REAL
            )
        """)
    conn.commit()
