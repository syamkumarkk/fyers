# Algo Trading with Fyers API and MongoDB

This repository contains a collection of scripts and notebooks designed to demonstrate algorithmic trading using the Fyers API with Python. It is intended for educational purposes and provides a foundational framework for building your own algorithmic trading strategies. Additionally, this repository integrates MongoDB for persistent storage of trade data, strategy logs, and other relevant metrics.

## Overview

The Fyers API offers a comprehensive interface that allows traders to execute trades, retrieve live market data, manage portfolios, and much more, directly through Python scripts. By leveraging the capabilities of the Fyers API and combining it with MongoDB, this repository showcases various trading strategies, real-time data processing, and the ability to store and retrieve important trading information for analysis and reporting.

## Key Features

- **Real-time Market Data**: Use the Fyers API to fetch live market data for your algorithmic strategies.
- **Trade Execution**: Execute buy and sell orders through the Fyers API based on your trading strategies.
- **MongoDB Integration**: Store and retrieve trade-related data (such as executed orders, historical market data, strategy performance logs) using MongoDB.
- **Educational Resource**: Provides examples and templates for building custom trading strategies and working with the Fyers API.

## Prerequisites

Before you start, ensure the following prerequisites are met:

1. **Fyers Account**: Sign up for a Fyers account [here](https://www.fyers.in/).
2. **Fyers API Token**: You will need an API token from Fyers. Refer to the [Fyers API documentation](https://api.fyers.in/) to obtain it.
3. **Python 3.6 or higher**: Ensure that Python 3.6+ is installed on your system.
4. **MongoDB Setup**: Set up MongoDB to store trade data, performance logs, and other relevant information. You can install MongoDB locally or use a cloud-based solution such as MongoDB Atlas.

## MongoDB Configuration

To store data in MongoDB, you'll need to configure a connection to your MongoDB instance. Below is a basic guide to setting up MongoDB with this repository.

### Step 1: Install MongoDB Python Driver

If you haven't already installed the MongoDB Python driver (`pymongo`), you can install it using `pip`:

```bash
pip install pymongo


### Step 2: Install MongoDB Python Driver

In your Python script, you can configure the MongoDB connection as follows:

```bash
from pymongo import MongoClient

# MongoDB URI
mongo_uri = "mongodb://localhost:27017/"  # Update with your MongoDB connection string

# Connect to MongoDB
client = MongoClient(mongo_uri)

# Select the database
db = client['trading_db']

# Select the collection (table) where data will be stored
trades_collection = db['trades']
logs_collection = db['logs']
```

### Step 2: Install MongoDB Python Driver

Once you have the MongoDB connection set up, you can store trade data. For example, after executing a trade through the Fyers API, you can store the trade details in MongoDB like so:

```bash
trade_data = {
    "symbol": "AAPL",
    "action": "buy",
    "quantity": 10,
    "price": 150.25,
    "timestamp": "2024-11-22T14:45:00",
    "status": "executed"
}

# Insert the trade data into the MongoDB collection
trades_collection.insert_one(trade_data)
```


# Running the Code
Once the configuration is complete, you can run the Python scripts to:

**Execute trades based on your strategies.**
- Retrieve real-time market data.
- Log trade executions and performance metrics to MongoDB.

# Conclusion
This repository demonstrates how to use the Fyers API for algorithmic trading with Python, along with MongoDB for storing and analyzing trade data and logs. It provides a base to create and test your own trading strategies while ensuring persistent storage of relevant information for further analysis.

For further details on the Fyers API, refer to the official Fyers API documentation. 