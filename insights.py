# insights.py
import math
import streamlit as st


def build_finding_and_recommendation(filtered_data, fraud_count_f, legit_avg_f, fraud_avg_f,
                                      total_transactions_f, fraud_rate_f, peak_hour_f):
    legit_avg_f = 0 if math.isnan(legit_avg_f) else legit_avg_f
    fraud_avg_f = 0 if math.isnan(fraud_avg_f) else fraud_avg_f
    pct_larger = round(((fraud_avg_f - legit_avg_f) / legit_avg_f) * 100, 1) if legit_avg_f != 0 else 0
    legit_count_f = filtered_data[filtered_data["is_fraud"] == 0].shape[0]

    if filtered_data.empty:
        finding_text = "No data available for this selection."
    elif legit_count_f == 0 and fraud_count_f > 0:
        finding_text = (
            f"🔍 Every transaction in this selection is fraudulent — "
            f"there are no legitimate transactions to compare against "
            f"(avg fraud amount: KES {round(fraud_avg_f):,})."
        )
    elif pct_larger > 50:
        finding_text = (
            f"🔍 Big gap: Fraudulent transactions here run {pct_larger}% larger than legitimate ones "
            f"(KES {round(fraud_avg_f):,} vs KES {round(legit_avg_f):,}) — high-value transactions are clearly the target for fraud."
        )
    elif pct_larger > 0:
        finding_text = (
            f"🔍 Fraudulent transactions are modestly larger than legitimate ones in this selection "
            f"({pct_larger}% more — KES {round(fraud_avg_f):,} vs KES {round(legit_avg_f):,})."
        )
    elif fraud_count_f == 0:
        finding_text = "✅ No fraud detected in this selection — all transactions came back clean."
    else:
        finding_text = (
            f"🔍 Interesting reversal: in this selection, fraudulent transactions are actually "
            f"smaller on average than legitimate ones (KES {round(fraud_avg_f):,} vs KES {round(legit_avg_f):,})."
        )

    if filtered_data.empty:
        recommendation_text = "No data available for this selection."
    elif total_transactions_f < 50:
        recommendation_text = "⚠️ Sample size is small for this selection — treat any pattern here as exploratory, not conclusive."
    elif fraud_rate_f > 5:
        recommendation_text = (
            f"🛡️ Recommendation: Fraud rate here is elevated at {round(fraud_rate_f,2)}%. "
            f"Consider requiring additional verification (PIN/OTP) for transactions in this segment, "
            f"especially around hour {peak_hour_f if peak_hour_f is not None else 'N/A'}, where fraud concentrates."
        )
    elif fraud_rate_f > 2:
        recommendation_text = (
            f"🛡️ Recommendation: Fraud rate ({round(fraud_rate_f,2)}%) is moderate. "
            f"Monitor this segment and consider flagging transactions above KES {round(legit_avg_f*2):,} for manual review."
        )
    else:
        recommendation_text = (
            f"✅ Fraud rate is low ({round(fraud_rate_f,2)}%) for this selection — current controls appear effective here."
        )

    return finding_text, recommendation_text


def render_device_split_insight(smart_pct_f, feature_pct_f, device_fraud_rate_f):
    if device_fraud_rate_f.empty:
        st.info("📱 Device split insight: No device data available for this selection.")
        return

    smartphone_rows = device_fraud_rate_f[device_fraud_rate_f["device_type"] == "smartphone"]
    feature_rows = device_fraud_rate_f[device_fraud_rate_f["device_type"] == "feature"]

    parts = [
        f"📱 Device split insight: Feature phones and smartphones are split "
        f"{feature_pct_f}% vs {smart_pct_f}% across this selection."
    ]

    if not smartphone_rows.empty:
        top_smart = smartphone_rows.loc[smartphone_rows["is_fraud"].idxmax()]
        parts.append(
            f"{top_smart['region']} has the highest smartphone fraud rate at {top_smart['is_fraud']}%."
        )

    if not feature_rows.empty:
        low_feature = feature_rows.loc[feature_rows["is_fraud"].idxmin()]
        parts.append(
            f"{low_feature['region']} feature phones are the lowest at {low_feature['is_fraud']}%."
        )

    st.info(" ".join(parts))


def render_hourly_finding(filtered_data, region_filter):
    fraud_by_hour = (
        filtered_data[filtered_data["is_fraud"] == 1]
        .groupby("hour")
        .size()
        .sort_values(ascending=False)
    )

    region_label = ", ".join(region_filter) if region_filter else "all regions"

    if fraud_by_hour.empty:
        st.info(f"🌙 No fraud cases recorded in {region_label} for this selection.")
        return

    top_hour = fraud_by_hour.index[0]
    top_count = fraud_by_hour.iloc[0]

    def fmt_hour(h):
        suffix = "AM" if h < 12 else "PM"
        display_h = h % 12
        display_h = 12 if display_h == 0 else display_h
        return f"{display_h} {suffix}"

    if len(fraud_by_hour) > 1:
        second_hour = fraud_by_hour.index[1]
        second_count = fraud_by_hour.iloc[1]
        peak_text = (
            f"Fraud peaks at {fmt_hour(top_hour)} (hour {top_hour}) with {top_count} cases, "
            f"followed closely by {fmt_hour(second_hour)} (hour {second_hour}) with {second_count}."
        )
    else:
        peak_text = f"Fraud peaks at {fmt_hour(top_hour)} (hour {top_hour}) with {top_count} cases."

    is_odd_hour = top_hour < 6 or top_hour >= 23
    context_note = (
        " This is an unusual time for legitimate activity, making it a strong fraud signal."
        if is_odd_hour else
        " This falls within normal transacting hours, so timing alone isn't a strong signal here."
    )

    recommendation = (
        f" Recommendation: flag transactions in {region_label} around hour {top_hour} "
        f"for additional verification (PIN/OTP), especially given the concentration of {top_count} cases."
    )

    st.info(f"finding🔍 — {region_label}: {peak_text}{context_note}{recommendation}")