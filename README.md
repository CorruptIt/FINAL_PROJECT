# Dedicated How To For Running This Pipeline

## Python Version

- 3.14

## Clone Repository

- git clone <git@github.com>:CorruptIt/FINAL_PROJECT.git

### Windows Instructions (Powershell)

- cd .\market-valuation-ml
- Create python Virtual Environment
  - python -m venv venv
- Activate Virtual Environment
  - .\venv\Scripts\Activate.ps1
- Install Requirements
  - pip install -r .\requirements-windows.txt
- create file .env for API keys
  - ALPHA_VANTAGE_KEY='your-key'
  - FRED_API_KEY='your-key'
- Run Pipeline
  - python -m src.main

  ### Linux Instructions

- cd ./market-valuation-ml/
- Create python Virtual Environment
  - python -m venv venv
- Install Requirements
  - pip install -r ./requirments.txt
- create file .env for API keys
  - ALPHA_VANTAGE_KEY='your-key'
  - FRED_API_KEY='your-key'
- Run Pipeline
  - python -m src.main

### Factors to Consider

- ALPHA Vantage is a paid API key. You can use ALPHA Vantage's free tier however you will hit rate limits.
- FRED API and Yahoo Finance is free to get FRED API key sign up for it on their website
- ALPHA Vantages requests take the longest time to pull about 30 minutes

### Running Half The Pipeline

- All raw data (.csv, .json) is supported and on github using lfs, pull that data if you do not want to run the entire pipeline.
- The Data Base on this Repository contains all information need to create a training set for the gradient boost model.
- If you do not want to run the entire pipeline ignore creating .env file with keys set up environment like the instructions above suggest and just run: python -m src.train_pipeline

### Notebooks Directory

- Contains all analysis of Gradient Boost Model
- In future iterations more models will be evaluated...
