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

/Trades

![Test1](https://github.com/praveensingh929/Steeleye/assets/117822190/6d995004-af75-4f27-9986-478a92658142)

/trades?page=2&per_page=20


![test2](https://github.com/praveensingh929/Steeleye/assets/117822190/0323046d-81a1-4368-8247-9142bd34a53c)


/trades?asset_class=Bond&start=2023-06-01&end=2023-12-31&min_price=100.0&max_price=900.0&trade_type=SELL&page=2&per_page=5&sort_by=trade_date_time&reverse_sort=true

![test3](https://github.com/praveensingh929/Steeleye/assets/117822190/ef581a17-8efa-4c38-ad78-f722451ede2f)

/trades?sort_by=trade_id
![test4](https://github.com/praveensingh929/Steeleye/assets/117822190/357e63f8-8b91-403d-9b50-75cf7931ff9e)


  /trades?search=ABC%20Corporation
  ![test5](https://github.com/praveensingh929/Steeleye/assets/117822190/5353f7ef-fe60-4e92-a70e-1bd271738f74)




