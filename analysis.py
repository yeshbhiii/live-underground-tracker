import pandas as pd


def average_wait(df):

    if df.empty:
        return 0

    return round(
        df["Minutes_Away"].mean(),
        1
    )


def total_records(history):

    return len(history)


def most_common_line(history):

    if history.empty:
        return "N/A"

    return history["line"].mode()[0]


def most_common_destination(history):

    if history.empty:
        return "N/A"

    return history["destination"].mode()[0]


def average_wait_by_line(history):

    if history.empty:
        return pd.DataFrame()

    result = history.groupby(
        "line"
    )["minutes_away"].mean()

    result = result.reset_index()

    result["minutes_away"] = result[
        "minutes_away"
    ].round(1)

    return result.sort_values(
        "minutes_away",
        ascending=False
    )


def average_wait_by_hour(history):

    if history.empty:
        return pd.DataFrame()

    history = history.copy()

    history["fetched_at"] = pd.to_datetime(
        history["fetched_at"]
    )

    history["hour"] = history[
        "fetched_at"
    ].dt.hour

    result = history.groupby(
        "hour"
    )["minutes_away"].mean()

    result = result.reset_index()

    result["minutes_away"] = result[
        "minutes_away"
    ].round(1)

    return result


def best_time_to_travel(history):

    if history.empty:
        return "N/A", 0

    hourly_data = average_wait_by_hour(
        history
    )

    if hourly_data.empty:
        return "N/A", 0

    best_row = hourly_data.loc[
        hourly_data["minutes_away"].idxmin()
    ]

    return (
        int(best_row["hour"]),
        best_row["minutes_away"]
    )


def delay_status(current_df, history_df):

    if current_df.empty or history_df.empty:

        return {
            "current": 0,
            "historical": 0,
            "difference": 0,
            "status": "No Data"
        }

    current_average = round(
        current_df["Minutes_Away"].mean(),
        1
    )

    historical_average = round(
        history_df["minutes_away"].mean(),
        1
    )

    if historical_average == 0:

        difference = 0

    else:

        difference = round(
            (
                (
                    current_average
                    - historical_average
                )
                / historical_average
            ) * 100,
            1
        )

    if difference < 20:

        status = "🟢 Normal"

    elif difference < 50:

        status = "🟡 Busy"

    else:

        status = "🔴 Heavy Delay"

    return {
        "current": current_average,
        "historical": historical_average,
        "difference": difference,
        "status": status
    }


def weekday_weekend(history):

    if history.empty:
        return pd.DataFrame()

    history = history.copy()

    history["fetched_at"] = pd.to_datetime(
        history["fetched_at"]
    )

    history["hour"] = history[
        "fetched_at"
    ].dt.hour

    history["day_type"] = history[
        "fetched_at"
    ].dt.dayofweek.apply(
        lambda day: "Weekend"
        if day >= 5
        else "Weekday"
    )

    result = history.groupby(
        ["hour", "day_type"]
    )["minutes_away"].mean()

    result = result.reset_index()

    result["minutes_away"] = result[
        "minutes_away"
    ].round(1)

    return result


def reliability_score(current_df, history_df):

    if current_df.empty or history_df.empty:
        return 0

    current_average = current_df[
        "Minutes_Away"
    ].mean()

    historical_average = history_df[
        "minutes_away"
    ].mean()

    if historical_average == 0:
        return 100

    difference = (
        abs(
            current_average
            - historical_average
        )
        / historical_average
    ) * 100

    score = 100 - difference

    if score < 0:
        score = 0

    return round(score, 1)