from db_init import initialize_db
from companies_raw import grab_top_100_companies
from fill_db import populate_companies_table, populate_with_masters
from data_acquisition import (
    get_db_connection,
    get_tickers_from_db,
    get_daily_prices_raw,
    get_fundamentals_raw,
    get_macro_raw,
)
from clean_aquisitioned import clean_fundamental, clean_daily, clean_macro
from features import create_training_set
from train_gbm import train_gbm


def pipeline():
    grab_top_100_companies()
    populate_companies_table()
    tickers = get_tickers_from_db()
    get_daily_prices_raw(tickers)
    get_fundamentals_raw(tickers)
    get_macro_raw()
    clean_daily()
    clean_fundamental()
    clean_macro()
    populate_with_masters()
    create_training_set()
    train_gbm()


if __name__ == "__main__":
    pipeline()
