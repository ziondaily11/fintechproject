# data_loader.py
import pandas as pd
import streamlit as st
from pathlib import Path


def data_store():
    saf_data = pd.read_csv(Path(__file__).parent / "mpesa_synthetic.csv")
    return saf_data


@st.cache_data(ttl=90)
def calc(saf_data):
    saf_data = saf_data.dropna(subset="transaction_id")
    total_transactions = saf_data["transaction_id"].nunique()
    total_volume = saf_data["amount"].sum()
    fraud_count = saf_data["is_fraud"].sum()
    fraud_rate = fraud_count * 100 / total_transactions

    saf_data["amount_cat"] = pd.cut(
        saf_data["amount"],
        bins=[0, 500, 1000, 2000, 5000, float("inf")],
        labels=["0-500", "500-1k", "1k-2k", "2k-5k", "5k+"]
    )
    fraud_rate_per_amount = (
        (saf_data.groupby("amount_cat")["is_fraud"].mean() * 100)
        .rename("rate")
        .reset_index()
    )

    fraud_amt = saf_data[saf_data["is_fraud"] == 1]["amount"].sum()
    legit_amt = round(total_volume - fraud_amt, 0)

    fraud_avg = saf_data[saf_data["is_fraud"] == 1]["amount"].mean()
    legit_avg = saf_data[saf_data["is_fraud"] == 0]["amount"].mean()

    fraud_hourly_counts = (
        saf_data[saf_data["is_fraud"] == 1]
        .groupby("hour")
        .size()
        .reset_index(name="count")
    )
    fraud_hourly_counts = fraud_hourly_counts.sort_values("hour")
    if fraud_hourly_counts.empty:
        peak_hour = None
        peak_hour_counts = 0
    else:
        peak_hour = fraud_hourly_counts.loc[fraud_hourly_counts["count"].idxmax(), "hour"]
        peak_hour_counts = fraud_hourly_counts["count"].max()

    threshold = peak_hour_counts * 0.9

    fraud_rate_region = (
        saf_data.groupby(by=["region"])["is_fraud"].mean().reset_index()
    )
    fraud_rate_region["is_fraud"] = round(fraud_rate_region["is_fraud"] * 100, 2)

    fraud_rate_hour = (saf_data.groupby(by=["hour"])["is_fraud"].mean().reset_index())
    fraud_rate_hour["is_fraud"] = round(fraud_rate_hour["is_fraud"] * 100, 2)

    transaction_split = (
        saf_data.groupby(by="transaction_type")[["transaction_id"]].size()
    )

    amount_dist = (
        saf_data.groupby("amount_cat")["amount"]
        .sum()
        .rename("total_amount")
        .reset_index()
    )

    tran_per_hour = (
        saf_data.groupby("hour")["transaction_id"].size().sort_index()
    )

    smart_count = (saf_data["device_type"] == "smartphone").sum()
    feature_count = (saf_data["device_type"] == "feature").sum()
    total = smart_count + feature_count
    smart_pct = round(smart_count * 100 / total, 2)
    feature_pct = round(feature_count * 100 / total, 2)
    #fraud rate by device type per region
    device_fraud_rate = (
        saf_data.groupby(["region", "device_type"])["is_fraud"].mean().reset_index()
    )
    device_fraud_rate["is_fraud"] = round(device_fraud_rate["is_fraud"] * 100, 2)
    device_per_region = (
        saf_data.groupby(["region", "device_type"]).size()
    )

    phone_dist = (
        saf_data.groupby(["region", "device_type"])
        .size()
        .reset_index(name="count")
    )

    Trans_daily = (
        saf_data.groupby(by=["day_of_week"])[["transaction_id"]].size()
        .reset_index(name="count")
        .rename(columns={"day_of_week": "day"})
    )
    Trans_daily = Trans_daily.sort_values("day")

    return (
        total_transactions, total_volume, transaction_split, tran_per_hour,
        fraud_amt, fraud_avg, fraud_count, fraud_hourly_counts, fraud_rate,
        fraud_rate_per_amount, feature_count, feature_pct, smart_count, smart_pct,
        legit_amt, legit_avg, peak_hour, peak_hour_counts, amount_dist,
        fraud_rate_region, fraud_rate_hour, phone_dist, device_fraud_rate, Trans_daily, threshold
    )