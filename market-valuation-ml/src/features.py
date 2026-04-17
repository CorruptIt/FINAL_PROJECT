import pandas as pd
import sqlite3
import numpy as np
import os
import config


def create_training_set():
    """
    Load tables from sql to pandas
    Join tables in pandas
    Create features save model csv
    """
    conn = sqlite3.connect(config.DB_PATH)

    daily_prices = pd.read_sql("SELECT * FROM Daily_Prices ORDER BY date", conn)
    fundamentals = pd.read_sql(
        "SELECT * FROM Fundamentals ORDER BY effective_date", conn
    )
    macro = pd.read_sql("SELECT * FROM Macro ORDER BY date", conn)

    daily_prices["date"] = pd.to_datetime(daily_prices["date"])
    fundamentals["effective_date"] = pd.to_datetime(fundamentals["effective_date"])
    macro["date"] = pd.to_datetime(macro["date"])

    daily_prices = daily_prices.sort_values(by="date")
    fundamentals = fundamentals.sort_values(by="effective_date")
    macro = macro.sort_values(by="date")

    # time series aware join daily_prices and fundamentals focusing on tickers
    df = pd.merge_asof(
        daily_prices,
        fundamentals,
        left_on="date",
        right_on="effective_date",
        by="ticker",
        direction="backward",
    )
    # time series aware join for merged above and macro
    df = pd.merge_asof(
        df.sort_values("date"),
        macro,
        on="date",
        direction="backward",
    )

    # ffill data to handle NaN values
    df = df.sort_values(["ticker", "date"])
    possible_NaN_cols = [
        "net_income",
        "total_equity",
        "shares_out",
        "unemployment_rate",
        "cpi_yoy",
        "fed_rate",
    ]
    df[possible_NaN_cols] = df.groupby("ticker")[possible_NaN_cols].ffill()

    df["market_cap"] = df["close"] * df["shares_out"]

    df["pe_ratio"] = df["market_cap"] / df["net_income"].replace(0, np.nan)
    df["pb_ratio"] = df["market_cap"] / df["total_equity"].replace(0, np.nan)

    # shift 30 days prior so our model can predict
    df["target_market_cap"] = df.groupby("ticker")["market_cap"].shift(-30)

    # Normalize market cap
    df["log_market_cap"] = np.log1p(df["market_cap"])
    df["log_target_market_cap"] = np.log1p(df["target_market_cap"])

    # drop nan values

    df = df.dropna(subset=["log_target_market_cap", "shares_out"])

    conn.close()

    path = os.path.join(config.CLEANED_PATH, "training_set.csv")
    df.to_csv(path, index=False)

    print(f"training_set rows : {df.shape[0]}\n training_set cols : {df.shape[1]}")
    print(df[["log_market_cap", "log_target_market_cap"]].corr())


if __name__ == "__main__":
    create_training_set()
