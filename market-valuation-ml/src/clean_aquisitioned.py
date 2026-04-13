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
                "totalShareHolderEquity": "total_equity",
                "commonStockSharesOutstanding": "shares_outstanding",
                "ticker": "ticker",
            }

            df_filtered = df[list(target_cols.keys())].rename(columns=target_cols)

            numeric_cols = [
                "net_income",
                "total_assets",
                "total_liabilities",
                "total_liabilities",
                "total_equity",
                "shares_outstanding",
            ]

            for col in numeric_cols:
                df_filtered[col] = pd.to_numeric(
                    df_filtered[col].replace("None", np.nan)
                )

            df_filtered["effective_date"] = pd.to_datetime(
                df_filtered["report_date"]
            ) + pd.Timedelta(days=45)

            cleaned_data.append(df_filtered)
            print(f"Cleaned data for {filename}")

    master_df = pd.concat(cleaned_data, ignore_index=True)
    master_path = os.path.join(config.CLEANED_PATH, "cleaned_fundamentals_master.csv")
    master_df.to_csv(master_path, index=False)
    return master_df
