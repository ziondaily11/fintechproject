# config.py

METRIC_CARD_CSS = """
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
"""

LAYOUT_CSS = """
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
"""

METRIC_DELTA_CSS = """
<style>
[data-testid="stMetricDelta"] svg {
    display: none;
}
</style>
"""

LOGO_HEADER_CSS = """
<style>
    div[data-testid="stVerticalBlock"]:has(div.st-key-logo_header) div[data-testid="stHorizontalBlock"] {
        gap: 0rem;
    }
</style>
"""