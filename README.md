# Steeleye Assignment

An API for managing trades, providing functionalities to retrieve trades, search for trades, apply advanced filters, and perform pagination and sorting.

## Usage

Retrieve a single trade by ID: GET `/trades/{trade_id}`
- Search for trades: GET `/trades?search={search_query}`
- Apply advanced filters: GET `/trades?asset_class={asset_class}&start={start_date}&end={end_date}&min_price={min_price}&max_price={max_price}&trade_type={trade_type}`
- Pagination and sorting: GET `/trades?page={page_number}&per_page={trades_per_page}&sort_by={field}&reverse_sort={true/false}`

## Data Generation

A data generation function is available to facilitate testing. It generates random trade data, allowing for different scenarios and edge cases to be tested thoroughly.
## Screenshots


