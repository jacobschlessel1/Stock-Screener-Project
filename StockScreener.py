#!/usr/bin/env python
# coding: utf-8

# In[2]:


import yfinance as yf

import streamlit as st

import pandas as pd
import numpy as np


# In[3]:


import requests
from bs4 import BeautifulSoup

#Scraping the S&P 500 tickers from Wikipedia
url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
response = requests.get(url)

soup = BeautifulSoup(response.content, 'html.parser')

table = soup.find('table', {'class': 'wikitable'})

tickers = []
sectors = []

# Iterate through all rows in the table (skip the header row)
for row in table.find_all('tr')[1:]:
    cells = row.find_all('td')
    
    ticker = cells[0].get_text(strip=True)
    

    sector = cells[2].get_text(strip=True)
    
    tickers.append(ticker)
    sectors.append(sector)

#Changing names of sectors to match how they appear in yfinance
sectors = ['Consumer Cyclical' if sector == 'Consumer Discretionary' else sector for sector in sectors]
sectors = ['Financial Services' if sector == 'Financials' else sector for sector in sectors]
sectors = ['Consumer Cyclical' if sector == 'Materials' else sector for sector in sectors]
sectors = ['Healthcare' if sector == 'Health Care' else sector for sector in sectors]
sectors = ['Consumer Defensive' if sector == 'Consumer Staples' else sector for sector in sectors]
sectors = ['Technology' if sector == 'Information Technology' else sector for sector in sectors]


# In[4]:


#Title and header
st.title('Stock Screener App - Created by Jacob Schlessel')
st.subheader('Welcome to the Stock Screener App. The app is designed to find your ideal stocks within a given sector. To gauge how a stock compares to others in the sector, the app returns the percentile score for a variety of common metrics of evaluation: Market cap, P/E ratio, price increase over the past year, debt-to-equity ratio, and average volume. Please use the dropdown menus below to filter stocks according to your criteria. For low/mid/high options, the percentile threshold is <30th percentile, 30th-70th percentile, and >70th percentile.') 


#Dropdown option for sector
unique_sectors = list(set(sectors))
sector_choice = st.selectbox('Sector:', unique_sectors)
st.write('You selected:', sector_choice)

#Dropdown for market cap
option_range1 = ['show all', 'low', 'mid', 'high']
marketcap_choice = st.selectbox('Market Cap:', option_range1, key='marketcap')
st.write('You selected:', marketcap_choice)

#Dropdown for P/E ratio
option_range2 = ['show all', 'low', 'mid', 'high']
PEratio_choice = st.selectbox('P/E Ratio:', option_range2, key='PEratio')
st.write('You selected:', PEratio_choice)

#Dropdown for price action
options_price_action = ['show all', 'close to 52wk high', 'close to 52wk low']
price_action_choice = st.selectbox('Price Action:', options_price_action)
st.write('You selected:', price_action_choice)

#Dropdown for debt-to-equity ratio
option_range3 = ['show all', 'low', 'mid', 'high']
debtToEquity_choice = st.selectbox('Debt-to-Equity Ratio:', option_range3, key='debtToEquity')
st.write('You selected:', debtToEquity_choice)

#Dropdown for average volume
option_range4 = ['show all', 'low', 'mid', 'high']
avgVolume_choice = st.selectbox('Average Volume:', option_range4, key='avgVolumeChoice')
st.write('You selected:', avgVolume_choice)


# In[1]:


metrics = ["P/E Ratio", "Market Cap", "Debt-to-Equity", "52 Week Change", "Average Volume"]

# Initialize weights dictionary
weights = {}

# Add sliders for each metric
st.header("Customize Metric Weights for Scoring the Stocks:")
st.subheader("Ensure that the sum of weights is 1. Otherwise, the score of each metric will be normalized based on the adjusted sum (displayed below). In addition, if looking for low/mid cap stocks, set the weight of market cap to 0.")

total_weight = 0
for metric in metrics:
    weights[metric] = st.slider(
        f"Weight for {metric}",
        min_value=0.0,
        max_value=1.0,
        value=0.2,  # Default weight
        step=0.01,
    )
    total_weight += weights[metric]

# Normalize weights if needed
if total_weight > 0:
    normalized_weights = {k: v / total_weight for k, v in weights.items()}
else:
    normalized_weights = weights

# Display normalized weights
st.subheader("Normalized Weights")
st.write(normalized_weights)

# Sum of weights
st.write(f"Sum of Weights: {sum(normalized_weights.values()):.2f}")

# Feedback
if round(sum(normalized_weights.values()), 2) != 1.0:
    st.warning("Weights have been normalized to ensure the sum equals 1.")


# In[6]:


tech_stocks = [ticker for ticker, sector in zip(tickers, sectors) if sector == 'Technology']
healthcare_stocks = [ticker for ticker, sector in zip(tickers, sectors) if sector == 'Healthcare']
consumerdefensive_stocks = [ticker for ticker, sector in zip(tickers, sectors) if sector == 'Consumer Defensive']
consumercyclical_stocks = [ticker for ticker, sector in zip(tickers, sectors) if sector == 'Consumer Cyclical']
financialservices_stocks = [ticker for ticker, sector in zip(tickers, sectors) if sector == 'Financial Services']
industrials_stocks = [ticker for ticker, sector in zip(tickers, sectors) if sector == 'Industrials']
realestate_stocks = [ticker for ticker, sector in zip(tickers, sectors) if sector == 'Real Estate']
energy_stocks = [ticker for ticker, sector in zip(tickers, sectors) if sector == 'Energy']
communicationservices_stocks = [ticker for ticker, sector in zip(tickers, sectors) if sector == 'Communication Services']
utilities_stocks = [ticker for ticker, sector in zip(tickers, sectors) if sector == 'Utilities']

@st.cache_data
def get_technology_stocks_metrics():
    data = {}
    for stock in tech_stocks:
        # Fetch the stock data using yfinance's Ticker object
        ticker = yf.Ticker(stock)
        info = ticker.info
        
        # Extract the required metrics
        stock_data = {
            'P/E Ratio': info.get('trailingPE', 'N/A'),
            'Market Cap': info.get('marketCap', 'N/A'),
            '52 Week Change': info.get('52WeekChange', 'N/A'),
            'Debt-to-Equity': info.get('debtToEquity', 'N/A'),
            'Average Volume': info.get('averageVolume', 'N/A')
        }
        
        # Store the data for this stock
        data[stock] = stock_data
    return data

def get_healthcare_stocks_metrics():
    data = {}
    for stock in healthcare_stocks:
        # Fetch the stock data using yfinance's Ticker object
        ticker = yf.Ticker(stock)
        info = ticker.info
        
        # Extract the required metrics
        stock_data = {
            'P/E Ratio': info.get('trailingPE', 'N/A'),
            'Market Cap': info.get('marketCap', 'N/A'),
            '52 Week Change': info.get('52WeekChange', 'N/A'),
            'Debt-to-Equity': info.get('debtToEquity', 'N/A'),
            'Average Volume': info.get('averageVolume', 'N/A')
        }
        
        # Store the data for this stock
        data[stock] = stock_data
    return data

def get_consumerdefensive_stocks_metrics():
    data = {}
    for stock in consumerdefensive_stocks:
        # Fetch the stock data using yfinance's Ticker object
        ticker = yf.Ticker(stock)
        info = ticker.info
        
        # Extract the required metrics
        stock_data = {
            'P/E Ratio': info.get('trailingPE', 'N/A'),
            'Market Cap': info.get('marketCap', 'N/A'),
            '52 Week Change': info.get('52WeekChange', 'N/A'),
            'Debt-to-Equity': info.get('debtToEquity', 'N/A'),
            'Average Volume': info.get('averageVolume', 'N/A')
        }
        
        # Store the data for this stock
        data[stock] = stock_data
    return data

def get_consumercyclical_stocks_metrics():
    data = {}
    for stock in consumercyclical_stocks:
        # Fetch the stock data using yfinance's Ticker object
        ticker = yf.Ticker(stock)
        info = ticker.info
        
        # Extract the required metrics
        stock_data = {
            'P/E Ratio': info.get('trailingPE', 'N/A'),
            'Market Cap': info.get('marketCap', 'N/A'),
            '52 Week Change': info.get('52WeekChange', 'N/A'),
            'Debt-to-Equity': info.get('debtToEquity', 'N/A'),
            'Average Volume': info.get('averageVolume', 'N/A')
        }
        
        # Store the data for this stock
        data[stock] = stock_data
    return data

def get_financialservices_stocks_metrics():
    data = {}
    for stock in financialservices_stocks:
        # Fetch the stock data using yfinance's Ticker object
        ticker = yf.Ticker(stock)
        info = ticker.info
        
        # Extract the required metrics
        stock_data = {
            'P/E Ratio': info.get('trailingPE', 'N/A'),
            'Market Cap': info.get('marketCap', 'N/A'),
            '52 Week Change': info.get('52WeekChange', 'N/A'),
            'Debt-to-Equity': info.get('debtToEquity', 'N/A'),
            'Average Volume': info.get('averageVolume', 'N/A')
        }
        
        # Store the data for this stock
        data[stock] = stock_data
    return data

def get_industrials_stocks_metrics():
    data = {}
    for stock in industrials_stocks:
        # Fetch the stock data using yfinance's Ticker object
        ticker = yf.Ticker(stock)
        info = ticker.info
        
        # Extract the required metrics
        stock_data = {
            'P/E Ratio': info.get('trailingPE', 'N/A'),
            'Market Cap': info.get('marketCap', 'N/A'),
            '52 Week Change': info.get('52WeekChange', 'N/A'),
            'Debt-to-Equity': info.get('debtToEquity', 'N/A'),
            'Average Volume': info.get('averageVolume', 'N/A')
        }
        
        # Store the data for this stock
        data[stock] = stock_data
    return data

def get_realestate_stocks_metrics():
    data = {}
    for stock in realestate_stocks:
        # Fetch the stock data using yfinance's Ticker object
        ticker = yf.Ticker(stock)
        info = ticker.info
        
        # Extract the required metrics
        stock_data = {
            'P/E Ratio': info.get('trailingPE', 'N/A'),
            'Market Cap': info.get('marketCap', 'N/A'),
            '52 Week Change': info.get('52WeekChange', 'N/A'),
            'Debt-to-Equity': info.get('debtToEquity', 'N/A'),
            'Average Volume': info.get('averageVolume', 'N/A')
        }
        
        # Store the data for this stock
        data[stock] = stock_data
    return data

def get_energy_stocks_metrics():
    data = {}
    for stock in energy_stocks:
        # Fetch the stock data using yfinance's Ticker object
        ticker = yf.Ticker(stock)
        info = ticker.info
        
        # Extract the required metrics
        stock_data = {
            'P/E Ratio': info.get('trailingPE', 'N/A'),
            'Market Cap': info.get('marketCap', 'N/A'),
            '52 Week Change': info.get('52WeekChange', 'N/A'),
            'Debt-to-Equity': info.get('debtToEquity', 'N/A'),
            'Average Volume': info.get('averageVolume', 'N/A')
        }
        
        # Store the data for this stock
        data[stock] = stock_data
    return data

def get_communicationservices_stocks_metrics():
    data = {}
    for stock in communicationservices_stocks:
        # Fetch the stock data using yfinance's Ticker object
        ticker = yf.Ticker(stock)
        info = ticker.info
        
        # Extract the required metrics
        stock_data = {
            'P/E Ratio': info.get('trailingPE', 'N/A'),
            'Market Cap': info.get('marketCap', 'N/A'),
            '52 Week Change': info.get('52WeekChange', 'N/A'),
            'Debt-to-Equity': info.get('debtToEquity', 'N/A'),
            'Average Volume': info.get('averageVolume', 'N/A')
        }
        
        # Store the data for this stock
        data[stock] = stock_data
    return data

def get_utilities_stocks_metrics():
    data = {}
    for stock in utilities_stocks:
        # Fetch the stock data using yfinance's Ticker object
        ticker = yf.Ticker(stock)
        info = ticker.info
        
        # Extract the required metrics
        stock_data = {
            'P/E Ratio': info.get('trailingPE', 'N/A'),
            'Market Cap': info.get('marketCap', 'N/A'),
            '52 Week Change': info.get('52WeekChange', 'N/A'),
            'Debt-to-Equity': info.get('debtToEquity', 'N/A'),
            'Average Volume': info.get('averageVolume', 'N/A')
        }
        
        # Store the data for this stock
        data[stock] = stock_data
    return data


# In[7]:


from scipy.stats import percentileofscore

if sector_choice == 'Technology':
    # Get and display cached stock metrics for the technology sector
    st.write(f"Showing financial metrics for the Technology sector:")
    
    # Fetch cached data for technology stocks
    technology_data = get_technology_stocks_metrics()

    # Store values in dataframe
    df = pd.DataFrame.from_dict(technology_data, orient="index")

    # Convert all columns to numeric, replacing invalid entries with NaN
    for col in df.columns:
        df[col] = pd.to_numeric(df[col], errors='coerce')
        
    # Replace NaN in numeric columns with the column mean
    numeric_cols = df.select_dtypes(include=['number']).columns
    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())

    # Calculate and display percentile ranks
    percentile_ranks_technology = pd.DataFrame(index=df.index)
    for metric in df.columns:
        df[metric] = pd.to_numeric(df[metric], errors='coerce')
        percentile_ranks_technology[metric] = df[metric].apply(lambda x: percentileofscore(df[metric], x, kind='rank'))


    final_df = percentile_ranks_technology.copy()
    
    if marketcap_choice == 'show all':
        pass
    elif marketcap_choice == 'low':
        final_df = final_df[final_df['Market Cap'] < 30]
    elif marketcap_choice == 'mid':
        final_df = final_df[(final_df["Market Cap"] >= 30) & (final_df["Market Cap"] <= 70)]
    elif marketcap_choice == 'high':
        final_df = final_df[final_df['Market Cap'] > 70]

    if PEratio_choice == 'show all':
        pass
    elif PEratio_choice == 'low':
        final_df = final_df[final_df['P/E Ratio'] < 30]
    elif PEratio_choice == 'mid':
        final_df = final_df[(final_df["P/E Ratio"] >= 30) & (final_df["P/E Ratio"] <= 70)]
    elif PEratio_choice == 'high':
        final_df = final_df[final_df['P/E Ratio'] > 70]

    if price_action_choice == 'show all':
        pass
    elif price_action_choice == 'close to 52wk high':
        final_df = final_df[final_df['52 Week Change'] > 70]
    elif price_action_choice == 'close to 52wk low':    
        final_df = final_df[final_df['52 Week Change'] < 30]

    if debtToEquity_choice == 'show all':
        pass
    elif debtToEquity_choice == 'low':
        final_df = final_df[final_df['Debt-to-Equity'] < 30]
    elif debtToEquity_choice == 'mid':
        final_df = final_df[(final_df["Debt-to-Equity"] >= 30) & (final_df["Debt-to-Equity"] <= 70)]
    elif debtToEquity_choice == 'high':
        final_df = final_df[final_df['Debt-to-Equity'] > 70]


    if avgVolume_choice == 'show all':
        pass
    elif avgVolume_choice == 'low':
        final_df = final_df[final_df['Average Volume'] < 30]
    elif avgVolume_choice == 'mid':
        final_df = final_df[(final_df["Average Volume"] >= 30) & (final_df["Average Volume"] <= 70)]
    elif avgVolume_choice == 'high':
        final_df = final_df[final_df['Average Volume'] > 70]

    #Calculate custom score based on weights of each criteria
    final_df["Score"] = final_df.apply(lambda row: sum(row[metric] * weights[metric] for metric in weights), axis=1)
    
    #print sorted results
    sorted_df = final_df.sort_values(by="Score", ascending=False)
    st.subheader(f"Filtered Stocks: By Percentile")
    st.write(sorted_df)






elif sector_choice == 'Healthcare':
    
    # Fetch cached data for technology stocks
    healthcare_data = get_healthcare_stocks_metrics()

# Get and display cached stock metrics for the technology sector
    st.write(f"Showing financial metrics for the Healthcare sector:")
    


    # Store values in dataframe
    df = pd.DataFrame.from_dict(healthcare_data, orient="index")

    # Convert all columns to numeric, replacing invalid entries with NaN
    for col in df.columns:
        df[col] = pd.to_numeric(df[col], errors='coerce')
        
    # Replace NaN in numeric columns with the column mean
    numeric_cols = df.select_dtypes(include=['number']).columns
    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())

    # Calculate and display percentile ranks
    percentile_ranks_healthcare = pd.DataFrame(index=df.index)
    for metric in df.columns:
        df[metric] = pd.to_numeric(df[metric], errors='coerce')
        percentile_ranks_healthcare[metric] = df[metric].apply(lambda x: percentileofscore(df[metric], x, kind='rank'))


    final_df = percentile_ranks_healthcare.copy()
    
    if marketcap_choice == 'show all':
        pass
    elif marketcap_choice == 'low':
        final_df = final_df[final_df['Market Cap'] < 30]
    elif marketcap_choice == 'mid':
        final_df = final_df[(final_df["Market Cap"] >= 30) & (final_df["Market Cap"] <= 70)]
    elif marketcap_choice == 'high':
        final_df = final_df[final_df['Market Cap'] > 70]

    if PEratio_choice == 'show all':
        pass
    elif PEratio_choice == 'low':
        final_df = final_df[final_df['P/E Ratio'] < 30]
    elif PEratio_choice == 'mid':
        final_df = final_df[(final_df["P/E Ratio"] >= 30) & (final_df["P/E Ratio"] <= 70)]
    elif PEratio_choice == 'high':
        final_df = final_df[final_df['P/E Ratio'] > 70]

    if price_action_choice == 'show all':
        pass
    elif price_action_choice == 'close to 52wk high':
        final_df = final_df[final_df['52 Week Change'] > 70]
    elif price_action_choice == 'close to 52wk low':    
        final_df = final_df[final_df['52 Week Change'] < 30]

    if debtToEquity_choice == 'show all':
        pass
    elif debtToEquity_choice == 'low':
        final_df = final_df[final_df['Debt-to-Equity'] < 30]
    elif debtToEquity_choice == 'mid':
        final_df = final_df[(final_df["Debt-to-Equity"] >= 30) & (final_df["Debt-to-Equity"] <= 70)]
    elif debtToEquity_choice == 'high':
        final_df = final_df[final_df['Debt-to-Equity'] > 70]


    if avgVolume_choice == 'show all':
        pass
    elif avgVolume_choice == 'low':
        final_df = final_df[final_df['Average Volume'] < 30]
    elif avgVolume_choice == 'mid':
        final_df = final_df[(final_df["Average Volume"] >= 30) & (final_df["Average Volume"] <= 70)]
    elif avgVolume_choice == 'high':
        final_df = final_df[final_df['Average Volume'] > 70]

    #Calculate custom score based on weights of each criteria
    final_df["Score"] = final_df.apply(lambda row: sum(row[metric] * weights[metric] for metric in weights), axis=1)
    
    #print sorted results
    sorted_df = final_df.sort_values(by="Score", ascending=False)
    st.subheader(f"Filtered Stocks: By Percentile")
    st.write(sorted_df)


elif sector_choice == 'Consumer Defensive':
    
    # Fetch cached data for technology stocks
    consumerdefensive_data = get_consumerdefensive_stocks_metrics()


# Get and display cached stock metrics for the consumer defensive sector
    st.write(f"Showing financial metrics for the Consumer Defensive sector:")
    
    # Store values in dataframe
    df = pd.DataFrame.from_dict(consumerdefensive_data, orient="index")

    # Convert all columns to numeric, replacing invalid entries with NaN
    for col in df.columns:
        df[col] = pd.to_numeric(df[col], errors='coerce')
        
    # Replace NaN in numeric columns with the column mean
    numeric_cols = df.select_dtypes(include=['number']).columns
    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())

    # Calculate and display percentile ranks
    percentile_ranks_CD = pd.DataFrame(index=df.index)
    for metric in df.columns:
        df[metric] = pd.to_numeric(df[metric], errors='coerce')
        percentile_ranks_CD[metric] = df[metric].apply(lambda x: percentileofscore(df[metric], x, kind='rank'))


    final_df = percentile_ranks_CD.copy()
    
    if marketcap_choice == 'show all':
        pass
    elif marketcap_choice == 'low':
        final_df = final_df[final_df['Market Cap'] < 30]
    elif marketcap_choice == 'mid':
        final_df = final_df[(final_df["Market Cap"] >= 30) & (final_df["Market Cap"] <= 70)]
    elif marketcap_choice == 'high':
        final_df = final_df[final_df['Market Cap'] > 70]

    if PEratio_choice == 'show all':
        pass
    elif PEratio_choice == 'low':
        final_df = final_df[final_df['P/E Ratio'] < 30]
    elif PEratio_choice == 'mid':
        final_df = final_df[(final_df["P/E Ratio"] >= 30) & (final_df["P/E Ratio"] <= 70)]
    elif PEratio_choice == 'high':
        final_df = final_df[final_df['P/E Ratio'] > 70]

    if price_action_choice == 'show all':
        pass
    elif price_action_choice == 'close to 52wk high':
        final_df = final_df[final_df['52 Week Change'] > 70]
    elif price_action_choice == 'close to 52wk low':    
        final_df = final_df[final_df['52 Week Change'] < 30]

    if debtToEquity_choice == 'show all':
        pass
    elif debtToEquity_choice == 'low':
        final_df = final_df[final_df['Debt-to-Equity'] < 30]
    elif debtToEquity_choice == 'mid':
        final_df = final_df[(final_df["Debt-to-Equity"] >= 30) & (final_df["Debt-to-Equity"] <= 70)]
    elif debtToEquity_choice == 'high':
        final_df = final_df[final_df['Debt-to-Equity'] > 70]


    if avgVolume_choice == 'show all':
        pass
    elif avgVolume_choice == 'low':
        final_df = final_df[final_df['Average Volume'] < 30]
    elif avgVolume_choice == 'mid':
        final_df = final_df[(final_df["Average Volume"] >= 30) & (final_df["Average Volume"] <= 70)]
    elif avgVolume_choice == 'high':
        final_df = final_df[final_df['Average Volume'] > 70]

    #Calculate custom score based on weights of each criteria
    final_df["Score"] = final_df.apply(lambda row: sum(row[metric] * weights[metric] for metric in weights), axis=1)
    
    #print sorted results
    sorted_df = final_df.sort_values(by="Score", ascending=False)
    st.subheader(f"Filtered Stocks: By Percentile")
    st.write(sorted_df)



elif sector_choice == 'Consumer Cyclical':
    #Fetch cached data for consumer cyclical stocks
    consumercyclical_data = get_consumercyclical_stocks_metrics()


# Get and display cached stock metrics for the consumer defensive sector
    st.write(f"Showing financial metrics for the Consumer Cyclical sector:")
    
    # Store values in dataframe
    df = pd.DataFrame.from_dict(consumercyclical_data, orient="index")

    # Convert all columns to numeric, replacing invalid entries with NaN
    for col in df.columns:
        df[col] = pd.to_numeric(df[col], errors='coerce')
        
    # Replace NaN in numeric columns with the column mean
    numeric_cols = df.select_dtypes(include=['number']).columns
    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())

    # Calculate and display percentile ranks
    percentile_ranks_CC = pd.DataFrame(index=df.index)
    for metric in df.columns:
        df[metric] = pd.to_numeric(df[metric], errors='coerce')
        percentile_ranks_CC[metric] = df[metric].apply(lambda x: percentileofscore(df[metric], x, kind='rank'))


    final_df = percentile_ranks_CC.copy()
    
    if marketcap_choice == 'show all':
        pass
    elif marketcap_choice == 'low':
        final_df = final_df[final_df['Market Cap'] < 30]
    elif marketcap_choice == 'mid':
        final_df = final_df[(final_df["Market Cap"] >= 30) & (final_df["Market Cap"] <= 70)]
    elif marketcap_choice == 'high':
        final_df = final_df[final_df['Market Cap'] > 70]

    if PEratio_choice == 'show all':
        pass
    elif PEratio_choice == 'low':
        final_df = final_df[final_df['P/E Ratio'] < 30]
    elif PEratio_choice == 'mid':
        final_df = final_df[(final_df["P/E Ratio"] >= 30) & (final_df["P/E Ratio"] <= 70)]
    elif PEratio_choice == 'high':
        final_df = final_df[final_df['P/E Ratio'] > 70]

    if price_action_choice == 'show all':
        pass
    elif price_action_choice == 'close to 52wk high':
        final_df = final_df[final_df['52 Week Change'] > 70]
    elif price_action_choice == 'close to 52wk low':    
        final_df = final_df[final_df['52 Week Change'] < 30]

    if debtToEquity_choice == 'show all':
        pass
    elif debtToEquity_choice == 'low':
        final_df = final_df[final_df['Debt-to-Equity'] < 30]
    elif debtToEquity_choice == 'mid':
        final_df = final_df[(final_df["Debt-to-Equity"] >= 30) & (final_df["Debt-to-Equity"] <= 70)]
    elif debtToEquity_choice == 'high':
        final_df = final_df[final_df['Debt-to-Equity'] > 70]


    if avgVolume_choice == 'show all':
        pass
    elif avgVolume_choice == 'low':
        final_df = final_df[final_df['Average Volume'] < 30]
    elif avgVolume_choice == 'mid':
        final_df = final_df[(final_df["Average Volume"] >= 30) & (final_df["Average Volume"] <= 70)]
    elif avgVolume_choice == 'high':
        final_df = final_df[final_df['Average Volume'] > 70]

    #Calculate custom score based on weights of each criteria
    final_df["Score"] = final_df.apply(lambda row: sum(row[metric] * weights[metric] for metric in weights), axis=1)
    
    #print sorted results
    sorted_df = final_df.sort_values(by="Score", ascending=False)
    st.subheader(f"Filtered Stocks: By Percentile")
    st.write(sorted_df)




elif sector_choice == 'Financial Services':
    
    financialservices_data = get_financialservices_stocks_metrics()

# Get and display cached stock metrics for the Financial Services sector
    st.write(f"Showing financial metrics for the Financial Services sector:")
    
    # Store values in dataframe
    df = pd.DataFrame.from_dict(financialservices_data, orient="index")

    # Convert all columns to numeric, replacing invalid entries with NaN
    for col in df.columns:
        df[col] = pd.to_numeric(df[col], errors='coerce')
        
    # Replace NaN in numeric columns with the column mean
    numeric_cols = df.select_dtypes(include=['number']).columns
    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())

    # Calculate and display percentile ranks
    percentile_ranks_FS = pd.DataFrame(index=df.index)
    for metric in df.columns:
        df[metric] = pd.to_numeric(df[metric], errors='coerce')
        percentile_ranks_FS[metric] = df[metric].apply(lambda x: percentileofscore(df[metric], x, kind='rank'))


    final_df = percentile_ranks_FS.copy()
    
    if marketcap_choice == 'show all':
        pass
    elif marketcap_choice == 'low':
        final_df = final_df[final_df['Market Cap'] < 30]
    elif marketcap_choice == 'mid':
        final_df = final_df[(final_df["Market Cap"] >= 30) & (final_df["Market Cap"] <= 70)]
    elif marketcap_choice == 'high':
        final_df = final_df[final_df['Market Cap'] > 70]

    if PEratio_choice == 'show all':
        pass
    elif PEratio_choice == 'low':
        final_df = final_df[final_df['P/E Ratio'] < 30]
    elif PEratio_choice == 'mid':
        final_df = final_df[(final_df["P/E Ratio"] >= 30) & (final_df["P/E Ratio"] <= 70)]
    elif PEratio_choice == 'high':
        final_df = final_df[final_df['P/E Ratio'] > 70]

    if price_action_choice == 'show all':
        pass
    elif price_action_choice == 'close to 52wk high':
        final_df = final_df[final_df['52 Week Change'] > 70]
    elif price_action_choice == 'close to 52wk low':    
        final_df = final_df[final_df['52 Week Change'] < 30]

    if debtToEquity_choice == 'show all':
        pass
    elif debtToEquity_choice == 'low':
        final_df = final_df[final_df['Debt-to-Equity'] < 30]
    elif debtToEquity_choice == 'mid':
        final_df = final_df[(final_df["Debt-to-Equity"] >= 30) & (final_df["Debt-to-Equity"] <= 70)]
    elif debtToEquity_choice == 'high':
        final_df = final_df[final_df['Debt-to-Equity'] > 70]


    if avgVolume_choice == 'show all':
        pass
    elif avgVolume_choice == 'low':
        final_df = final_df[final_df['Average Volume'] < 30]
    elif avgVolume_choice == 'mid':
        final_df = final_df[(final_df["Average Volume"] >= 30) & (final_df["Average Volume"] <= 70)]
    elif avgVolume_choice == 'high':
        final_df = final_df[final_df['Average Volume'] > 70]

    #Calculate custom score based on weights of each criteria
    final_df["Score"] = final_df.apply(lambda row: sum(row[metric] * weights[metric] for metric in weights), axis=1)
    
    #print sorted results
    sorted_df = final_df.sort_values(by="Score", ascending=False)
    st.subheader(f"Filtered Stocks: By Percentile")
    st.write(sorted_df)


elif sector_choice == 'Industrials':
    industrials_data = get_industrials_stocks_metrics()

# Get and display cached stock metrics for the Industrials sector
    st.write(f"Showing financial metrics for the Industrials sector:")
    
    # Store values in dataframe
    df = pd.DataFrame.from_dict(industrials_data, orient="index")

    # Convert all columns to numeric, replacing invalid entries with NaN
    for col in df.columns:
        df[col] = pd.to_numeric(df[col], errors='coerce')
        
    # Replace NaN in numeric columns with the column mean
    numeric_cols = df.select_dtypes(include=['number']).columns
    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())

    # Calculate and display percentile ranks
    percentile_ranks_ID = pd.DataFrame(index=df.index)
    for metric in df.columns:
        df[metric] = pd.to_numeric(df[metric], errors='coerce')
        percentile_ranks_ID[metric] = df[metric].apply(lambda x: percentileofscore(df[metric], x, kind='rank'))


    final_df = percentile_ranks_ID.copy()
    
    if marketcap_choice == 'show all':
        pass
    elif marketcap_choice == 'low':
        final_df = final_df[final_df['Market Cap'] < 30]
    elif marketcap_choice == 'mid':
        final_df = final_df[(final_df["Market Cap"] >= 30) & (final_df["Market Cap"] <= 70)]
    elif marketcap_choice == 'high':
        final_df = final_df[final_df['Market Cap'] > 70]

    if PEratio_choice == 'show all':
        pass
    elif PEratio_choice == 'low':
        final_df = final_df[final_df['P/E Ratio'] < 30]
    elif PEratio_choice == 'mid':
        final_df = final_df[(final_df["P/E Ratio"] >= 30) & (final_df["P/E Ratio"] <= 70)]
    elif PEratio_choice == 'high':
        final_df = final_df[final_df['P/E Ratio'] > 70]

    if price_action_choice == 'show all':
        pass
    elif price_action_choice == 'close to 52wk high':
        final_df = final_df[final_df['52 Week Change'] > 70]
    elif price_action_choice == 'close to 52wk low':    
        final_df = final_df[final_df['52 Week Change'] < 30]

    if debtToEquity_choice == 'show all':
        pass
    elif debtToEquity_choice == 'low':
        final_df = final_df[final_df['Debt-to-Equity'] < 30]
    elif debtToEquity_choice == 'mid':
        final_df = final_df[(final_df["Debt-to-Equity"] >= 30) & (final_df["Debt-to-Equity"] <= 70)]
    elif debtToEquity_choice == 'high':
        final_df = final_df[final_df['Debt-to-Equity'] > 70]


    if avgVolume_choice == 'show all':
        pass
    elif avgVolume_choice == 'low':
        final_df = final_df[final_df['Average Volume'] < 30]
    elif avgVolume_choice == 'mid':
        final_df = final_df[(final_df["Average Volume"] >= 30) & (final_df["Average Volume"] <= 70)]
    elif avgVolume_choice == 'high':
        final_df = final_df[final_df['Average Volume'] > 70]

    #Calculate custom score based on weights of each criteria
    final_df["Score"] = final_df.apply(lambda row: sum(row[metric] * weights[metric] for metric in weights), axis=1)
    
    #print sorted results
    sorted_df = final_df.sort_values(by="Score", ascending=False)
    st.subheader(f"Filtered Stocks: By Percentile")
    st.write(sorted_df)


elif sector_choice == 'Real Estate':
    realestate_data = get_realestate_stocks_metrics()


# Get and display cached stock metrics for the real estate sector
    st.write(f"Showing financial metrics for the Real Estate sector:")
    
    # Store values in dataframe
    df = pd.DataFrame.from_dict(realestate_data, orient="index")

    # Convert all columns to numeric, replacing invalid entries with NaN
    for col in df.columns:
        df[col] = pd.to_numeric(df[col], errors='coerce')
        
    # Replace NaN in numeric columns with the column mean
    numeric_cols = df.select_dtypes(include=['number']).columns
    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())

    # Calculate and display percentile ranks
    percentile_ranks_RE = pd.DataFrame(index=df.index)
    for metric in df.columns:
        df[metric] = pd.to_numeric(df[metric], errors='coerce')
        percentile_ranks_RE[metric] = df[metric].apply(lambda x: percentileofscore(df[metric], x, kind='rank'))


    final_df = percentile_ranks_RE.copy()
    
    if marketcap_choice == 'show all':
        pass
    elif marketcap_choice == 'low':
        final_df = final_df[final_df['Market Cap'] < 30]
    elif marketcap_choice == 'mid':
        final_df = final_df[(final_df["Market Cap"] >= 30) & (final_df["Market Cap"] <= 70)]
    elif marketcap_choice == 'high':
        final_df = final_df[final_df['Market Cap'] > 70]

    if PEratio_choice == 'show all':
        pass
    elif PEratio_choice == 'low':
        final_df = final_df[final_df['P/E Ratio'] < 30]
    elif PEratio_choice == 'mid':
        final_df = final_df[(final_df["P/E Ratio"] >= 30) & (final_df["P/E Ratio"] <= 70)]
    elif PEratio_choice == 'high':
        final_df = final_df[final_df['P/E Ratio'] > 70]

    if price_action_choice == 'show all':
        pass
    elif price_action_choice == 'close to 52wk high':
        final_df = final_df[final_df['52 Week Change'] > 70]
    elif price_action_choice == 'close to 52wk low':    
        final_df = final_df[final_df['52 Week Change'] < 30]

    if debtToEquity_choice == 'show all':
        pass
    elif debtToEquity_choice == 'low':
        final_df = final_df[final_df['Debt-to-Equity'] < 30]
    elif debtToEquity_choice == 'mid':
        final_df = final_df[(final_df["Debt-to-Equity"] >= 30) & (final_df["Debt-to-Equity"] <= 70)]
    elif debtToEquity_choice == 'high':
        final_df = final_df[final_df['Debt-to-Equity'] > 70]


    if avgVolume_choice == 'show all':
        pass
    elif avgVolume_choice == 'low':
        final_df = final_df[final_df['Average Volume'] < 30]
    elif avgVolume_choice == 'mid':
        final_df = final_df[(final_df["Average Volume"] >= 30) & (final_df["Average Volume"] <= 70)]
    elif avgVolume_choice == 'high':
        final_df = final_df[final_df['Average Volume'] > 70]

    #Calculate custom score based on weights of each criteria
    final_df["Score"] = final_df.apply(lambda row: sum(row[metric] * weights[metric] for metric in weights), axis=1)
    
    #print sorted results
    sorted_df = final_df.sort_values(by="Score", ascending=False)
    st.subheader(f"Filtered Stocks: By Percentile")
    st.write(sorted_df)


elif sector_choice == 'Energy':
    
    energy_data = get_energy_stocks_metrics()

# Get and display cached stock metrics for the energysector
    st.write(f"Showing financial metrics for the Energy sector:")
    
    # Store values in dataframe
    df = pd.DataFrame.from_dict(energy_data, orient="index")

    # Convert all columns to numeric, replacing invalid entries with NaN
    for col in df.columns:
        df[col] = pd.to_numeric(df[col], errors='coerce')
        
    # Replace NaN in numeric columns with the column mean
    numeric_cols = df.select_dtypes(include=['number']).columns
    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())

    # Calculate and display percentile ranks
    percentile_ranks_energy = pd.DataFrame(index=df.index)
    for metric in df.columns:
        df[metric] = pd.to_numeric(df[metric], errors='coerce')
        percentile_ranks_energy[metric] = df[metric].apply(lambda x: percentileofscore(df[metric], x, kind='rank'))


    final_df = percentile_ranks_energy.copy()
    
    if marketcap_choice == 'show all':
        pass
    elif marketcap_choice == 'low':
        final_df = final_df[final_df['Market Cap'] < 30]
    elif marketcap_choice == 'mid':
        final_df = final_df[(final_df["Market Cap"] >= 30) & (final_df["Market Cap"] <= 70)]
    elif marketcap_choice == 'high':
        final_df = final_df[final_df['Market Cap'] > 70]

    if PEratio_choice == 'show all':
        pass
    elif PEratio_choice == 'low':
        final_df = final_df[final_df['P/E Ratio'] < 30]
    elif PEratio_choice == 'mid':
        final_df = final_df[(final_df["P/E Ratio"] >= 30) & (final_df["P/E Ratio"] <= 70)]
    elif PEratio_choice == 'high':
        final_df = final_df[final_df['P/E Ratio'] > 70]

    if price_action_choice == 'show all':
        pass
    elif price_action_choice == 'close to 52wk high':
        final_df = final_df[final_df['52 Week Change'] > 70]
    elif price_action_choice == 'close to 52wk low':    
        final_df = final_df[final_df['52 Week Change'] < 30]

    if debtToEquity_choice == 'show all':
        pass
    elif debtToEquity_choice == 'low':
        final_df = final_df[final_df['Debt-to-Equity'] < 30]
    elif debtToEquity_choice == 'mid':
        final_df = final_df[(final_df["Debt-to-Equity"] >= 30) & (final_df["Debt-to-Equity"] <= 70)]
    elif debtToEquity_choice == 'high':
        final_df = final_df[final_df['Debt-to-Equity'] > 70]


    if avgVolume_choice == 'show all':
        pass
    elif avgVolume_choice == 'low':
        final_df = final_df[final_df['Average Volume'] < 30]
    elif avgVolume_choice == 'mid':
        final_df = final_df[(final_df["Average Volume"] >= 30) & (final_df["Average Volume"] <= 70)]
    elif avgVolume_choice == 'high':
        final_df = final_df[final_df['Average Volume'] > 70]

    #Calculate custom score based on weights of each criteria
    final_df["Score"] = final_df.apply(lambda row: sum(row[metric] * weights[metric] for metric in weights), axis=1)
    
    #print sorted results
    sorted_df = final_df.sort_values(by="Score", ascending=False)
    st.subheader(f"Filtered Stocks: By Percentile")
    st.write(sorted_df)


elif sector_choice == 'Communication Services':
    communicationservices_data = get_communicationservices_stocks_metrics()

# Get and display cached stock metrics for the communication services sector
    st.write(f"Showing financial metrics for the Communication Services sector:")
    
    # Store values in dataframe
    df = pd.DataFrame.from_dict(communicationservices_data, orient="index")

    # Convert all columns to numeric, replacing invalid entries with NaN
    for col in df.columns:
        df[col] = pd.to_numeric(df[col], errors='coerce')
        
    # Replace NaN in numeric columns with the column mean
    numeric_cols = df.select_dtypes(include=['number']).columns
    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())

    # Calculate and display percentile ranks
    percentile_ranks_CS = pd.DataFrame(index=df.index)
    for metric in df.columns:
        df[metric] = pd.to_numeric(df[metric], errors='coerce')
        percentile_ranks_CS[metric] = df[metric].apply(lambda x: percentileofscore(df[metric], x, kind='rank'))


    final_df = percentile_ranks_CS.copy()
    
    if marketcap_choice == 'show all':
        pass
    elif marketcap_choice == 'low':
        final_df = final_df[final_df['Market Cap'] < 30]
    elif marketcap_choice == 'mid':
        final_df = final_df[(final_df["Market Cap"] >= 30) & (final_df["Market Cap"] <= 70)]
    elif marketcap_choice == 'high':
        final_df = final_df[final_df['Market Cap'] > 70]

    if PEratio_choice == 'show all':
        pass
    elif PEratio_choice == 'low':
        final_df = final_df[final_df['P/E Ratio'] < 30]
    elif PEratio_choice == 'mid':
        final_df = final_df[(final_df["P/E Ratio"] >= 30) & (final_df["P/E Ratio"] <= 70)]
    elif PEratio_choice == 'high':
        final_df = final_df[final_df['P/E Ratio'] > 70]

    if price_action_choice == 'show all':
        pass
    elif price_action_choice == 'close to 52wk high':
        final_df = final_df[final_df['52 Week Change'] > 70]
    elif price_action_choice == 'close to 52wk low':    
        final_df = final_df[final_df['52 Week Change'] < 30]

    if debtToEquity_choice == 'show all':
        pass
    elif debtToEquity_choice == 'low':
        final_df = final_df[final_df['Debt-to-Equity'] < 30]
    elif debtToEquity_choice == 'mid':
        final_df = final_df[(final_df["Debt-to-Equity"] >= 30) & (final_df["Debt-to-Equity"] <= 70)]
    elif debtToEquity_choice == 'high':
        final_df = final_df[final_df['Debt-to-Equity'] > 70]


    if avgVolume_choice == 'show all':
        pass
    elif avgVolume_choice == 'low':
        final_df = final_df[final_df['Average Volume'] < 30]
    elif avgVolume_choice == 'mid':
        final_df = final_df[(final_df["Average Volume"] >= 30) & (final_df["Average Volume"] <= 70)]
    elif avgVolume_choice == 'high':
        final_df = final_df[final_df['Average Volume'] > 70]

    #Calculate custom score based on weights of each criteria
    final_df["Score"] = final_df.apply(lambda row: sum(row[metric] * weights[metric] for metric in weights), axis=1)
    
    #print sorted results
    sorted_df = final_df.sort_values(by="Score", ascending=False)
    st.subheader(f"Filtered Stocks: By Percentile")
    st.write(sorted_df)
    
elif sector_choice == 'Utilities':
    utilities_data = get_utilities_stocks_metrics()

# Get and display cached stock metrics for the utilities sector
    st.write(f"Showing financial metrics for the Utilities sector:")
    
    # Store values in dataframe
    df = pd.DataFrame.from_dict(utilities_data, orient="index")

    # Convert all columns to numeric, replacing invalid entries with NaN
    for col in df.columns:
        df[col] = pd.to_numeric(df[col], errors='coerce')
        
    # Replace NaN in numeric columns with the column mean
    numeric_cols = df.select_dtypes(include=['number']).columns
    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())

    # Calculate and display percentile ranks
    percentile_ranks_U = pd.DataFrame(index=df.index)
    for metric in df.columns:
        df[metric] = pd.to_numeric(df[metric], errors='coerce')
        percentile_ranks_U[metric] = df[metric].apply(lambda x: percentileofscore(df[metric], x, kind='rank'))


    final_df = percentile_ranks_U.copy()
    
    if marketcap_choice == 'show all':
        pass
    elif marketcap_choice == 'low':
        final_df = final_df[final_df['Market Cap'] < 30]
    elif marketcap_choice == 'mid':
        final_df = final_df[(final_df["Market Cap"] >= 30) & (final_df["Market Cap"] <= 70)]
    elif marketcap_choice == 'high':
        final_df = final_df[final_df['Market Cap'] > 70]

    if PEratio_choice == 'show all':
        pass
    elif PEratio_choice == 'low':
        final_df = final_df[final_df['P/E Ratio'] < 30]
    elif PEratio_choice == 'mid':
        final_df = final_df[(final_df["P/E Ratio"] >= 30) & (final_df["P/E Ratio"] <= 70)]
    elif PEratio_choice == 'high':
        final_df = final_df[final_df['P/E Ratio'] > 70]

    if price_action_choice == 'show all':
        pass
    elif price_action_choice == 'close to 52wk high':
        final_df = final_df[final_df['52 Week Change'] > 70]
    elif price_action_choice == 'close to 52wk low':    
        final_df = final_df[final_df['52 Week Change'] < 30]

    if debtToEquity_choice == 'show all':
        pass
    elif debtToEquity_choice == 'low':
        final_df = final_df[final_df['Debt-to-Equity'] < 30]
    elif debtToEquity_choice == 'mid':
        final_df = final_df[(final_df["Debt-to-Equity"] >= 30) & (final_df["Debt-to-Equity"] <= 70)]
    elif debtToEquity_choice == 'high':
        final_df = final_df[final_df['Debt-to-Equity'] > 70]


    if avgVolume_choice == 'show all':
        pass
    elif avgVolume_choice == 'low':
        final_df = final_df[final_df['Average Volume'] < 30]
    elif avgVolume_choice == 'mid':
        final_df = final_df[(final_df["Average Volume"] >= 30) & (final_df["Average Volume"] <= 70)]
    elif avgVolume_choice == 'high':
        final_df = final_df[final_df['Average Volume'] > 70]

    #Calculate custom score based on weights of each criteria
    final_df["Score"] = final_df.apply(lambda row: sum(row[metric] * weights[metric] for metric in weights), axis=1)
    
    #print sorted results
    sorted_df = final_df.sort_values(by="Score", ascending=False)
    st.subheader(f"Filtered Stocks: By Percentile")
    st.write(sorted_df)

