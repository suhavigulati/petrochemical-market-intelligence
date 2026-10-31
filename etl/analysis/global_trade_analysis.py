import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px


# ========================================
# LOAD DATA
# ========================================

input_file = "data/processed/petrochemical_global_trade_cleaned.csv"

df = pd.read_csv(input_file)

print("Global trade data loaded successfully!")
print("Total records:", len(df))


# ========================================
# BASIC INFORMATION
# ========================================

print("\n========================================")
print("DATASET INFORMATION")
print("========================================")

print("\nCountries:")
print(df["reporter_country"].unique())

print("\nYears:")
print(df["year"].unique())

print("\nProducts:")
print(df["product"].unique())

print("\nColumns:")
print(df.columns.tolist())


# ========================================
# RECORD COUNT BY COUNTRY
# ========================================

country_count = (
    df["reporter_country"]
    .value_counts()
)

print("\n========================================")
print("RECORDS BY COUNTRY")
print("========================================")

print(country_count)


# ========================================
# TOTAL EXPORT VALUE BY COUNTRY
# ========================================

country_export_value = (
    df.groupby("reporter_country")["export_value"]
    .sum()
    .sort_values(ascending=False)
)

print("\n========================================")
print("TOTAL EXPORT VALUE BY COUNTRY")
print("========================================")

print(country_export_value)


# ========================================
# TOTAL EXPORT VALUE BY PRODUCT
# ========================================

product_export_value = (
    df.groupby("product")["export_value"]
    .sum()
    .sort_values(ascending=False)
)

print("\n========================================")
print("TOTAL EXPORT VALUE BY PRODUCT")
print("========================================")

print(product_export_value)


# ========================================
# TOTAL EXPORT VALUE BY YEAR
# ========================================

year_export_value = (
    df.groupby("year")["export_value"]
    .sum()
    .sort_index()
)

print("\n========================================")
print("TOTAL EXPORT VALUE BY YEAR")
print("========================================")

print(year_export_value)


# ========================================
# TOTAL NET WEIGHT BY COUNTRY
# ========================================

country_net_weight = (
    df.groupby("reporter_country")["net_weight"]
    .sum()
    .sort_values(ascending=False)
)

print("\n========================================")
print("TOTAL NET WEIGHT BY COUNTRY")
print("========================================")

print(country_net_weight)


# ========================================
# 1. EXPORT VALUE BY COUNTRY
# ========================================

plt.figure(figsize=(10, 6))

sns.barplot(
    x=country_export_value.index,
    y=country_export_value.values
)

plt.title("Petrochemical Export Value by Country")
plt.xlabel("Country")
plt.ylabel("Export Value")

plt.xticks(rotation=45)
plt.tight_layout()

plt.show()


# ========================================
# 2. EXPORT VALUE BY PRODUCT
# ========================================

plt.figure(figsize=(10, 6))

sns.barplot(
    x=product_export_value.index,
    y=product_export_value.values
)

plt.title("Petrochemical Export Value by Product")
plt.xlabel("Product")
plt.ylabel("Export Value")

plt.xticks(rotation=45)
plt.tight_layout()

plt.show()


# ========================================
# 3. EXPORT VALUE TREND BY YEAR
# ========================================

plt.figure(figsize=(10, 6))

sns.lineplot(
    data=df,
    x="year",
    y="export_value",
    estimator="sum",
    errorbar=None,
    marker="o"
)

plt.title("Petrochemical Export Value Trend (2021–2023)")
plt.xlabel("Year")
plt.ylabel("Export Value")

plt.tight_layout()

plt.show()


# ========================================
# 4. COUNTRY-WISE YEARLY TREND
# ========================================

country_year = (
    df.groupby(
        ["year", "reporter_country"]
    )["export_value"]
    .sum()
    .reset_index()
)

plt.figure(figsize=(12, 6))

sns.lineplot(
    data=country_year,
    x="year",
    y="export_value",
    hue="reporter_country",
    marker="o"
)

plt.title("Petrochemical Export Trend by Country")
plt.xlabel("Year")
plt.ylabel("Export Value")

plt.tight_layout()

plt.show()


# ========================================
# 5. PRODUCT-WISE YEARLY TREND
# ========================================

product_year = (
    df.groupby(
        ["year", "product"]
    )["export_value"]
    .sum()
    .reset_index()
)

plt.figure(figsize=(12, 6))

sns.lineplot(
    data=product_year,
    x="year",
    y="export_value",
    hue="product",
    marker="o"
)

plt.title("Petrochemical Export Trend by Product")
plt.xlabel("Year")
plt.ylabel("Export Value")

plt.tight_layout()

plt.show()


# ========================================
# 6. CORRELATION ANALYSIS
# ========================================

numeric_columns = [
    "net_weight",
    "trade_value",
    "export_value"
]

correlation_matrix = df[numeric_columns].corr()

print("\n========================================")
print("CORRELATION MATRIX")
print("========================================")

print(correlation_matrix)


plt.figure(figsize=(8, 6))

sns.heatmap(
    correlation_matrix,
    annot=True,
    fmt=".2f"
)

plt.title("Correlation Between Trade Variables")

plt.tight_layout()

plt.show()


# ========================================
# 7. INTERACTIVE COUNTRY CHART
# ========================================

plotly_country = (
    df.groupby(
        "reporter_country",
        as_index=False
    )["export_value"]
    .sum()
    .sort_values(
        "export_value",
        ascending=False
    )
)

fig_country = px.bar(
    plotly_country,
    x="reporter_country",
    y="export_value",
    title="Interactive Petrochemical Export Value by Country",
    labels={
        "reporter_country": "Country",
        "export_value": "Export Value"
    }
)

fig_country.show()


# ========================================
# 8. INTERACTIVE PRODUCT CHART
# ========================================

plotly_product = (
    df.groupby(
        "product",
        as_index=False
    )["export_value"]
    .sum()
    .sort_values(
        "export_value",
        ascending=False
    )
)

fig_product = px.bar(
    plotly_product,
    x="product",
    y="export_value",
    title="Interactive Petrochemical Export Value by Product",
    labels={
        "product": "Product",
        "export_value": "Export Value"
    }
)

fig_product.show()


# ========================================
# 9. MARKET INSIGHTS
# ========================================

highest_country = country_export_value.idxmax()
highest_country_value = country_export_value.max()

highest_product = product_export_value.idxmax()
highest_product_value = product_export_value.max()

highest_year = year_export_value.idxmax()
highest_year_value = year_export_value.max()

highest_weight_country = country_net_weight.idxmax()
highest_weight = country_net_weight.max()


print("\n========================================")
print("GLOBAL MARKET INSIGHTS")
print("========================================")

print(
    f"Highest total export value by country: "
    f"{highest_country} "
    f"({highest_country_value:,.2f})"
)

print(
    f"Highest total export value by product: "
    f"{highest_product} "
    f"({highest_product_value:,.2f})"
)

print(
    f"Highest export value year: "
    f"{highest_year} "
    f"({highest_year_value:,.2f})"
)

print(
    f"Highest total net weight by country: "
    f"{highest_weight_country} "
    f"({highest_weight:,.2f})"
)


# ========================================
# ANALYSIS COMPLETE
# ========================================

print("\n========================================")
print("GLOBAL TRADE ANALYSIS COMPLETE")
print("========================================")