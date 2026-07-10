# filters.py
import streamlit as st


def render_filters(saf_data):
    logo_col, space_col, col_region, col_type, col_fraud, col_hour = st.columns(
        [1, 1, 2, 2, 2, 2], vertical_alignment="center", gap="small"
    )

    with col_region:
        region_filter = st.multiselect(
            "Region",
            options=sorted(saf_data["region"].unique()),
            default=[],
            placeholder="Choose Region",
            label_visibility="collapsed"
        )
    with col_type:
        type_filter = st.multiselect(
            "Transaction Type",
            options=sorted(saf_data["transaction_type"].unique()),
            default=[],
            placeholder="Choose Txn Type",
            label_visibility="collapsed"
        )
    with col_fraud:
        fraud_filter = st.selectbox(
            "Fraud Status",
            options=["Choose Fraud Status", "All", "Fraud only", "Legit only"],
            label_visibility="collapsed"
        )
    with col_hour:
        hour_filter = st.number_input(
            "hour 0-23",
            min_value=0,
            max_value=23,
            value=None,
            placeholder="Enter hour",
            step=1,
            label_visibility="collapsed"
        )

    return region_filter, type_filter, fraud_filter, hour_filter, logo_col


def apply_filters(saf_data, region_filter, type_filter, fraud_filter, hour_filter):
    filtered_data = saf_data.copy()
    if region_filter:
        filtered_data = filtered_data[filtered_data["region"].isin(region_filter)]
    if type_filter:
        filtered_data = filtered_data[filtered_data["transaction_type"].isin(type_filter)]
    if fraud_filter == "Fraud only":
        filtered_data = filtered_data[filtered_data["is_fraud"] == 1]
    elif fraud_filter == "Legit only":
        filtered_data = filtered_data[filtered_data["is_fraud"] == 0]
    if hour_filter is not None:
        filtered_data = filtered_data[filtered_data["hour"] == hour_filter]
    return filtered_data