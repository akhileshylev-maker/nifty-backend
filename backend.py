from flask import Flask, jsonify
from kiteconnect import KiteConnect
import os

app = Flask(__name__)

API_KEY = "chd1njoljnzyu2n6"
ACCESS_TOKEN = os.environ.get("ACCESS_TOKEN")   # Set on Render.com

kite = KiteConnect(api_key=API_KEY)
if ACCESS_TOKEN:
    kite.set_access_token(ACCESS_TOKEN)
    print("Kite connected successfully")

@app.route('/market_data')
def market_data():
    if not kite or not ACCESS_TOKEN:
        return jsonify({"error": "Kite not connected"}), 500

    try:
        funds = kite.margins()
        eq = funds['equity']
        live_cash = eq['available']['cash'] + eq['available'].get('collateral', 0)
        display_funds = live_cash if live_cash > 0 else eq['available']['opening_balance']

        watch = [
            "NSEIX:GIFT NIFTY", "NSE:INDIA VIX", "CDS:USDINR26APRFUT",
            "MCX:CRUDEOIL26APRFUT", "MCX:GOLD26APRFUT", "MCX:SILVER26MAYFUT"
        ]
        quotes = kite.quote(watch)

        return jsonify({
            "available_balance": f"₹{display_funds:,.2f}",
            "gift_nifty": quotes.get('NSEIX:GIFT NIFTY', {}).get('last_price', 'N/A'),
            "india_vix": quotes.get('NSE:INDIA VIX', {}).get('last_price', 'N/A'),
            "usdinr": quotes.get('CDS:USDINR26APRFUT', {}).get('last_price', 'N/A'),
            "brent": quotes.get('MCX:CRUDEOIL26APRFUT', {}).get('last_price', 'N/A'),
            "gold": quotes.get('MCX:GOLD26APRFUT', {}).get('last_price', 'N/A'),
            "silver": quotes.get('MCX:SILVER26MAYFUT', {}).get('last_price', 'N/A')
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)