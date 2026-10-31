import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px


# ========================================
# LOAD DATA
# ========================================

input_file = "data/processed/petrochemical_trade_cleaned.csv"

df = pd.read_csv(input_file)

print("Data loaded successfully!")
print("Total records:", len(df))


# ========================================
# BASIC DATASET INFORMATION
# ========================================

print("\n========================================")
print("DATASET INFORMATION")
print("========================================")

print("\nColumns:")
print(df.columns.tolist())

print("\nProducts:")
print(df["product"].unique())

print("\nData types:")
print(df.dtypes)


# ========================================
# RECORD COUNT BY PRODUCT
# ========================================

product_count = df["product"].value_counts()

print("\n========================================")
print("RECORDS BY PRODUCT")
print("========================================")

print(product_count)


# ========================================
# TOTAL EXPORT VALUE BY PRODUCT
# ========================================

export_value = (
    df.groupby("product")["export_value"]
    .sum()
    .sort_values(ascending=False)
)

print("\n========================================")
print("TOTAL EXPORT VALUE BY PRODUCT")
print("========================================")

print(export_value)


# ========================================
# TOTAL NET WEIGHT BY PRODUCT
# ========================================

net_weight = (
    df.groupby("product")["net_weight"]
    .sum()
    .sort_values(ascending=False)
)

print("\n========================================")
print("TOTAL NET WEIGHT BY PRODUCT")
print("========================================")

print(net_weight)


# ========================================
# AVERAGE TRADE VALUE BY PRODUCT
# ========================================

average_trade_value = (
    df.groupby("product")["trade_value"]
    .mean()
    .sort_values(ascending=False)
)

print("\n========================================")
print("AVERAGE TRADE VALUE BY PRODUCT")
print("========================================")

print(average_trade_value)


# ========================================
# 1. EXPORT VALUE BAR CHART
# ========================================

plt.figure(figsize=(10, 6))

sns.barplot(
    x=export_value.index,
    y=export_value.values
)

plt.title("Petrochemical Export Value by Product")
plt.xlabel("Petrochemical Product")
plt.ylabel("Export Value")

plt.xticks(rotation=45)
plt.tight_layout()

plt.show()


# ========================================
# 2. NET WEIGHT BAR CHART
# ========================================

plt.figure(figsize=(10, 6))

sns.barplot(
    x=net_weight.index,
    y=net_weight.values
)

plt.title("Petrochemical Export Quantity by Product")
plt.xlabel("Petrochemical Product")
plt.ylabel("Net Weight")

plt.xticks(rotation=45)
plt.tight_layout()

plt.show()


# ========================================
# 3. TRADE VALUE DISTRIBUTION
# ========================================

plt.figure(figsize=(10, 6))

sns.boxplot(
    data=df,
    x="product",
    y="trade_value"
)

plt.title("Trade Value Distribution by Product")
plt.xlabel("Petrochemical Product")
plt.ylabel("Trade Value")

plt.xticks(rotation=45)
plt.tight_layout()

plt.show()


# ========================================
# 4. CORRELATION ANALYSIS
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
    cmap="coolwarm",
    fmt=".2f"
)

plt.title("Correlation Between Trade Variables")

plt.tight_layout()

plt.show()


# ========================================
# 5. INTERACTIVE PLOTLY CHART
# ========================================

plotly_df = (
    df.groupby("product", as_index=False)["export_value"]
    .sum()
    .sort_values("export_value", ascending=False)
)

fig = px.bar(
    plotly_df,
    x="product",
    y="export_value",
    title="Interactive Petrochemical Export Value by Product",
    labels={
        "product": "Petrochemical Product",
        "export_value": "Export Value"
    }
)

fig.show()


# ========================================
# MARKET INSIGHTS
# ========================================

highest_export_product = export_value.idxmax()
highest_export_value = export_value.max()

highest_weight_product = net_weight.idxmax()
highest_weight = net_weight.max()

highest_average_trade_product = average_trade_value.idxmax()
highest_average_trade = average_trade_value.max()

print("\n========================================")
print("MARKET INSIGHTS")
print("========================================")

print(
    f"Highest total export value: "
    f"{highest_export_product} "
    f"({highest_export_value:,.2f})"
)

print(
    f"Highest total net weight: "
    f"{highest_weight_product} "
    f"({highest_weight:,.2f})"
)

print(
    f"Highest average trade value: "
    f"{highest_average_trade_product} "
    f"({highest_average_trade:,.2f})"
)


# ========================================
# ANALYSIS COMPLETE
# ========================================

print("\n========================================")
print("ADVANCED DATA ANALYSIS COMPLETE")
print("========================================")