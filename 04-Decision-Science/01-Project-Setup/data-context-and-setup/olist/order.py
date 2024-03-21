import pandas as pd
import numpy as np
from olist.utils import haversine_distance
from olist.data import Olist


class Order:
    """
    DataFrames containing all orders as index,
    and various properties of these orders as columns
    """

    def __init__(self):
        # Assign an attribute ".data" to all new instances of Order
        self.data = Olist().get_data()

    def get_wait_time(self, is_delivered=True):
        """
        Returns a DataFrame with:
        [order_id, wait_time, expected_wait_time, delay_vs_expected, order_status]
        and filters out non-delivered orders unless specified
        """

        dt_columns = [
            "order_purchase_timestamp",
            "order_approved_at",
            "order_delivered_carrier_date",
            "order_delivered_customer_date",
            "order_estimated_delivery_date",
        ]
        orders = self.data["orders"].copy()

        # Optionally filter on order_status="delivered"
        if is_delivered:
            orders = orders[orders["order_status"] == "delivered"]

        # Convert date columns to datetime
        for col_name in dt_columns:
            orders.loc[:, col_name] = pd.to_datetime(orders.loc[:, col_name])

        # Calculate datetime
        orders["wait_time"] = (
            orders["order_delivered_customer_date"] - orders["order_purchase_timestamp"]
        ).dt.days

        # Calculate time between purchase and expected delivery
        orders["expected_wait_time"] = (
            orders["order_estimated_delivery_date"] - orders["order_purchase_timestamp"]
        ).dt.days

        # Calculate delay
        orders["delay_vs_expected"] = (
            orders["order_delivered_customer_date"]
            - orders["order_estimated_delivery_date"]
        ).dt.days
        orders.loc[orders["delay_vs_expected"] < 0, "delay_vs_expected"] = 0

        return orders[
            [
                "order_id",
                "wait_time",
                "expected_wait_time",
                "delay_vs_expected",
                "order_status",
            ]
        ]

    # Option to get_review_score
    def get_all_review_score_counts(self):
       """
       Returns a DataFrame with:
       order_id, dim_is_five_star, dim_is_one_star, review_score
       """
       reviews = self.data["order_reviews"].copy()
       reviews["dim_is_one_star"] = np.where(reviews["review_score"] == 1, 1, 0)
       reviews["dim_is_two_star"] = np.where(reviews["review_score"] == 2, 1, 0)
       reviews["dim_is_three_star"] = np.where(reviews["review_score"] == 3, 1, 0)
       reviews["dim_is_four_star"] = np.where(reviews["review_score"] == 4, 1, 0)
       reviews["dim_is_five_star"] = np.where(reviews["review_score"] == 5, 1, 0)

       return reviews[
           [
               "order_id",
               "dim_is_one_star",
               "dim_is_two_star",
               "dim_is_three_star",
               "dim_is_four_star",
               "dim_is_five_star",
               "review_score",
           ]
       ]

    def get_review_score(self):
        """
        Returns a DataFrame with:
        order_id, dim_is_five_star, dim_is_one_star, review_score, review_cost
        """
        # Calculate cost per review
        score_cost = {1: 100, 2: 50, 3: 40, 4: 0, 5: 0}

        reviews = self.data["order_reviews"].copy()[["order_id", "review_score"]]

        reviews["review_cost"] = reviews["review_score"].replace(score_cost)

        reviews["dim_is_one_star"] = np.where(reviews["review_score"] == 1, 1, 0)
        reviews["dim_is_five_star"] = np.where(reviews["review_score"] == 5, 1, 0)

        # Group reviews by order. Aggregate according to the following:
        # For review score, keep the minimum -- i.e. worst review
        # For review cost, keep the maximum cost -- i.e. most costly review
        # For dim_is_one_star and dim_is_fivee_star, keep the max value -- i.e. the 1.
        # This means that an "aggregated review" can be both a one star review and a five star review.
        reviews_by_order = reviews.groupby("order_id").agg(
            {
                "review_score": "min",
                "review_cost": "max",
                "dim_is_one_star": "max",
                "dim_is_five_star": "max",
            }
        )

        return reviews_by_order

    def get_number_products(self):
        """
        Returns a DataFrame with:
        order_id, number_of_products
        """
        return (
            self.data["order_items"]
            .copy()[["order_id", "product_id"]]
            .groupby("order_id")
            .count()
            .reset_index()
            .rename(columns={"product_id": "number_of_products"})
        )

    def get_number_sellers(self):
        """
        Returns a DataFrame with:
        order_id, number_of_sellers
        """
        return (
            self.data["order_items"]
            .copy()[["order_id", "seller_id"]]
            .groupby("order_id")
            .nunique()
            .reset_index()
            .rename(columns={"seller_id": "number_of_sellers"})
        )

    def get_price_and_freight(self):
        """
        Returns a DataFrame with:
        order_id, price, freight_value
        """
        return (
            self.data["order_items"]
            .copy()
            .groupby("order_id")
            .sum()
            .drop("order_item_id", axis=1)
            .reset_index()
        )

    # Optional
    def get_distance_seller_customer(self):
        """
        Returns a DataFrame with:
        order_id, distance_seller_customer
        """
        orders = self.data["orders"].copy()
        order_items = self.data["order_items"].copy()
        customers = self.data["customers"].copy()
        sellers = self.data["sellers"].copy()

        # Group by zip code prefix
        geolocation = (
            self.data["geolocation"]
            .copy()[
                ["geolocation_zip_code_prefix", "geolocation_lat", "geolocation_lng"]
            ]
            .groupby("geolocation_zip_code_prefix")
            .mean()
            .reset_index()
        )

        items_customers_sellers = order_items.merge(orders, how="left", on="order_id")[
            ["order_id", "customer_id", "seller_id"]
        ]

        items_customers_sellers_zips = items_customers_sellers.merge(
            customers[["customer_id", "customer_zip_code_prefix"]],
            how="left",
            on="customer_id",
        ).merge(
            sellers[["seller_id", "seller_zip_code_prefix"]], how="left", on="seller_id"
        )

        items_customers_sellers_zips_coords = items_customers_sellers_zips.merge(
            geolocation,
            how="left",
            left_on="customer_zip_code_prefix",
            right_on="geolocation_zip_code_prefix",
        ).merge(
            geolocation,
            how="left",
            left_on="seller_zip_code_prefix",
            right_on="geolocation_zip_code_prefix",
            suffixes=["_customer", "_seller"],
        )

        items_customers_sellers_zips_coords[
            "distance_seller_customer"
        ] = items_customers_sellers_zips_coords.apply(
            lambda x: haversine_distance(
                x["geolocation_lng_customer"],
                x["geolocation_lat_customer"],
                x["geolocation_lng_seller"],
                x["geolocation_lat_seller"],
            ),
            axis=1,
        )

        orders_with_distance = (
            items_customers_sellers_zips_coords[
                ["order_id", "distance_seller_customer"]
            ]
            .groupby("order_id")
            .mean()
        )

        return orders_with_distance

    def get_training_data(self, is_delivered=True, with_distance_seller_customer=False):
        """
        Returns a clean DataFrame (without NaN), with the all following columns:
        ['order_id', 'wait_time', 'expected_wait_time', 'delay_vs_expected',
        'order_status', 'dim_is_five_star', 'dim_is_one_star', 'review_score',
        'number_of_products', 'number_of_sellers', 'price', 'freight_value',
        'distance_seller_customer']
        """

        orders_summary = (
            self.get_wait_time(is_delivered)
            .merge(self.get_review_score(), how="inner", on="order_id")
            .merge(self.get_number_products(), how="inner", on="order_id")
            .merge(self.get_number_sellers(), how="inner", on="order_id")
            .merge(self.get_price_and_freight(), how="inner", on="order_id")
        )

        if with_distance_seller_customer:
            orders_summary = orders_summary.merge(
                self.get_distance_seller_customer(), how="left", on="order_id"
            ).dropna()

        return orders_summary.dropna()
