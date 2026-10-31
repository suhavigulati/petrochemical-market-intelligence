import pandas as pd
import os

# --------------------------------------------------
# FILE PATHS
# --------------------------------------------------

input_file = "data/raw/petrochemical_trade_2023.csv"
output_file = "data/processed/petrochemical_trade_cleaned.csv"

# --------------------------------------------------
# CREATE PROCESSED FOLDER
# --------------------------------------------------

os.makedirs("data/processed", exist_ok=True)

# --------------------------------------------------
# LOAD RAW DATA
# --------------------------------------------------

print("Loading raw data...")

df = pd.read_csv(input_file)

print("Raw records:", len(df))

# --------------------------------------------------
# SELECT IMPORTANT COLUMNS
# --------------------------------------------------

columns_to_keep = [
    "period",
    "reporterCode",
    "partnerCode",
    "cmdCode",
    "netWgt",
    "primaryValue",
    "fobvalue",
    "product",
    "product_hs_code",
    "reporter_country"
]

df = df[columns_to_keep]

# --------------------------------------------------
# RENAME COLUMNS
# --------------------------------------------------

df = df.rename(columns={
    "period": "year",
    "reporterCode": "reporter_code",
    "partnerCode": "partner_code",
    "cmdCode": "hs_code",
    "netWgt": "net_weight",
    "primaryValue": "trade_value",
    "fobvalue": "export_value"
})

# --------------------------------------------------
# REMOVE DUPLICATES
# --------------------------------------------------

before_duplicates = len(df)

df = df.drop_duplicates()

after_duplicates = len(df)

print("Duplicates removed:",
      before_duplicates - after_duplicates)

# --------------------------------------------------
# HANDLE MISSING VALUES
# --------------------------------------------------

print("\nMissing values before cleaning:")

print(df.isnull().sum())

# Replace missing numerical values with 0
numeric_columns = [
    "net_weight",
    "trade_value",
    "export_value"
]

for column in numeric_columns:
    df[column] = df[column].fillna(0)

# --------------------------------------------------
# DATA TYPES
# --------------------------------------------------

df["year"] = pd.to_numeric(
    df["year"],
    errors="coerce"
)

df["net_weight"] = pd.to_numeric(
    df["net_weight"],
    errors="coerce"
)

df["trade_value"] = pd.to_numeric(
    df["trade_value"],
    errors="coerce"
)

df["export_value"] = pd.to_numeric(
    df["export_value"],
    errors="coerce"
)

# --------------------------------------------------
# REMOVE INVALID YEARS
# --------------------------------------------------

df = df.dropna(subset=["year"])

df["year"] = df["year"].astype(int)

# --------------------------------------------------
# STANDARDIZE PRODUCT NAMES
# --------------------------------------------------

df["product"] = df["product"].str.strip().str.title()

# --------------------------------------------------
# SORT DATA
# --------------------------------------------------

df = df.sort_values(
    by=["product", "year"]
)

# --------------------------------------------------
# RESET INDEX
# --------------------------------------------------

df = df.reset_index(drop=True)

# --------------------------------------------------
# SAVE CLEAN DATA
# --------------------------------------------------

df.to_csv(
    output_file,
    index=False
)

# --------------------------------------------------
# FINAL REPORT
# --------------------------------------------------

print("\n========================================")
print("ETL CLEANING COMPLETE")
print("========================================")

print("Final records:", len(df))

print("\nProducts:")

print(df["product"].value_counts())

print("\nFinal columns:")

print(df.columns.tolist())

print("\nCleaned data saved to:")

print(output_file)