# charts.py
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots as msp
from kpis import format_number


def fraud_rate_by_amount_chart(fraud_rate_per_amount_f):
    fig = px.bar(
        fraud_rate_per_amount_f,
        x="amount_cat",
        y="rate",
        title="<b>Fraud rate by transaction amount</b>",
        text= "rate",
        color_discrete_sequence=["#2E5EAA"]
    )
    fig.update_layout(
        height=250, showlegend=False, title_font_color="#E24B4A",
        margin=dict(t=40, b=10, l=10, r=10),
        yaxis=dict(ticksuffix="%", title=None),
        xaxis=dict(title=None, showgrid=False),
    )
    fig.update_traces(
        textposition= "outside",
        texttemplate= "%{text:.2f}%",
        textfont= dict(size= 11, color= "#E24B4A")
    )
    return fig


def fraud_rate_by_region_chart(fraud_rate_region):
    fraud_rate_region= fraud_rate_region.sort_values("is_fraud", ascending= False)
    fig = px.bar(
        fraud_rate_region,
        x="region", 
        y="is_fraud",
        title="<b> Fraud Rate Per Region</b>",
        color="region", color_discrete_sequence=["#2E5EAA"],
        text= "is_fraud"
    )
    fig.update_layout(
        title_font_color="#E24B4A", height=260, showlegend=False,
        margin=dict(t=40, b=10, l=10, r=10),
        xaxis=dict(showgrid=False, title=None),
        yaxis=dict(range=[2.7, 3.05], ticksuffix="%", title=None),
    )
    fig.update_traces(
        textposition= "outside",
        texttemplate= "%{text:.2f}%",
        textfont= dict(size= 11, color= "#E24B4A")
    )
    return fig


def transaction_split_chart(transaction_split_f):
    label_with_count = [
        f"{label.upper()} ({value:,})"
        for label, value in zip(transaction_split_f.index, transaction_split_f.values)
    ]
    fig = go.Figure(go.Pie(
        labels=label_with_count, values=transaction_split_f.values,
        hole=0.7, textinfo="none",
        marker_colors=["#2E5EAA", "#E8935A", "#1D9E75"]
    ))
    fig.update_traces(domain=dict(x=[0.1, 0.9], y=[0.1, 0.9]))
    fig.update_layout(
        title=dict(text="<b>Transaction Type Split</b>", x=0, y=0.97, font=dict(color="#1D9E75")),
        height=250, margin=dict(t=40, b=10, l=10, r=10),
        annotations=[dict(
            text=f"{transaction_split_f.values.sum():,.0f}txns",
            x=0.5, y=0.5, font_size=10, showarrow=False
        )]
    )
    return fig


def amount_distribution_chart(amount_dist_f):
    amount_dist_f["amount_label"]= amount_dist_f["total_amount"].apply(format_number)

    fig = px.bar(
        amount_dist_f,
        x="amount_cat", 
        y="total_amount",
        title="Amount Distribution",
        color_discrete_sequence=["#2E5EAA"],
        text= "amount_label"
    )
    fig.update_layout(
        height=250, 
        margin=dict(t=40, b=10, l=10, r=10),
        title_font_color="#1D9E75",
        showlegend=False,
        yaxis=dict(title=None, showticklabels= False, showgrid= False),
        xaxis=dict(title=None, showgrid=False),
        bargap=0.1
    )
    fig.update_traces(
        textposition="outside", texttemplate="%{text}",
        textfont=dict(size=11),
    )
    return fig


def transactions_vs_fraud_rate_chart(tran_per_hour, fraud_rate_hour):
    fig = msp(specs=[[{"secondary_y": True}]])
    trace = go.Scatter(
        x=tran_per_hour.index, y=tran_per_hour.values,
        name="Transactions", mode="lines", fill="tozeroy",
        line=dict(shape="spline", width=3, color="#1D9E75"),
        marker=dict(size=7),
        hovertemplate="<b>Hour %{x}:00</b><br>Transactions: %{y}<extra></extra>"
    )
    fig.add_trace(trace, secondary_y=False)

    fraud_trace = go.Scatter(
        x=fraud_rate_hour["hour"], y=fraud_rate_hour["is_fraud"],
        name="Fraud Rate", mode="lines",
        line=dict(shape="spline", width=2, color="#E24B4A"),
        hovertemplate="<b>Hour %{x}:00</b><br>Fraud Rate: %{y:.2f}%<extra></extra>"
    )
    fig.add_trace(fraud_trace, secondary_y=True)

    fig.update_layout(
        title="Transactions V Fraud Rate by Hour",
        title_font=dict(color="#1D9E75"),
        template="plotly_dark", hovermode="x unified",
        legend=dict(orientation="h", y=1.08, x=0.5, xanchor="center"),
        margin=dict(t=40, b=10, l=10, r=10), height=250
    )
    fig.update_yaxes(title="Transactions", title_font_color="#1D9E75",
                      range=[4700, 5200], tickformat="~s", secondary_y=False)
    fig.update_yaxes(title="Fraud Rate", title_font=dict(color="#E24B4A"),
                      ticksuffix="%", secondary_y=True)
    fig.update_xaxes(ticksuffix="h", tickmode="linear", dtick=2)
    return fig


def daily_volume_chart(Trans_daily_f):
    Trans_daily_f = Trans_daily_f.copy()
    Trans_daily_f["count_label"] = Trans_daily_f["count"].apply(format_number)

    fig = px.bar(
        Trans_daily_f, x="day", y="count",
        category_orders={"day": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]},
        title="Transaction Volume By Day",
        color="day", color_discrete_sequence=["#2E5EAA"],
        text="count_label"
    )
    fig.update_traces(
        textposition="outside", texttemplate="%{text}",
        textfont=dict(size=11),
    )
    fig.update_layout(
        height=300, margin=dict(t=40, b=10, l=10, r=10),
        title_font=dict(color="#1D9E75"), showlegend=False,
        yaxis=dict(title=None, showgrid=False, showticklabels= False,
                    range=[0, Trans_daily_f["count"].max() * 1.15]),
        xaxis=dict(title=None, showgrid=False),
    )
    return fig


def fraud_hourly_counts_chart(fraud_hourly_counts_f, threshold_f):
    colors = {
        str(hour): "#E24B4A" if count >= threshold_f else "#2E5EAA"
        for hour, count in zip(fraud_hourly_counts_f["hour"], fraud_hourly_counts_f["count"])
    }
    fig = px.bar(
        fraud_hourly_counts_f, x="hour", y="count",
        title="Fraud Counts By Hour Of Day",
        color=fraud_hourly_counts_f["hour"].astype(str),
        color_discrete_map=colors
    )
    fig.update_layout(
        height=300, margin=dict(t=40, b=10, l=10, r=10),
        title_font=dict(color="#E24B4A"), showlegend=False,
        yaxis=dict(title=None, showgrid=False),
        xaxis=dict(title=None, showgrid=False, dtick=2)
    )
    return fig