import yfinance as yf
from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime
from database import Database

def get_stock_data(ticker):
    try:
        stock = yf.Ticker(ticker)
        stock_data = stock.history(period='1d', interval='15m')
        return stock_data
    except Exception as e:
        print(f"Error retrieving stock data: {e}")
        return None

def store_data():
    try:
        ticker = "ICICIBANK.NS"
        current_time = datetime.now().time()
        if current_time >= datetime.strptime('11:15:00', '%H:%M:%S').time() and current_time <= datetime.strptime('14:15:00', '%H:%M:%S').time():
            stock_data = get_stock_data(ticker)

            if stock_data is not None and not stock_data.empty:
                data_to_store = {
                    'timestamp': datetime.now(),
                    'ticker': ticker,
                    'data': stock_data.to_dict(orient='records')
                }

                db.insert_data('stock_data_collection', data_to_store)
                print(f"Data stored at {datetime.now()}")
            else:
                print("No stock data available or empty")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    db = Database()
    scheduler = BlockingScheduler()
    scheduler.add_job(store_data, 'interval', minutes=15)
    scheduler.start()

    try:
        print("Press Ctrl + C to exit")
        while True:
            pass
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
