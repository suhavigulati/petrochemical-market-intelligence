import pandas as pd
import os


# ========================================
# FILE PATHS
# ========================================

trade_file = (
    "data/processed/"
    "petrochemical_global_trade_cleaned.csv"
)

price_file = (
    "data/processed/"
    "petrochemical_prices_cleaned.csv"
)

output_file = (
    "data/processed/"
    "petrochemical_market_intelligence.csv"
)


# ========================================
# LOAD DATA
# ========================================

print("Loading trade data...")

trade_df = pd.read_csv(trade_file)

print(
    "Trade records:",
    len(trade_df)
)


print("\nLoading price data...")

price_df = pd.read_csv(price_file)

print(
    "Price records:",
    len(price_df)
)


# ========================================
# DISPLAY PRODUCTS
# ========================================

print("\nTrade products:")

print(
    sorted(
        trade_df["product"].unique()
    )
)

print("\nPrice products:")

print(
    sorted(
        price_df["product"].unique()
    )
)


# ========================================
# SELECT PRICE COLUMNS
# ========================================

price_columns = [
    "year",
    "product",
    "price_usd_per_mt",
    "price_region"
]

price_df = price_df[
    price_columns
]


# ========================================
# MERGE DATA
# ========================================

print("\nCombining trade and price data...")

combined_df = trade_df.merge(
    price_df,
    on=[
        "year",
        "product"
    ],
    how="left"
)


# ========================================
# CHECK PRICE MATCHING
# ========================================

matched_prices = (
    combined_df["price_usd_per_mt"]
    .notna()
    .sum()
)

missing_prices = (
    combined_df["price_usd_per_mt"]
    .isna()
    .sum()
)


print("\n========================================")
print("PRICE MATCHING RESULTS")
print("========================================")

print(
    "Trade records:",
    len(trade_df)
)

print(
    "Records with matched price:",
    matched_prices
)

print(
    "Records without price:",
    missing_prices
)


# ========================================
# CHECK MISSING VALUES
# ========================================

print("\nMissing values in combined dataset:")

print(
    combined_df.isnull().sum()
)


# ========================================
# CREATE PRICE PER KG
# ========================================

combined_df["price_usd_per_kg"] = (
    combined_df["price_usd_per_mt"] / 1000
)


# ========================================
# CALCULATE ESTIMATED MARKET VALUE
# ========================================

combined_df["estimated_market_value"] = (
    combined_df["net_weight"]
    * combined_df["price_usd_per_kg"]
)


# ========================================
# SORT DATA
# ========================================

combined_df = combined_df.sort_values(
    by=[
        "reporter_country",
        "year",
        "product"
    ]
)


# ========================================
# RESET INDEX
# ========================================

combined_df = combined_df.reset_index(
    drop=True
)


# ========================================
# SAVE DATASET
# ========================================

combined_df.to_csv(
    output_file,
    index=False
)


# ========================================
# FINAL SUMMARY
# ========================================

print("\n========================================")
print("MARKET INTELLIGENCE DATASET CREATED")
print("========================================")

print(
    "Final records:",
    len(combined_df)
)

print("\nFinal columns:")

print(
    combined_df.columns.tolist()
)

print("\nProducts:")

print(
    combined_df["product"]
    .value_counts()
)

print("\nCountries:")

print(
    combined_df["reporter_country"]
    .value_counts()
)

print("\nYears:")

print(
    combined_df["year"]
    .value_counts()
    .sort_index()
)

print("\nEstimated market value by country:")

market_value_country = (
    combined_df
    .groupby("reporter_country")[
        "estimated_market_value"
    ]
    .sum()
    .sort_values(
        ascending=False
    )
)

print(
    market_value_country
)

print("\nDataset saved to:")

print(output_file)


# ========================================
# COMPLETE
# ========================================

print("\n========================================")
print("TRADE + PRICE COMBINATION COMPLETE")
print("========================================")