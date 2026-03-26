from pathlib import Path
"""This is the config file for file paths that way it runs independent of the environment"""

ROOT_DIR = Path(__file__).resolve.parent

DATA_DIR = ROOT_DIR / 'data'
DB_PATH = DATA_DIR / 'market_data.db'
SRC_DIR = ROOT_DIR / 'src'