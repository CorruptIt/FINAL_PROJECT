import pandas as pd
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score
import numpy as np
import os
import config


def train_gbm():
    path = os.path.join(config.CLEANED_PATH, "training_set.csv")
    df = pd.read_csv(path)

    # drop columns that are not numeric and ones that prevent bias
    drop_cols = [
        "date",
        "ticker",
        "target_market_cap",
        "log_target_market_cap",
        "market_cap",
        "log_market_cap",
        "effective_date",
        "report_date",
        "open",
        "high",
        "low",
        "close",
        "adj_close",
    ]

    X = df.drop(columns=drop_cols)
    y = df["log_target_market_cap"]

    split = int(len(df) * 0.8)
    X_train, X_test = X.iloc[:split], X.iloc[split:]
    y_train, y_test = y.iloc[:split], y.iloc[split:]

    model = xgb.XGBRegressor(
        n_estimators=1000,
        learning_rate=0.05,
        max_depth=6,
        subsample=0.8,
        colsample_bytree=0.8,
        n_jobs=-1,
        early_stopping_rounds=50,
    )

    model.fit(X_train, y_train, eval_set=[(X_test, y_test)], verbose=100)

    preds = model.predict(X_test)
    mae = mean_absolute_error(np.expm1(y_test), np.expm1(preds))
    r2 = r2_score(y_test, preds)

    print(f"R2 Score: {r2:.4f}")
    print(f"MAE : ${mae:,.2f}")
    model_path = os.path.join(config.MODELS_DIR, "xg_model.json")
    model.save_model(model_path)

    # save results for further analyzation
    model_results = df.iloc[split:][[
        "ticker", "date", "log_target_market_cap"]].copy()
    model_results["actual_market_cap"] = np.expm1(
        model_results["log_target_market_cap"]
    )
    model_results["predicted_market_cap"] = np.expm1(preds)

    model_results["absolute_error"] = abs(
        model_results["actual_market_cap"] -
        model_results["predicted_market_cap"]
    )
    model_results["percent_error"] = (
        model_results["absolute_error"] / model_results["actual_market_cap"]
    ) * 100

    model_results_path = os.path.join(
        config.CLEANED_PATH, "xgb_test_results.csv")
    model_results.to_csv(model_results_path, index=False)

    return model

    # if __name__ == "__main__":
    # train_gbm()
