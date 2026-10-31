import streamlit as st
import pandas as pd
import plotly.express as px


# ========================================
# PAGE CONFIGURATION
# ========================================

st.set_page_config(
    page_title="Petrochemical Market Intelligence",
    page_icon="📊",
    layout="wide"
)


# ========================================
# LOAD DATA
# ========================================

data_file = (
    "data/processed/"
    "petrochemical_market_intelligence.csv"
)

df = pd.read_csv(data_file)


# ========================================
# LOAD FORECAST DATA
# ========================================

forecast_file = (
    "data/processed/"
    "petrochemical_price_forecasts.csv"
)

forecast_df = pd.read_csv(forecast_file)


# ========================================
# TITLE
# ========================================

st.title(
    "📊 Petrochemical Market Intelligence Dashboard"
)

st.markdown(
    """
    **Global Trade, Pricing and Market Analytics**

    This dashboard provides insights into petrochemical
    trade flows, export values, benchmark prices and
    baseline price forecasts.
    """
)


# ========================================
# SIDEBAR
# ========================================

st.sidebar.header("Dashboard Filters")


countries = sorted(
    df["reporter_country"].unique()
)

products = sorted(
    df["product"].unique()
)

years = sorted(
    df["year"].unique()
)


selected_country = st.sidebar.selectbox(
    "Select Country",
    ["All"] + countries
)

selected_product = st.sidebar.selectbox(
    "Select Product",
    ["All"] + products
)

selected_year = st.sidebar.selectbox(
    "Select Year",
    ["All"] + years
)


# ========================================
# FILTER DATA
# ========================================

filtered_df = df.copy()


if selected_country != "All":

    filtered_df = filtered_df[
        filtered_df["reporter_country"]
        == selected_country
    ]


if selected_product != "All":

    filtered_df = filtered_df[
        filtered_df["product"]
        == selected_product
    ]


if selected_year != "All":

    filtered_df = filtered_df[
        filtered_df["year"]
        == selected_year
    ]


# ========================================
# KPI CALCULATIONS
# ========================================

total_export_value = filtered_df[
    "export_value"
].sum()

total_trade_value = filtered_df[
    "trade_value"
].sum()

total_net_weight = filtered_df[
    "net_weight"
].sum()

total_records = len(filtered_df)


# ========================================
# KPI CARDS
# ========================================

col1, col2, col3, col4 = st.columns(4)


with col1:

    st.metric(
        "Total Export Value",
        f"${total_export_value:,.0f}"
    )


with col2:

    st.metric(
        "Total Trade Value",
        f"${total_trade_value:,.0f}"
    )


with col3:

    st.metric(
        "Total Net Weight",
        f"{total_net_weight:,.0f}"
    )


with col4:

    st.metric(
        "Trade Records",
        f"{total_records:,}"
    )


# ========================================
# EXPORT VALUE BY COUNTRY
# ========================================

st.header("🌍 Export Value by Country")


country_export = (
    filtered_df
    .groupby("reporter_country")["export_value"]
    .sum()
    .reset_index()
    .sort_values(
        "export_value",
        ascending=False
    )
)


fig_country = px.bar(
    country_export,
    x="reporter_country",
    y="export_value",
    title="Total Export Value by Country",
    labels={
        "reporter_country": "Country",
        "export_value": "Export Value (USD)"
    }
)


st.plotly_chart(
    fig_country,
    use_container_width=True
)


# ========================================
# EXPORT VALUE BY PRODUCT
# ========================================

st.header("🧪 Export Value by Product")


product_export = (
    filtered_df
    .groupby("product")["export_value"]
    .sum()
    .reset_index()
    .sort_values(
        "export_value",
        ascending=False
    )
)


fig_product = px.bar(
    product_export,
    x="product",
    y="export_value",
    title="Total Export Value by Product",
    labels={
        "product": "Petrochemical Product",
        "export_value": "Export Value (USD)"
    }
)


st.plotly_chart(
    fig_product,
    use_container_width=True
)


# ========================================
# PRICE TREND
# ========================================

st.header("📈 Petrochemical Price Trend")


price_data = (
    filtered_df[
        [
            "year",
            "product",
            "price_usd_per_mt"
        ]
    ]
    .drop_duplicates()
    .sort_values("year")
)


fig_price = px.line(
    price_data,
    x="year",
    y="price_usd_per_mt",
    color="product",
    markers=True,
    title="Benchmark Petrochemical Price Trend",
    labels={
        "year": "Year",
        "price_usd_per_mt": "Price (USD/MT)",
        "product": "Product"
    }
)


st.plotly_chart(
    fig_price,
    use_container_width=True
)


# ========================================
# FORECAST
# ========================================

st.header("🔮 2024 Price Forecast")


forecast_display = forecast_df[
    [
        "product",
        "forecast_year",
        "forecast_price_usd_per_mt"
    ]
].copy()


forecast_display.columns = [
    "Product",
    "Forecast Year",
    "Forecast Price (USD/MT)"
]


st.dataframe(
    forecast_display,
    use_container_width=True
)


# ========================================
# FOOTER
# ========================================

st.markdown("---")

st.caption(
    "Petrochemical Market Intelligence Dashboard | "
    "Trade data: UN Comtrade | "
    "Price data: Centrum Chemical Pulse | "
    "Forecasting: Linear Regression"
)