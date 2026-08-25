import sqlite3
from datetime import datetime

import pandas as pd


DATABASE = "data/arrivals.db"


def create_database():

    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS arrivals(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            station TEXT,
            line TEXT,
            destination TEXT,
            minutes_away INTEGER,
            expected_arrival TEXT,
            fetched_at TEXT
        )
    """)

    connection.commit()
    connection.close()


def save_arrivals(df, station):

    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    for _, row in df.iterrows():

        cursor.execute("""
            INSERT INTO arrivals(
                station,
                line,
                destination,
                minutes_away,
                expected_arrival,
                fetched_at
            )
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            station,
            row["Line"],
            row["Destination"],
            row["Minutes_Away"],
            row["Expected_Arrival"],
            current_time
        ))

    connection.commit()
    connection.close()


def get_history(station):

    connection = sqlite3.connect(DATABASE)

    query = """
    SELECT *
    FROM arrivals
    WHERE station = ?
    ORDER BY fetched_at DESC
    """

    df = pd.read_sql_query(
        query,
        connection,
        params=(station,)
    )

    connection.close()

    return df