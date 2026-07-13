#A safaricom mpesa dataset analysis
#modules

import pandas as pd
import streamlit as st
import plotly_express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots as msp
from streamlit_option_menu import option_menu
from pathlib import Path  
import math
import warnings
import sys 
from data_loader import data_store, calc
from filters import render_filters, apply_filters
from kpis import render_kpis
from insights import build_finding_and_recommendation, render_device_split_insight, render_hourly_finding
from charts import (
    fraud_rate_by_amount_chart, fraud_rate_by_region_chart, transaction_split_chart,
    amount_distribution_chart, transactions_vs_fraud_rate_chart, daily_volume_chart,
    fraud_hourly_counts_chart
)


sys.modules['warnings'] = warnings


st.set_page_config(
    page_title= "FinPulseAnalysis",
    page_icon= ":bar_chart:",
    layout= "wide"
)


def show_home():
    st.markdown("""
    <style>
        [data-testid="stVerticalBlock"] > [data-testid="stVerticalBlockBorderWrapper"] {
            padding-top: 0rem;
        }
        .block-container {
            padding-top: 0.5rem;
        }
        div[data-testid="stHorizontalBlock"] {
            margin-top: -2rem;
        }
    </style>
""", unsafe_allow_html=True) 
    saf_data = data_store()
    (
        total_transactions,
        total_volume,
        transaction_split,
        tran_per_hour,
        fraud_amt,
        fraud_avg,
        fraud_count,
        fraud_hourly_counts,
        fraud_rate,
        fraud_rate_per_amount,
        feature_count,
        feature_pct,
        smart_count,
        smart_pct,
        legit_amt,
        legit_avg,
        peak_hour,
        peak_hour_counts,
        amount_dist,
        fraud_rate_region,
        fraud_rate_hour,
        phone_dist,
        device_fraud_rate,
        Trans_daily,
        threshold
    ) = calc(saf_data)

    def format_number(num):
        if num >= 1_000_000_000:
            return f"{num/1_000_000_000:.1f}B"
        elif num >= 1_000_000:
            return f"{num/1_000_000:.1f}M"
        elif num >= 1_000:
            return f"{num/1_000:.1f}K"
        return str(num)

    def format_hour_12(hour):
        if hour is None:
            return "N/A"
        period = "AM" if hour < 12 else "PM"
        hour_12 = hour % 12
        if hour_12 == 0:
            hour_12 = 12
        return f"{hour_12} {period}"

    st.markdown("""
        <style>
            [data-testid="stMetric"] {
                background-color: #0E0D0B;
                border: 1px solid #333;
                border-radius: 10px;
                padding: 20px;
            }
            [data-testid="stMetricLabel"] {
                color: #F4F2F1;
                font-size: 16px;
            }
            [data-testid="stMetricValue"] {
                color: #F4F2F1;
                font-size: 28px;
            }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("""
        <style>
        [data-testid="stMetricDelta"] svg {
            display: none;
        }
        </style>
        """, unsafe_allow_html=True)

    

    region_filter, type_filter, fraud_filter, hour_filter, logo_col = render_filters(saf_data)

    with logo_col:
        st.image(Path(__file__).parent / "projectlogo.png", width=140)
        st.markdown("<div style='margin-left: 0px;'></div>", unsafe_allow_html=True)
        st.markdown("""
            <h1 style="color: #9E1405; font-family: Orbitron, sans-serif;
                font-size:20px; margin: -20px 0 0 0; margin: 0; padding: 0;">
                FINPULSE 
            </h1>
        """, unsafe_allow_html=True)

    filtered_data = apply_filters(saf_data, region_filter, type_filter, fraud_filter, hour_filter)

    if filtered_data.empty:
        st.warning("No transactions match the selected filters. Try widening your selection.")
    (
            total_transactions_f, total_volume_f, transaction_split_f, tran_per_hour_f,
            fraud_amt_f, fraud_avg_f, fraud_count_f, fraud_hourly_counts_f,
            fraud_rate_f, fraud_rate_per_amount_f, feature_count_f, feature_pct_f,
            smart_count_f, smart_pct_f, legit_amt_f, legit_avg_f, peak_hour_f, peak_hour_counts_f,
            amount_dist_f, fraud_rate_region_f, fraud_rate_hour_f, phone_dist_f, device_fraud_rate_f, Trans_daily_f, threshold_f
    ) = calc(filtered_data)
    legit_avg_f = 0 if math.isnan(legit_avg_f) else legit_avg_f
    fraud_avg_f = 0 if math.isnan(fraud_avg_f) else fraud_avg_f


    

    st.markdown("""
                    <style>
                        div[data-testid="stVerticalBlock"]:has(div.st-key-logo_header) div[data-testid="stHorizontalBlock"] {
                            gap: 0rem;
                        }
                    </style>
                """, unsafe_allow_html=True)
    st.markdown("<div style='margin-top: 20px;'></div>", unsafe_allow_html=True)
    render_kpis(
        total_transactions_f, total_transactions, total_volume_f, total_volume,
        fraud_rate_f, fraud_count_f, legit_avg_f, fraud_avg_f, peak_hour_f, peak_hour_counts_f
    )
    finding_text, recommendation_text = build_finding_and_recommendation(
        filtered_data, fraud_count_f, legit_avg_f, fraud_avg_f,
        total_transactions_f, fraud_rate_f, peak_hour_f
    )
    st.info(f"{finding_text}\n\n{recommendation_text}")
    st.markdown("-")
    #GRAPHS
    #fraude rate per amount

    #GRAPHS
    fraud_rate_bar = fraud_rate_by_amount_chart(fraud_rate_per_amount_f)
    fraud_region = fraud_rate_by_region_chart(fraud_rate_region)
    transaction_split_pie = transaction_split_chart(transaction_split_f)
    amount_dist_bar = amount_distribution_chart(amount_dist_f)
    fig = transactions_vs_fraud_rate_chart(tran_per_hour, fraud_rate_hour)
    trans_daily_bar = daily_volume_chart(Trans_daily_f)
    fraud_count_bar = fraud_hourly_counts_chart(fraud_hourly_counts_f, threshold_f)
    with st.container(border= True):
        col, col1, col_c= st.columns(3)
        with col:
            st.plotly_chart(amount_dist_bar)

        with col1:
            st.plotly_chart(transaction_split_pie)

        with col_c:
            st.plotly_chart(fraud_region)
    st.markdown("<div style='margin-top: 20px;'></div>", unsafe_allow_html=True)  
    with st.container(border= True):
        bar_col, area_col= st.columns([0.9, 2.1])
        with bar_col:
            st.plotly_chart(fraud_rate_bar)
            st.info("🔍:1 in 10 transactions above 5k are Flagged as Fraud.")

        with area_col:
                st.plotly_chart(fig)
                st.info("⚠️Transaction volume remains relatively stable throughout the day\n" 
                "while fraud rates flactuate independently.This suggests that increases in fraud are not driven solely by higher transaction volumes.")
    render_device_split_insight(smart_pct_f, feature_pct_f, device_fraud_rate_f)
    with st.container(border= True):
        bar_col2,  bar_col3= st.columns([2, 3])
        
        with bar_col2:
                st.plotly_chart(trans_daily_bar)
        with bar_col3:
                st.plotly_chart(fraud_count_bar)
    render_hourly_finding(filtered_data, region_filter)
    with st.container(border= True):
        st.caption("Sample dataset")
        st.dataframe(saf_data.head(100))
        st.info(Follow me on X- TheeAnalyst_ke)

show_home()
