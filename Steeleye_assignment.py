import datetime as dt
import random
from string import ascii_uppercase
from fastapi import FastAPI, Query
from pydantic import BaseModel, Field
from typing import List, Optional

app = FastAPI()

# Mocked database
db = []


class TradeDetails(BaseModel):
    buySellIndicator: str = Field(description="A value of BUY for buys, SELL for sells.")
    price: float = Field(description="The price of the Trade.")
    quantity: int = Field(description="The amount of units traded.")


class Trade(BaseModel):
    asset_class: Optional[str] = Field(alias="assetClass", default=None,
                                       description="The asset class of the instrument traded. E.g. Bond, Equity, FX...etc")
    counterparty: Optional[str] = Field(default=None,
                                        description="The counterparty the trade was executed with. May not always be available")
    instrument_id: str = Field(alias="instrumentId", description="The ISIN/ID of the instrument traded. E.g. TSLA, AAPL, AMZN...etc")
    instrument_name: str = Field(alias="instrumentName", description="The name of the instrument traded.")
    trade_date_time: dt.datetime = Field(alias="tradeDateTime", description="The date-time the Trade was executed")
    trade_details: TradeDetails = Field(alias="tradeDetails", description="The details of the trade, i.e. price, quantity")
    trade_id: str = Field(alias="tradeId", default=None, description="The unique ID of the trade")
    trader: str = Field(description="The name of the Trader")


@app.get("/trades/{trade_id}")
def get_trade(trade_id: str):
    trade = find_trade_by_id(trade_id)
    if trade is None:
        return {"message": "Trade not found"}
    return trade.dict()


@app.get("/trades")
def get_trades(
    search: Optional[str] = Query(None),
    asset_class: Optional[str] = Query(None),
    start: Optional[str] = Query(None),
    end: Optional[str] = Query(None),
    min_price: Optional[float] = Query(None),
    max_price: Optional[float] = Query(None),
    trade_type: Optional[str] = Query(None),
    page: int = Query(1),
    per_page: int = Query(10),
    sort_by: Optional[str] = Query(None),
    reverse_sort: bool = Query(False)
):
    if min_price is not None:
        min_price = float(min_price)

    if max_price is not None:
        max_price = float(max_price)

    if asset_class == "alltrade":
        # Return all trades
        trades = db
    else:
        trades = filter_trades(asset_class, start, end, min_price, max_price, trade_type)

    # Apply search
    if search:
        trades = search_trades(trades, search)

    # Apply sorting
    if sort_by is not None:
        trades = sorted(trades, key=lambda t: getattr(t, sort_by), reverse=reverse_sort)

    # Apply pagination
    start_index = (page - 1) * per_page
    end_index = start_index + per_page
    paginated_trades = trades[start_index:end_index]

    return [trade.dict() for trade in paginated_trades]


def find_trade_by_id(trade_id: str):
    for trade in db:
        if trade.trade_id == trade_id:
            return trade
    return None


def filter_trades(asset_class: Optional[str] = None, start: Optional[str] = None, end: Optional[str] = None,
                  min_price: Optional[float] = None, max_price: Optional[float] = None,
                  trade_type: Optional[str] = None):
    filtered_trades = db

    if asset_class:
        filtered_trades = [trade for trade in filtered_trades if trade.asset_class == asset_class]

    if start:
        start_date = dt.datetime.strptime(start, "%Y-%m-%d")
        filtered_trades = [trade for trade in filtered_trades if trade.trade_date_time >= start_date]

    if end:
        end_date = dt.datetime.strptime(end, "%Y-%m-%d")
        filtered_trades = [trade for trade in filtered_trades if trade.trade_date_time <= end_date]

    if min_price:
        filtered_trades = [trade for trade in filtered_trades if trade.trade_details.price >= min_price]

    if max_price:
        filtered_trades = [trade for trade in filtered_trades if trade.trade_details.price <= max_price]

    if trade_type:
        filtered_trades = [trade for trade in filtered_trades if trade.trade_details.buySellIndicator == trade_type]

    return filtered_trades


def search_trades(trades: List[Trade], search_query: str):
    search_results = []
    for trade in trades:
        if (
            search_query.lower() in trade.counterparty.lower()
            or search_query.lower() in trade.instrument_id.lower()
            or search_query.lower() in trade.instrument_name.lower()
            or search_query.lower() in trade.trader.lower()
        ):
            search_results.append(trade)
    return search_results


def generate_random_trade():
    asset_classes = ["Equity", "Bond", "FX"]
    counterparty_names = ["ABC Corporation", "XYZ Bank", "DEF Investments"]
    instrument_ids = ["AAPL", "TSLA", "GOOGL", "AMZN"]
    instrument_names = ["Apple Inc.", "Tesla Inc.", "Alphabet Inc.", "Amazon.com Inc."]
    buy_sell_indicators = ["BUY", "SELL"]

    trade_id = str(random.randint(100000, 999999))
    asset_class = random.choice(asset_classes)
    counterparty = random.choice(counterparty_names)
    instrument_id = random.choice(instrument_ids)
    instrument_name = random.choice(instrument_names)
    trade_date_time = generate_random_datetime()  # Generate random trade date-time
    price = round(random.uniform(10.0, 1000.0), 2)
    quantity = random.randint(1, 100)
    buy_sell_indicator = random.choice(buy_sell_indicators)
    trader = ''.join(random.choices(ascii_uppercase, k=5))

    trade_details = TradeDetails(buySellIndicator=buy_sell_indicator, price=price, quantity=quantity)
    trade = Trade(assetClass=asset_class, counterparty=counterparty, instrumentId=instrument_id,
                  instrumentName=instrument_name, tradeDateTime=trade_date_time, tradeDetails=trade_details,
                  tradeId=trade_id, trader=trader)

    return trade


def generate_random_datetime(start_date=dt.datetime(2023, 1, 1), end_date=dt.datetime(2023, 12, 31)):
    time_between_dates = end_date - start_date
    random_number_of_days = random.randrange(time_between_dates.days)
    random_date = start_date + dt.timedelta(days=random_number_of_days)
    random_time = dt.time(hour=random.randint(0, 23), minute=random.randint(0, 59), second=random.randint(0, 59))
    return dt.datetime.combine(random_date, random_time)


# Generate random trades
for _ in range(100):
    random_trade = generate_random_trade()
    db.append(random_trade)

# Run the server
import nest_asyncio
from uvicorn import run

nest_asyncio.apply()
run(app, host="0.0.0.0", port=8000)
