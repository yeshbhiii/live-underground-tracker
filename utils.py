import pandas as pd


def format_time(df):

    df = df.copy()

    df["Expected_Arrival"] = pd.to_datetime(
        df["Expected_Arrival"]
    ).dt.strftime("%I:%M:%S %p")

    return df


def sort_arrivals(df):

    df = df.sort_values(
        by="Minutes_Away",
        ascending=True
    ).reset_index(drop=True)

    return df


def filter_line(df, selected_line):

    if selected_line != "All":

        df = df[df["Line"] == selected_line]

    return df


def prepare_history(history):

    history = history.sort_values(
        by="fetched_at",
        ascending=False
    )

    history = history.head(20)

    return history