# kpis.py
import streamlit as st


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


def render_kpis(total_transactions_f, total_transactions, total_volume_f, total_volume,
                 fraud_rate_f, fraud_count_f, legit_avg_f, fraud_avg_f,
                 peak_hour_f, peak_hour_counts_f):
    
    st.markdown("""
        <style>
            [data-testid="stMetric"] {
                background-color: #FFFCFA;
                border: 1px solid #333;
                border-radius: 10px;
                padding: 20px;
            }
            [data-testid="stMetricLabel"] {
                color:  #2E5EAA;
                font-size: 16px;
            }
            [data-testid="stMetricValue"] {
                color:  #2E5EAA;
                font-size: 28px;
            }
        </style>
    """, unsafe_allow_html=True)

    
    lef, mid_lef, mid, mid_righ, rig, col = st.columns(6)

    with lef:
        st.metric(
            label="Total Transactions",
            value=f"{total_transactions_f:,}",
            delta=f"{round(total_transactions_f/total_transactions*100, 1)}% of Total Trxnx"
        )
    with mid_lef:
        st.metric(
            label="Total Volume",
            value=f"KES {format_number(total_volume_f)}",
            delta=f"{round(total_volume_f/total_volume*100, 1)}% of Total Value"
        )
    with mid:
        st.metric(
            label="Fraud Rate", value=f"{round(fraud_rate_f, 2)}%",
            delta=f"{fraud_count_f} flagged txns",
            delta_color="inverse"
        )
    with mid_righ:
        st.metric(
            label="Avg. legitimate Amount",
            value=f"KES {round(legit_avg_f):,}",
            delta="per transaction"
        )
    with rig:
        if legit_avg_f == 0:
            delta_text = "no legitimate txns to compare" if fraud_avg_f > 0 else "no data"
        else:
            delta_text = f"{round(fraud_avg_f/legit_avg_f, 2)}x larger than legit"
        st.metric(
            label="Avg. Fraud Amount",
            value=f"KES {round(fraud_avg_f):,}",
            delta=delta_text,
            delta_color="inverse"
        )
    with col:
        st.metric(
            label="Peak Fraud Hour",
            value=format_hour_12(peak_hour_f),
            delta=f"Hour {peak_hour_f}--{peak_hour_counts_f} cases",
            delta_color="inverse"
        )