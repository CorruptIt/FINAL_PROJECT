# Market Valuation Model

### Database Schema: src/db_init.py

| Table Name       | Primary Key             | Foreign Key | Key Columns / Features                     |
| :--------------- | :---------------------- | :---------- | :----------------------------------------- |
| **Companies**    | `ticker`                | _None_      | `sector`, `industry_group`                 |
| **Daily Prices** | `(ticker, date)`        | `ticker`    | `close`, `volume`, `hl_pct_change`         |
| **Fundamentals** | `(ticker, report_date)` | `ticker`    | `net_income`, `total_assets`, `shares_out` |
| **Macro**        | `date`                  | _None_      | `unemployment_rate`, `cpi_yoy`, `fed_rate` |

### Scraping Logic

- [Top 100 companies] (<https://companiesmarketcap.com/usa/largest-companies-in-the-usa-by-market-cap/>)
