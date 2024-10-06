# Stock Prediction and Company Info API

This project is a Flask-based web application that predicts stock prices using historical data from the Yahoo Finance API and performs forecasting using the Prophet machine learning library. The application also retrieves company information, news, insider trading, analyst recommendations, and the next earnings date for a given stock symbol.

## Features

- **Stock Price Prediction:** Provides 30-day stock price predictions using Open, High, Low, and Close data.
- **Company Information:** Retrieves basic company information like name, CEO, headquarters, etc.
- **Stock News:** Displays the latest news related to the stock.
- **Analyst Recommendations:** Shows analyst price targets and ratings (buy, hold, sell).
- **Insider Trading:** Displays insider trading data for the company.
- **Next Earnings Date:** Fetches the next earnings date for the company.
  
## Tech Stack

- **Flask:** Python web framework to handle HTTP requests and build APIs.
- **yFinance:** Used to fetch historical stock data and company info from Yahoo Finance.
- **Prophet:** A forecasting tool to predict stock prices based on historical data.
- **Pandas & NumPy:** Used for data manipulation and calculations.
- **Flask-CORS:** To enable Cross-Origin Resource Sharing.
  
## Setup and Installation

### Prerequisites

- Python 3.7+
- pip (Python package installer)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/stock-prediction-api.git
   cd stock-prediction-api
