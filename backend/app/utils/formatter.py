def format_value(value: float) -> float:
    """Round to 2 decimal places."""
    return round(float(value), 2)

def format_value_billions(value: float) -> str:
    """Convert large USD values to readable string e.g. $1.23B"""
    if value >= 1_000_000_000:
        return f"${value / 1_000_000_000:.2f}B"
    elif value >= 1_000_000:
        return f"${value / 1_000_000:.2f}M"
    elif value >= 1_000:
        return f"${value / 1_000:.2f}K"
    return f"${value:.2f}"

def format_trend(trend_dict: dict) -> list:
    """Convert year->value dict to a list frontend can use for charts."""
    return [
        {"year": int(year), "value_usd": round(float(val), 2)}
        for year, val in sorted(trend_dict.items())
    ]

def format_rank_list(data: dict, value_key: str = "value") -> list:
    """Convert a grouped series to a ranked list."""
    return [
        {"rank": i + 1, "name": k, value_key: round(float(v), 2)}
        for i, (k, v) in enumerate(data.items())
    ]