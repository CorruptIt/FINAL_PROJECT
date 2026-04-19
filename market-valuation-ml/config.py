import os
from dotenv import load_dotenv

"""This is the config file for file paths that way it runs independent of the environment"""
# DIR Structure
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
SRC_DIR = os.path.join(BASE_DIR, "src")
MODELS_DIR = os.path.join(BASE_DIR, "models")

# Paths
DB_PATH = os.path.join(DATA_DIR, "market_data.db")
RAW_PATH = os.path.join(DATA_DIR, "raw")
DAILY_PATH = os.path.join(RAW_PATH, "daily")
FUNDAMENTALS_PATH = os.path.join(RAW_PATH, "fundamentals")
MACRO_PATH = os.path.join(RAW_PATH, "macro")
CLEANED_PATH = os.path.join(DATA_DIR, "cleaned")

# Urls
URLS = {
    "MARKET_CAP_RANKINGS": "https://companiesmarketcap.com/usa/largest-companies-in-the-usa-by-market-cap/",
    "FRED_BASE": "https://fred.stlouisfed.org/",
    "ALPHA_VANTAGE_BASE": "https://www.alphavantage.co",
    "YAHOO_FINANCE": "https://finance.yahoo.com/",
}

# File Names
RAW_100_COMPANIES = "top_100_usa_companies.csv"

load_dotenv()
ALPHA_VANTAGE_KEY = os.getenv("ALPHA_VANTAGE_KEY")
FRED_API_KEY = os.getenv("FRED_API_KEY")

os.makedirs(RAW_PATH, exist_ok=True)
os.makedirs(SRC_DIR, exist_ok=True)
