import streamlit as st
import plotly.express as px

from datetime import datetime

from streamlit_autorefresh import st_autorefresh

from pipeline import get_arrivals

from database import (
    create_database,
    save_arrivals,
    get_history
)

from stations import STATIONS

from utils import (
    format_time,
    sort_arrivals,
    filter_line,
    prepare_history
)

from analysis import (
    average_wait,
    total_records,
    most_common_line,
    most_common_destination,
    average_wait_by_line,
    average_wait_by_hour,
    delay_status,
    best_time_to_travel,
    weekday_weekend,
    reliability_score
)


st.set_page_config(
    page_title="London Underground Analytics",
    page_icon="🚇",
    layout="wide"
)


st_autorefresh(
    interval=60000,
    key="data_refresh"
)


# Sidebar

st.sidebar.title("🚇 Underground Tracker")

selected_station = st.sidebar.selectbox(
    "Choose Station",
    list(STATIONS.keys())
)

if st.sidebar.button("🔄 Refresh Now"):
    st.rerun()

st.sidebar.divider()

st.sidebar.write(
    "Data automatically refreshes every 60 seconds."
)


# Station

station_id = STATIONS[
    selected_station
]


# Get live data

df = get_arrivals(
    station_id
)


# Database

create_database()


if not df.empty:

    save_arrivals(
        df,
        selected_station
    )


# Historical data

history = get_history(
    selected_station
)


# Page title

st.title(
    "🚇 London Underground Analytics"
)

st.write(
    f"Live and historical Underground performance for "
    f"**{selected_station}**"
)


st.write(
    "Last Updated: "
    + datetime.now().strftime(
        "%d %B %Y %I:%M:%S %p"
    )
)


if df.empty:

    st.error(
        "Unable to connect to TfL API."
    )

else:

    # ----------------------------
    # Live Status
    # ----------------------------

    st.divider()

    st.subheader(
        "🚇 Live Status"
    )


    avg_wait = average_wait(
        df
    )

    records = total_records(
        history
    )


    col1, col2, col3, col4 = st.columns(4)


    with col1:

        st.metric(
            "Trains",
            len(df)
        )


    with col2:

        st.metric(
            "Next Train",
            f"{df['Minutes_Away'].min()} min"
        )


    with col3:

        st.metric(
            "Average Wait",
            f"{avg_wait} min"
        )


    with col4:

        st.metric(
            "Records",
            records
        )


    # ----------------------------
    # Performance
    # ----------------------------

    st.divider()

    st.subheader(
        "🚨 Station Performance"
    )


    delay = delay_status(
        df,
        history
    )


    reliability = reliability_score(
        df,
        history
    )


    col1, col2, col3, col4 = st.columns(4)


    with col1:

        st.metric(
            "Current Average",
            f"{delay['current']} min"
        )


    with col2:

        st.metric(
            "Historical Average",
            f"{delay['historical']} min"
        )


    with col3:

        st.metric(
            "Difference",
            f"{delay['difference']}%"
        )


    with col4:

        st.metric(
            "Reliability",
            f"{reliability}%"
        )


    st.write(
        f"Current Status: {delay['status']}"
    )


    # ----------------------------
    # Live Arrivals
    # ----------------------------

    st.divider()

    st.subheader(
        "🚇 Live Arrivals"
    )


    lines = [
        "All"
    ] + sorted(
        df["Line"].unique()
    )


    selected_line = st.selectbox(
        "Filter by Underground Line",
        lines
    )


    display_df = filter_line(
        df,
        selected_line
    )


    display_df = format_time(
        display_df
    )


    display_df = sort_arrivals(
        display_df
    )


    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True
    )


    # ----------------------------
    # Historical Analytics
    # ----------------------------

    st.divider()

    st.subheader(
        "📊 Historical Analytics"
    )


    # Average wait by line

    line_data = average_wait_by_line(
        history
    )


    if not line_data.empty:

        fig1 = px.bar(
            line_data,
            x="line",
            y="minutes_away",
            color="line",
            title=(
                f"Average Wait by Line - "
                f"{selected_station}"
            )
        )

        fig1.update_layout(
            xaxis_title="Underground Line",
            yaxis_title="Average Wait (minutes)"
        )


        st.plotly_chart(
            fig1,
            use_container_width=True
        )


    # Average wait by hour

    hour_data = average_wait_by_hour(
        history
    )


    if not hour_data.empty:

        fig2 = px.line(
            hour_data,
            x="hour",
            y="minutes_away",
            markers=True,
            title=(
                f"Average Wait by Hour - "
                f"{selected_station}"
            )
        )

        fig2.update_layout(
            xaxis_title="Hour of Day",
            yaxis_title="Average Wait (minutes)"
        )


        st.plotly_chart(
            fig2,
            use_container_width=True
        )


    # Weekday vs Weekend

    day_data = weekday_weekend(
        history
    )


    if not day_data.empty:

        fig3 = px.line(
            day_data,
            x="hour",
            y="minutes_away",
            color="day_type",
            markers=True,
            title=(
                f"Weekday vs Weekend Wait Time - "
                f"{selected_station}"
            )
        )

        fig3.update_layout(
            xaxis_title="Hour of Day",
            yaxis_title="Average Wait (minutes)"
        )


        st.plotly_chart(
            fig3,
            use_container_width=True
        )


    # ----------------------------
    # Recommendation
    # ----------------------------

    st.divider()

    st.subheader(
        "🟢 Travel Recommendation"
    )


    best_hour, best_wait = (
        best_time_to_travel(
            history
        )
    )


    if best_hour == "N/A":

        st.info(
            "Not enough historical data to "
            "recommend a travel time yet."
        )

    else:

        col1, col2 = st.columns(2)


        with col1:

            st.metric(
                "Best Hour",
                f"{best_hour}:00"
            )


        with col2:

            st.metric(
                "Average Wait",
                f"{best_wait} min"
            )


        st.write(
            "This recommendation is based on "
            "the historical data collected by "
            "this application."
        )


    # ----------------------------
    # Recent History
    # ----------------------------

    st.divider()

    with st.expander(
        "View Recent History"
    ):

        display_history = prepare_history(
            history
        )


        st.dataframe(
            display_history,
            use_container_width=True,
            hide_index=True
        )