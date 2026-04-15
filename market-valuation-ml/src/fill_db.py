import yfinance as yf
import pandas as pd
import sqlite3
import config
import os
import time


def populate_companies_table(limit=100):
    """
    Pull information from yahoo finance from the top 100 companies found in the top_100_usa_companies.csv
    """
    conn = sqlite3.connect(config.DB_PATH)
    cursor = conn.cursor()

    raw_df = pd.read_csv(
        os.path.join(config.RAW_PATH, config.RAW_100_COMPANIES), nrows=limit
    )

    print(f"Grabbing information for {len(raw_df)} companies...")
    for index, row in raw_df.iterrows():
        symbol = row["Symbol"]
        name = row["Name"]

        try:
            ticker = yf.Ticker(symbol)
            info = ticker.info

            sector = info.get("sector", "Unknown")
            industry = info.get("industry", "Unknown")

            cursor.execute(
                """
                INSERT OR REPLACE INTO Companies (ticker, name, sector, industry_group)
                VALUES (?,?,?,?)
                """,
                (symbol, name, sector, industry),
            )

            if index % 10 == 0:
                conn.commit()
                print(f"Progress: {index}/{len(raw_df)} companies done so far...")

            time.sleep(1.5)
        except Exception as e:
            print(f"Error processing {symbol}: {e}")
            continue

    conn.close()
    print("100 companies processed please verify!")


def populate_with_masters():
    conn = sqlite3.connect(config.DB_PATH)

    files_tables_tup = [
        ("cleaned_daily_master.csv", "Daily_Prices"),
        ("cleaned_fundamentals_master.csv", "Fundamentals"),
        ("cleaned_macro_master.csv", "Macro"),
    ]

    for fname, table in files_tables_tup:
        path = os.path.join(config.CLEANED_PATH, fname)

        if os.path.exists(path):
            df = pd.read_csv(path)
            df.to_sql(table, conn, if_exists="replace", index=False, chunksize=10000)
        else:
            print("Something went wrong")
    conn.close()


def audit_companies():
    """
    Check if there any missing data in the information commited to the data base from populate_companies_table
    """
    conn = sqlite3.connect(config.DB_PATH)
    query = """
        SELECT ticker, name FROM Companies 
        WHERE sector = 'Unknown' 
            OR industry_group = 'Unknown' 
            OR sector IS NULL 
            OR industry_group IS NULL
    """
    missing_data_df = pd.read_sql(query, conn)
    print("\n ###AUDIT OF COMPANY TABLE###")
    if not missing_data_df.empty:
        print(f"Found {len(missing_data_df)} missing records from company table")
        print(missing_data_df)
    else:
        print("No missing data! Knock on wood")

    conn.close()


def audit_masters():
    conn = sqlite3.connect(config.DB_PATH)

    tables = ["Daily_Prices", "Macro", "Fundamentals"]

    for table in tables:
        print(f"Top 5 rows of {table}")
        query = f"SELECT * FROM {table} LIMIT 5"
        df = pd.read_sql(query, conn)
        print(df)

        count = pd.read_sql(f"SELECT COUNT(*) as total FROM {table}", conn)
        print(f"Total rows in {table}: {count['total'][0]}")
    conn.close()


if __name__ == "__main__":
    # populate_companies_table(limit=100)
    # audit_companies()
    # populate_with_masters()
    audit_masters()
