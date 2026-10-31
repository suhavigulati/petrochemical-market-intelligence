import requests
import pandas as pd
import os
import time


# ========================================
# UN COMTRADE API
# ========================================

url = "https://comtradeapi.un.org/public/v1/preview/C/A/HS"


# ========================================
# PETROCHEMICAL PRODUCTS
# ========================================

products = {
    "Ethylene": "290121",
    "Propylene": "290122",
    "Benzene": "290220",
    "Toluene": "290230",
    "Methanol": "290511",
    "Styrene": "290250"
}


# ========================================
# COUNTRIES
# ========================================

countries = {
    "China": "156",
    "India": "356",
    "United States": "842",
    "Germany": "276",
    "Saudi Arabia": "682"
}


# ========================================
# YEARS
# ========================================

years = [
    "2021",
    "2022",
    "2023"
]


# ========================================
# TRADE FLOW
# X = EXPORTS
# ========================================

flow_code = "X"


# ========================================
# CREATE RAW DATA FOLDER
# ========================================

os.makedirs("data/raw", exist_ok=True)


# ========================================
# STORE ALL DATA
# ========================================

all_data = []


# ========================================
# START DATA COLLECTION
# ========================================

for country_name, reporter_code in countries.items():

    for year in years:

        for product_name, hs_code in products.items():

            print("\n========================================")
            print("Country:", country_name)
            print("Year:", year)
            print("Product:", product_name)
            print("HS Code:", hs_code)
            print("========================================")

            params = {
                "flowCode": flow_code,
                "reporterCode": reporter_code,
                "period": year,
                "cmdCode": hs_code
            }

            try:

                response = requests.get(
                    url,
                    params=params,
                    timeout=30
                )

                print("Status Code:", response.status_code)

                # ========================================
                # SUCCESS
                # ========================================

                if response.status_code == 200:

                    data = response.json()

                    record_count = data.get("count", 0)

                    print("Number of records:", record_count)

                    if record_count > 0:

                        df = pd.DataFrame(data["data"])

                        df["product"] = product_name
                        df["product_hs_code"] = hs_code
                        df["reporter_country"] = country_name
                        df["trade_year"] = year

                        print(
                            "Data received:",
                            len(df),
                            "records"
                        )

                        all_data.append(df)

                    else:

                        print(
                            "No data found for",
                            country_name,
                            year,
                            product_name
                        )


                # ========================================
                # RATE LIMIT
                # ========================================

                elif response.status_code == 429:

                    print(
                        "Rate limit reached."
                    )

                    print(
                        "Waiting 15 seconds before retry..."
                    )

                    time.sleep(15)

                    response = requests.get(
                        url,
                        params=params,
                        timeout=30
                    )

                    print(
                        "Retry Status Code:",
                        response.status_code
                    )

                    if response.status_code == 200:

                        data = response.json()

                        record_count = data.get(
                            "count",
                            0
                        )

                        print(
                            "Number of records:",
                            record_count
                        )

                        if record_count > 0:

                            df = pd.DataFrame(
                                data["data"]
                            )

                            df["product"] = product_name
                            df["product_hs_code"] = hs_code
                            df["reporter_country"] = country_name
                            df["trade_year"] = year

                            print(
                                "Data received:",
                                len(df),
                                "records"
                            )

                            all_data.append(df)

                    else:

                        print(
                            "Retry failed."
                        )


                # ========================================
                # OTHER ERROR
                # ========================================

                else:

                    print(
                        "Request failed with status:",
                        response.status_code
                    )

            except Exception as e:

                print(
                    "Error:",
                    e
                )


            # ========================================
            # DELAY BETWEEN REQUESTS
            # ========================================

            time.sleep(3)


# ========================================
# SAVE ALL DATA
# ========================================

if all_data:

    final_df = pd.concat(
        all_data,
        ignore_index=True
    )

    output_file = (
        "data/raw/"
        "petrochemical_global_trade_2021_2023.csv"
    )

    final_df.to_csv(
        output_file,
        index=False
    )


    # ========================================
    # SUMMARY
    # ========================================

    print("\n========================================")
    print("GLOBAL TRADE DATA SAVED")
    print("========================================")

    print(
        "Total records:",
        len(final_df)
    )

    print("\nCountries collected:")

    print(
        final_df["reporter_country"]
        .value_counts()
    )

    print("\nYears collected:")

    print(
        final_df["trade_year"]
        .value_counts()
        .sort_index()
    )

    print("\nProducts collected:")

    print(
        final_df["product"]
        .value_counts()
    )

    print("\nFile saved:")

    print(output_file)


else:

    print("\n========================================")
    print("NO DATA WAS COLLECTED")
    print("========================================")