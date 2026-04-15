# Market Valuation Model

### Database Schema: src/db_init.py

| Table Name       | Primary Key             | Foreign Key | Key Columns / Features                     |
| :--------------- | :---------------------- | :---------- | :----------------------------------------- |
| **Companies**    | `ticker`                | _None_      | `sector`, `industry_group`                 |
| **Daily Prices** | `(ticker, date)`        | `ticker`    | `close`, `volume`, `hl_pct_change`         |
| **Fundamentals** | `(ticker, report_date)` | `ticker`    | `net_income`, `total_assets`, `shares_out` |
| **Macro**        | `date`                  | _None_      | `unemployment_rate`, `cpi_yoy`, `fed_rate` |

### Scraping Logic

- [Top 100 companies](https://companiesmarketcap.com/usa/largest-companies-in-the-usa-by-market-cap/) Gather view requests library then start filling the database table.
  - [x] filled companies table with automatic script.
  - [x] data acquisition for fundamentals and daily prices, yahoo and alpha_vantage-3.
  - [x] data acquisition for macro data, fredapi.

### Clean data

- Before putting recently acquired data in DB it should be verified and cleaned.
  - [x] verify the data.
  - [x] clean the data.
  - [x] load data into db
  - [x] create features
