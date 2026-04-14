import yfinance as yf
from fredapi import Fred
from alpha_vantage.fundamentaldata import FundamentalData
import sqlite3
import os
import config
import pandas as pd
import time
from datetime import datetime, timedelta

# 5 year calculation for macro data
end_date = datetime.now()
start_date = datetime(2005, 1, 1)


def get_db_connection():
    """
    func to get sql connection
    """
    return sqlite3.connect(config.DB_PATH)


def get_tickers_from_db():
    """
    get the tickers from the DB
    """
    conn = get_db_connection()

    query = "SELECT ticker FROM Companies"
    tickers = pd.read_sql(query, conn)["ticker"].tolist()
    conn.close()
    return tickers


def get_daily_prices_raw(tickers):
    """
    utilizing yahoo finance get all
    daily price data from the past 5 years for
    each ticker
    """
    for ticker in tickers:
        print(f"Getting stock history for {ticker}")
        stock = yf.Ticker(ticker)
        daily_df = stock.history(start="2005-01-01", auto_adjust=True)

        if not daily_df.empty:
            daily_df["ticker"] = ticker
            daily_path = os.path.join(config.DAILY_PATH, f"{ticker}_daily.csv")
            daily_df.to_csv(daily_path)
            print(f"Saved daily stock information for {ticker}: {daily_path}")
        time.sleep(1.5)


def get_fundamentals_raw(tickers):
    """
    get all fundamental data for each ticker
    in the db
    """
    fd = FundamentalData(key=config.ALPHA_VANTAGE_KEY, output_format="pandas")

    for ticker in tickers:
        try:
            print(
                f"I can't believe I paid for this api to get 20y's of quarterly data for {
                    ticker
                }"
            )

            income_df, _ = fd.get_income_statement_quarterly(symbol=ticker)

            time.sleep(15)  # mandatory for rate limits

            balance_df, _ = fd.get_balance_sheet_quarterly(symbol=ticker)

            if not income_df.empty and not balance_df.empty:
                merged = income_df.join(
                    balance_df, how="outer", lsuffix="_inc", rsuffix="_bs"
                )
                merged["ticker"] = ticker

                fund_path = os.path.join(
                    config.FUNDAMENTALS_PATH, f"{ticker}_20y_fundamentals.csv"
                )
                merged.to_csv(fund_path)

                print(f"Saved fundamentals for {ticker} to : {fund_path}")

            time.sleep(15)
        except Exception as e:
            print(f"Error for {ticker} : {e}")

            time.sleep(60)


def get_macro_raw():
    """
    get macro economic data from fred
    from the past 5 years
    """
    fred = Fred(api_key=config.FRED_API_KEY)
    indicators = {
        "unemployment_rate": "UNRATE",
        "fed_funds_rate": "FEDFUNDS",
        "cpi_index": "CPIAUCSL",
    }

    macro_df = pd.DataFrame()

    for name, series_id in indicators.items():
        try:
            series = fred.get_series(
                series_id,
                observation_start=start_date.strftime("%Y-%m-%d"),
                observation_end=end_date.strftime("%Y-%m-%d"),
            )
            macro_df[name] = series

        except Exception as e:
            print(f"Error {name} : {e}")

    if not macro_df.empty:
        macro_path = os.path.join(config.MACRO_PATH, "us_macro_20y.csv")
        macro_df.to_csv(macro_path)
        print(f"Macro data saved to {macro_path}")


if __name__ == "__main__":
    ticker_list = get_tickers_from_db()
    get_daily_prices_raw(ticker_list)
    get_macro_raw()
    # get_fundamentals_raw(ticker_list)
