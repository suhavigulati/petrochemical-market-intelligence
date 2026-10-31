# Petrochemical Market Intelligence Dashboard

## Project Overview

The Petrochemical Market Intelligence Dashboard is a Python-based data analytics project designed to analyse petrochemical trade and price trends. It provides insights into international trade data, product-wise exports, country-wise performance, and future price predictions.

## Features

* Interactive dashboard using Streamlit.
* Country-wise and product-wise trade analysis.
* Petrochemical export and trade value visualisation.
* Historical price trend analysis.
* Price forecasting using Machine Learning.
* Data cleaning and preprocessing.
* Interactive filters for countries, products, and years.

## Technologies Used

* Python
* Streamlit
* Pandas
* NumPy
* Matplotlib
* Scikit-learn

## Project Structure

```text
petrochemical-market-intelligence/
│
├── dashboard/
│   └── app.py
├── data/
│   ├── raw/
│   ├── processed/
│   └── price/
├── etl/
│   └── analysis/
├── ml/
│   └── price_forecasting.py
├── scraper/
│   ├── price_scraper.py
│   └── trade_scraper.py
├── requirements.txt
└── README.md
```

## Installation

Clone the repository:

```bash
git clone https://github.com/suhavigulati/petrochemical-market-intelligence.git
```

Move into the project directory:

```bash
cd petrochemical-market-intelligence
```

Install the required libraries:

```bash
pip install -r requirements.txt
```

## Run the Dashboard

```bash
streamlit run dashboard/app.py
```

## Machine Learning

The project uses Linear Regression to forecast petrochemical prices based on historical price data.

## Applications

* Petrochemical market analysis.
* International trade monitoring.
* Price trend analysis.
* Market research and forecasting.

## Author

**Suhavi Gulati**

Petrochemical Market Intelligence Project
