from flask import Flask, jsonify, request
import yfinance as yf
import numpy as np
import pandas as pd
from prophet import Prophet
from datetime import datetime
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

@app.route("/", methods=['GET'])
def home():
    return 'Welcome Home'

@app.route("/stocks", methods=['POST'])
def get_stocks():
    try:
        data = request.get_json()
        stock_symbol = data['stock']
        stock = yf.Ticker(stock_symbol)
        hist = stock.history(period="6mo")
        hist = pd.DataFrame(hist)
        hist = hist.reset_index()
        hist['Date'] = hist['Date'].dt.date

        today = datetime.today().date()
        today_str = today.strftime('%Y-%m-%d')

        def prophet_formula(data):
            model = Prophet()
            model.fit(data)
            last_date = data['ds'].max()
            future_dates = pd.bdate_range(start=last_date, periods=30)
            future = pd.DataFrame(future_dates, columns=['ds'])
            Prediction = model.predict(future)
            return Prediction

        openData = pd.DataFrame({"ds": hist['Date'], 'y': hist['Open']})
        HighData = pd.DataFrame({"ds": hist['Date'], 'y': hist['High']})
        LowData = pd.DataFrame({"ds": hist['Date'], 'y': hist['Low']})
        CloseData = pd.DataFrame({"ds": hist['Date'], 'y': hist['Close']})

        opening = prophet_formula(openData)
        high = prophet_formula(HighData)
        low = prophet_formula(LowData)
        close = prophet_formula(CloseData)

        finalResults = pd.DataFrame({
            "Date": opening['ds'],
            "Open": opening['yhat'].round(2),
            "High": high['yhat'].round(2),
            "Low": low['yhat'].round(2),
            "Close": close['yhat'].round(2),
        })

        final = finalResults[finalResults['Date'] > today_str]
        final_json = final.to_json(orient='records')

        analysts = stock.analyst_price_targets
        earnings = stock.earnings_dates.reset_index()
        earnings['Earnings Date'] = pd.to_datetime(earnings['Earnings Date']).dt.date
        earningsDates = earnings[earnings['Earnings Date'] > today]
        nextEarnings = earningsDates[['Earnings Date', 'EPS Estimate']].dropna().to_json(orient='records')

        news = stock.news
        recommendations = stock.recommendations_summary.to_json(orient='records')
        insiders = stock.insider_roster_holders.to_json(orient='records')
        info = stock.info

        # Return all the data as a JSON object
        return jsonify({
            "predictions": final_json,
            "analysts": analysts,
            "nextEarnings": nextEarnings,
            "news": news,
            "recommendations": recommendations,
            "insiders": insiders,
            "info": info
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=os.getenv('FLASK_ENV') != 'production')
