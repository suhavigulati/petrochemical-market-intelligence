import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px


# ========================================
# LOAD DATA
# ========================================

input_file = (
    "data/processed/"
    "petrochemical_market_intelligence.csv"
)

df = pd.read_csv(input_file)

print("Market intelligence data loaded successfully!")
print("Total records:", len(df))


# ========================================
# DATASET INFORMATION
# ========================================

print("\n========================================")
print("DATASET INFORMATION")
print("========================================")

print("\nColumns:")
print(df.columns.tolist())

print("\nCountries:")
print(df["reporter_country"].unique())

print("\nProducts:")
print(df["product"].unique())

print("\nYears:")
print(df["year"].unique())


# ========================================
# EXPORT VALUE BY COUNTRY
# ========================================

country_export = (
    df.groupby("reporter_country")[
        "export_value"
    ]
    .sum()
    .sort_values(ascending=False)
)

print("\n========================================")
print("EXPORT VALUE BY COUNTRY")
print("========================================")

print(country_export)


# ========================================
# EXPORT VALUE BY PRODUCT
# ========================================

product_export = (
    df.groupby("product")[
        "export_value"
    ]
    .sum()
    .sort_values(ascending=False)
)

print("\n========================================")
print("EXPORT VALUE BY PRODUCT")
print("========================================")

print(product_export)


# ========================================
# PRICE BY PRODUCT AND YEAR
# ========================================

price_trend = (
    df.groupby(
        ["year", "product"]
    )["price_usd_per_mt"]
    .first()
    .reset_index()
)

print("\n========================================")
print("PETROCHEMICAL PRICE TREND")
print("========================================")

print(price_trend)


# ========================================
# TOTAL EXPORT VALUE BY YEAR
# ========================================

year_export = (
    df.groupby("year")[
        "export_value"
    ]
    .sum()
    .sort_index()
)

print("\n========================================")
print("EXPORT VALUE BY YEAR")
print("========================================")

print(year_export)


# ========================================
# ESTIMATED MARKET VALUE BY COUNTRY
# ========================================

market_value = (
    df.groupby("reporter_country")[
        "estimated_market_value"
    ]
    .sum()
    .sort_values(ascending=False)
)

print("\n========================================")
print("ESTIMATED MARKET VALUE BY COUNTRY")
print("========================================")

print(market_value)


# ========================================
# PRICE CHANGE 2021 → 2023
# ========================================

price_pivot = price_trend.pivot(
    index="product",
    columns="year",
    values="price_usd_per_mt"
)

price_pivot["price_change_percent"] = (
    (
        price_pivot[2023]
        - price_pivot[2021]
    )
    / price_pivot[2021]
) * 100

print("\n========================================")
print("PRICE CHANGE 2021 → 2023")
print("========================================")

print(
    price_pivot[
        [
            2021,
            2022,
            2023,
            "price_change_percent"
        ]
    ]
)


# ========================================
# EXPORT VALUE TREND
# ========================================

plt.figure(figsize=(10, 6))

sns.lineplot(
    x=year_export.index,
    y=year_export.values,
    marker="o"
)

plt.title(
    "Total Petrochemical Export Value (2021–2023)"
)

plt.xlabel("Year")
plt.ylabel("Export Value")

plt.tight_layout()

plt.show()


# ========================================
# PRICE TREND
# ========================================

plt.figure(figsize=(12, 6))

sns.lineplot(
    data=price_trend,
    x="year",
    y="price_usd_per_mt",
    hue="product",
    marker="o"
)

plt.title(
    "Petrochemical Price Trends (2021–2023)"
)

plt.xlabel("Year")

plt.ylabel(
    "Price (USD per Metric Ton)"
)

plt.tight_layout()

plt.show()


# ========================================
# EXPORT VALUE BY COUNTRY
# ========================================

plt.figure(figsize=(10, 6))

sns.barplot(
    x=country_export.index,
    y=country_export.values
)

plt.title(
    "Total Petrochemical Export Value by Country"
)

plt.xlabel("Country")

plt.ylabel("Export Value")

plt.xticks(rotation=45)

plt.tight_layout()

plt.show()


# ========================================
# PRICE VS EXPORT VALUE
# ========================================

price_export = (
    df.groupby(
        ["year", "product"]
    )
    .agg(
        price_usd_per_mt=(
            "price_usd_per_mt",
            "first"
        ),
        export_value=(
            "export_value",
            "sum"
        )
    )
    .reset_index()
)

print("\n========================================")
print("PRICE VS EXPORT VALUE CORRELATION")
print("========================================")

print(
    price_export[
        [
            "price_usd_per_mt",
            "export_value"
        ]
    ].corr()
)


# ========================================
# PRICE VS EXPORT VALUE SCATTER
# ========================================

plt.figure(figsize=(10, 6))

sns.scatterplot(
    data=price_export,
    x="price_usd_per_mt",
    y="export_value",
    hue="product",
    s=100
)

plt.title(
    "Petrochemical Price vs Export Value"
)

plt.xlabel(
    "Price (USD per Metric Ton)"
)

plt.ylabel(
    "Export Value"
)

plt.tight_layout()

plt.show()


# ========================================
# PLOTLY PRICE TREND
# ========================================

fig_price = px.line(
    price_trend,
    x="year",
    y="price_usd_per_mt",
    color="product",
    markers=True,
    title="Interactive Petrochemical Price Trends",
    labels={
        "year": "Year",
        "price_usd_per_mt": "Price (USD/MT)",
        "product": "Product"
    }
)

fig_price.show()


# ========================================
# PLOTLY COUNTRY EXPORTS
# ========================================

plotly_country = (
    country_export
    .reset_index()
)

fig_country = px.bar(
    plotly_country,
    x="reporter_country",
    y="export_value",
    title="Interactive Export Value by Country",
    labels={
        "reporter_country": "Country",
        "export_value": "Export Value"
    }
)

fig_country.show()


# ========================================
# MARKET INSIGHTS
# ========================================

highest_export_country = (
    country_export.idxmax()
)

highest_export_country_value = (
    country_export.max()
)

highest_export_product = (
    product_export.idxmax()
)

highest_export_product_value = (
    product_export.max()
)

highest_market_value_country = (
    market_value.idxmax()
)

highest_market_value = (
    market_value.max()
)

largest_price_increase_product = (
    price_pivot[
        "price_change_percent"
    ].idxmax()
)

largest_price_increase = (
    price_pivot[
        "price_change_percent"
    ].max()
)

largest_price_decrease_product = (
    price_pivot[
        "price_change_percent"
    ].idxmin()
)

largest_price_decrease = (
    price_pivot[
        "price_change_percent"
    ].min()
)


print("\n========================================")
print("MARKET INTELLIGENCE INSIGHTS")
print("========================================")

print(
    f"Highest export value country: "
    f"{highest_export_country} "
    f"({highest_export_country_value:,.2f})"
)

print(
    f"Highest export value product: "
    f"{highest_export_product} "
    f"({highest_export_product_value:,.2f})"
)

print(
    f"Highest estimated market value country: "
    f"{highest_market_value_country} "
    f"({highest_market_value:,.2f})"
)

print(
    f"Largest price increase, 2021–2023: "
    f"{largest_price_increase_product} "
    f"({largest_price_increase:.2f}%)"
)

print(
    f"Largest price decrease, 2021–2023: "
    f"{largest_price_decrease_product} "
    f"({largest_price_decrease:.2f}%)"
)


# ========================================
# COMPLETE
# ========================================

print("\n========================================")
print("MARKET INTELLIGENCE ANALYSIS COMPLETE")
print("========================================")