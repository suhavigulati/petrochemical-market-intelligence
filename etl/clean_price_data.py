import pandas as pd
import os


# ========================================
# FILE PATHS
# ========================================

input_file = "data/price/petrochemical_prices_2021_2023.csv"

output_file = "data/processed/petrochemical_prices_cleaned.csv"


# ========================================
# CREATE OUTPUT FOLDER
# ========================================

os.makedirs("data/processed", exist_ok=True)


# ========================================
# LOAD DATA
# ========================================

print("Loading petrochemical price data...")

df = pd.read_csv(input_file)

print("Raw records:", len(df))


# ========================================
# CHECK DUPLICATES
# ========================================

before_duplicates = len(df)

df = df.drop_duplicates()

after_duplicates = len(df)

print(
    "Duplicates removed:",
    before_duplicates - after_duplicates
)


# ========================================
# MISSING VALUES BEFORE CLEANING
# ========================================

print("\nMissing values before cleaning:")

print(df.isnull().sum())


# ========================================
# CONVERT DATA TYPES
# ========================================

df["year"] = pd.to_numeric(
    df["year"],
    errors="coerce"
)

df["price_usd_per_mt"] = pd.to_numeric(
    df["price_usd_per_mt"],
    errors="coerce"
)


# ========================================
# REMOVE INVALID RECORDS
# ========================================

df = df.dropna(
    subset=[
        "year",
        "product",
        "price_usd_per_mt"
    ]
)


# ========================================
# CONVERT YEAR TO INTEGER
# ========================================

df["year"] = df["year"].astype(int)


# ========================================
# CLEAN PRODUCT NAMES
# ========================================

df["product"] = (
    df["product"]
    .astype(str)
    .str.strip()
    .str.title()
)


# ========================================
# CLEAN REGION
# ========================================

df["price_region"] = (
    df["price_region"]
    .astype(str)
    .str.strip()
)


# ========================================
# CLEAN SOURCE
# ========================================

df["source"] = (
    df["source"]
    .astype(str)
    .str.strip()
)


# ========================================
# SORT DATA
# ========================================

df = df.sort_values(
    by=[
        "year",
        "product"
    ]
)


# ========================================
# RESET INDEX
# ========================================

df = df.reset_index(
    drop=True
)


# ========================================
# SAVE CLEANED DATA
# ========================================

df.to_csv(
    output_file,
    index=False
)


# ========================================
# FINAL SUMMARY
# ========================================

print("\n========================================")
print("PRICE ETL CLEANING COMPLETE")
print("========================================")

print(
    "Final records:",
    len(df)
)

print("\nYears:")

print(
    df["year"]
    .value_counts()
    .sort_index()
)

print("\nProducts:")

print(
    df["product"]
    .value_counts()
)

print("\nPrice range:")

print(
    "Minimum:",
    df["price_usd_per_mt"].min()
)

print(
    "Maximum:",
    df["price_usd_per_mt"].max()
)

print("\nMissing values after cleaning:")

print(
    df.isnull().sum()
)

print("\nFinal columns:")

print(
    df.columns.tolist()
)

print("\nCleaned data saved to:")

print(output_file)