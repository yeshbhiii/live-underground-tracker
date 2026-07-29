import streamlit as st
import pandas as pd

from datetime import datetime

from pipeline import get_arrivals


st.set_page_config(
    page_title="Live London Underground Tracker",
    page_icon="🚇",
    layout="wide"
)

st.title("🚇 Live London Underground Tracker")

st.write("Real-time arrivals from King's Cross St. Pancras")


if st.button("🔄 Refresh Live Data"):
    st.rerun()


df = get_arrivals()


if df.empty:

    st.error("Unable to connect to TfL API.")

else:

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Total Trains",
            len(df)
        )

    with col2:
        st.metric(
            "Tube Lines",
            df["Line"].nunique()
        )

    with col3:
        st.metric(
            "Next Train",
            f"{df['Minutes_Away'].min()} min"
        )


    st.write(
        "Last Updated:",
        datetime.now().strftime("%d %B %Y %I:%M:%S %p")
    )



    lines = ["All"] + sorted(df["Line"].unique())

    selected_line = st.selectbox(
        "Select Underground Line",
        lines
    )

    if selected_line != "All":

        df = df[df["Line"] == selected_line]


    df["Expected_Arrival"] = pd.to_datetime(
        df["Expected_Arrival"]
    ).dt.strftime("%I:%M:%S %p")
    

    df = df.sort_values(
        by="Minutes_Away",
        ascending=True
    ).reset_index(drop=True)


    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )