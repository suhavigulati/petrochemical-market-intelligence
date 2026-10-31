import pandas as pd
import os


# ========================================
# FILE PATHS
# ========================================

input_file = "data/raw/petrochemical_global_trade_2021_2023.csv"

output_file = "data/processed/petrochemical_global_trade_cleaned.csv"


# ========================================
# CREATE OUTPUT FOLDER
# ========================================

os.makedirs("data/processed", exist_ok=True)


# ========================================
# LOAD DATA
# ========================================

print("Loading global trade data...")

df = pd.read_csv(input_file)

print("Raw records:", len(df))


# ========================================
# SELECT IMPORTANT COLUMNS
# ========================================

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
    "reporter_country",
    "trade_year"
]

df = df[columns_to_keep]


# ========================================
# RENAME COLUMNS
# ========================================

df = df.rename(columns={
    "period": "year",
    "reporterCode": "reporter_code",
    "partnerCode": "partner_code",
    "cmdCode": "hs_code",
    "netWgt": "net_weight",
    "primaryValue": "trade_value",
    "fobvalue": "export_value"
})


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
# CONVERT NUMERIC COLUMNS
# ========================================

numeric_columns = [
    "year",
    "reporter_code",
    "partner_code",
    "hs_code",
    "net_weight",
    "trade_value",
    "export_value",
    "product_hs_code",
    "trade_year"
]

for column in numeric_columns:

    df[column] = pd.to_numeric(
        df[column],
        errors="coerce"
    )


# ========================================
# HANDLE MISSING NUMERIC VALUES
# ========================================

df["net_weight"] = df["net_weight"].fillna(0)

df["trade_value"] = df["trade_value"].fillna(0)

df["export_value"] = df["export_value"].fillna(0)


# ========================================
# REMOVE INVALID YEARS
# ========================================

df = df.dropna(
    subset=["year"]
)

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
# CLEAN COUNTRY NAMES
# ========================================

df["reporter_country"] = (
    df["reporter_country"]
    .astype(str)
    .str.strip()
)


# ========================================
# SORT DATA
# ========================================

df = df.sort_values(
    by=[
        "reporter_country",
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
print("GLOBAL ETL CLEANING COMPLETE")
print("========================================")

print(
    "Final records:",
    len(df)
)

print("\nCountries:")

print(
    df["reporter_country"]
    .value_counts()
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