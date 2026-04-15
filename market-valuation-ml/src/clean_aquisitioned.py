import pandas as pd
import os
import numpy as np
import config


def clean_fundamental():
    """
    func to clean raw fundamental data,
    filter only the cols that are needed for analysis
    """
    raw_folder = config.FUNDAMENTALS_PATH
    cleaned_data = []

    for filename in os.listdir(raw_folder):
        if filename.endswith(".csv"):
            file_path = os.path.join(raw_folder, filename)
            df = pd.read_csv(file_path)

            target_cols = {
                "fiscalDateEnding_inc": "report_date",
                "netIncome": "net_income",
                "totalAssets": "total_assets",
                "totalLiabilities": "total_liabilities",
                "totalShareholderEquity": "total_equity",
                "commonStockSharesOutstanding": "shares_out",
                "ticker": "ticker",
            }

            df_filtered = df[list(target_cols.keys())].rename(columns=target_cols)

            numeric_cols = [
                "net_income",
                "total_assets",
                "total_liabilities",
                "total_equity",
                "shares_out",
            ]

            for col in numeric_cols:
                df_filtered[col] = pd.to_numeric(
                    df_filtered[col].replace("None", np.nan)
                )

            df_filtered["effective_date"] = pd.to_datetime(
                df_filtered["report_date"]
            ) + pd.Timedelta(days=45)

            df_filtered["report_date"] = pd.to_datetime(
                df_filtered["report_date"], utc=True
            ).dt.strftime("%Y-%m-%d")
            df_filtered["effective_date"] = df_filtered["effective_date"].dt.strftime(
                "%Y-%m-%d"
            )

            cleaned_data.append(df_filtered)
            print(f"Cleaned data for {filename}")

    master_df = pd.concat(cleaned_data, ignore_index=True)
    master_df = master_df.sort_values(by=["ticker", "report_date"])
    master_path = os.path.join(config.CLEANED_PATH, "cleaned_fundamentals_master.csv")
    master_df.to_csv(master_path, index=False)
    return master_df


def clean_daily():
    """
    func to clean daily data,
    filtering data only necessary for analysis
    """

    raw_folder = config.DAILY_PATH
    cleaned_data = []

    for filename in os.listdir(raw_folder):
        if filename.endswith(".csv"):
            file_path = os.path.join(raw_folder, filename)
            df = pd.read_csv(file_path)

            target_cols = {
                "Date": "date",
                "ticker": "ticker",
                "Open": "open",
                "High": "high",
                "Low": "low",
                "Close": "close",
                "Volume": "volume",
            }

            df_cleaned = df[list(target_cols.keys())].rename(columns=target_cols)
            df_cleaned["adj_close"] = df_cleaned["close"]
            df_cleaned["hl_pct_change"] = (
                df_cleaned["high"] - df_cleaned["low"]
            ) / df_cleaned["low"]

            df_cleaned["date"] = pd.to_datetime(
                df_cleaned["date"], utc=True
            ).dt.strftime("%Y-%m-%d")

            num_cols = ["open", "high", "low", "close", "adj_close", "hl_pct_change"]

            df_cleaned[num_cols] = df_cleaned[num_cols].apply(
                pd.to_numeric, errors="coerce"
            )
            df_cleaned["volume"] = (
                pd.to_numeric(df_cleaned["volume"], errors="coerce")
                .fillna(0)
                .astype(int)
            )

            cleaned_data.append(df_cleaned)

    if cleaned_data:
        master_daily_df = pd.concat(cleaned_data, ignore_index=True)
        master_path = os.path.join(config.CLEANED_PATH, "cleaned_daily_master.csv")
        master_daily_df.to_csv(master_path, index=False)
        return master_daily_df


def clean_macro():
    """
    func to filter and clean macro data
    """
    raw_folder = config.MACRO_PATH
    cleaned_data = []

    for filename in os.listdir(raw_folder):
        if filename.endswith(".csv"):
            file_path = os.path.join(raw_folder, filename)
            df = pd.read_csv(file_path)

            df = df.rename(columns={df.columns[0]: "date"})

            target_cols = {
                "date": "date",
                "unemployment_rate": "unemployment_rate",
                "cpi_index": "cpi_index",
                "fed_funds_rate": "fed_rate",
            }

            df_cleaned = df[list(target_cols.keys())].rename(columns=target_cols)

            df_cleaned["date"] = pd.to_datetime(
                df_cleaned["date"], utc=True
            ).dt.strftime("%Y-%m-%d")
            num_cols = ["unemployment_rate", "cpi_index", "fed_rate"]
            df_cleaned[num_cols] = df_cleaned[num_cols].apply(
                pd.to_numeric, errors="coerce"
            )

            df_cleaned["cpi_yoy"] = df_cleaned["cpi_index"].pct_change(periods=12) * 100
            df_final = df_cleaned[df_cleaned["date"] >= "2005-01-01"].copy()

            sql_cols = ["date", "unemployment_rate", "cpi_yoy", "fed_rate"]

            df_final = df_final[sql_cols]
            cleaned_data.append(df_final)

        if cleaned_data:
            macro_master_df = pd.concat(cleaned_data, ignore_index=True)

            macro_master_df = macro_master_df.sort_values(by="date")

            master_path = os.path.join(config.CLEANED_PATH, "cleaned_macro_master.csv")
            macro_master_df.to_csv(master_path, index=False)
            return macro_master_df


# if __name__ == "__main__":
# clean_daily()
# clean_fundamental()
# clean_macro()
