import config
import os
import requests
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


def grab_top_100_companies():
    """Purpose is to automate the download of the top 100 companies raw data and put it in the correct directory"""
    url = config.URLS["MARKET_CAP_RANKINGS"] + "?download=csv"

    # Im not a bot a swear
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

    SAVE_PATH = os.path.join(config.RAW_PATH, config.RAW_100_COMPANIES)

    try:
        print(f"Grabbing top 100 Companies by market cap {url}...")
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        os.makedirs(config.RAW_PATH, exists_ok=True)

        with open(SAVE_PATH, "wb") as f:
            f.write(response.content)

        print(f"Saved raw data to: {SAVE_PATH}")
        return SAVE_PATH

    except requests.exceptions.RequestException as e:
        print(f"Error: File not downloaded. Detail: {e}")
        return None


if __name__ == "__main__":
    grab_top_100_companies()
