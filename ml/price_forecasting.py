import pandas as pd
import numpy as np

from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


# ========================================
# LOAD PRICE DATA
# ========================================

input_file = (
    "data/processed/"
    "petrochemical_prices_cleaned.csv"
)

df = pd.read_csv(input_file)

print("Price data loaded successfully!")

print(
    "Total records:",
    len(df)
)


# ========================================
# DISPLAY DATA
# ========================================

print("\n========================================")
print("PRICE DATA")
print("========================================")

print(df)


# ========================================
# PRODUCTS
# ========================================

products = df["product"].unique()

print("\nProducts:")

print(products)


# ========================================
# STORE FORECAST RESULTS
# ========================================

forecast_results = []


# ========================================
# MODEL FOR EACH PRODUCT
# ========================================

for product in products:

    print("\n========================================")
    print("PRODUCT:", product)
    print("========================================")

    product_df = (
        df[df["product"] == product]
        .sort_values("year")
        .copy()
    )

    print("\nHistorical data:")

    print(
        product_df[
            [
                "year",
                "price_usd_per_mt"
            ]
        ]
    )


    # ====================================
    # FEATURES AND TARGET
    # ====================================

    X = product_df[
        ["year"]
    ]

    y = product_df[
        "price_usd_per_mt"
    ]


    # ====================================
    # TRAIN MODEL
    # ====================================

    model = LinearRegression()

    model.fit(
        X,
        y
    )


    # ====================================
    # HISTORICAL PREDICTIONS
    # ====================================

    y_pred = model.predict(X)


    # ====================================
    # MODEL METRICS
    # ====================================

    mae = mean_absolute_error(
        y,
        y_pred
    )

    rmse = np.sqrt(
        mean_squared_error(
            y,
            y_pred
        )
    )

    r2 = r2_score(
        y,
        y_pred
    )


    print("\nModel metrics:")

    print(
        "MAE:",
        round(mae, 2)
    )

    print(
        "RMSE:",
        round(rmse, 2)
    )

    print(
        "R2:",
        round(r2, 4)
    )


    # ====================================
    # FORECAST 2024
    # ====================================

    future_year = pd.DataFrame(
        {
            "year": [2024]
        }
    )

    forecast_price = model.predict(
        future_year
    )[0]


    print(
        "\nForecast price for 2024:",
        round(
            forecast_price,
            2
        ),
        "USD/MT"
    )


    # ====================================
    # SAVE RESULT
    # ====================================

    forecast_results.append(
        {
            "product": product,
            "mae": mae,
            "rmse": rmse,
            "r2": r2,
            "forecast_year": 2024,
            "forecast_price_usd_per_mt":
                forecast_price
        }
    )


# ========================================
# CREATE RESULTS DATAFRAME
# ========================================

results_df = pd.DataFrame(
    forecast_results
)


# ========================================
# DISPLAY RESULTS
# ========================================

print("\n========================================")
print("PRICE FORECASTING RESULTS")
print("========================================")

print(
    results_df
)


# ========================================
# SAVE RESULTS
# ========================================

output_file = (
    "data/processed/"
    "petrochemical_price_forecasts.csv"
)

results_df.to_csv(
    output_file,
    index=False
)


print("\nForecast results saved to:")

print(output_file)


# ========================================
# COMPLETE
# ========================================

print("\n========================================")
print("PRICE FORECASTING COMPLETE")
print("========================================")