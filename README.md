# London Underground Analytics Dashboard

A beginner-level real-time transit analytics project built using Python and the Transport for London API.

The application collects live London Underground arrival data, stores historical observations in SQLite, analyses waiting-time patterns, and presents the results through an interactive Streamlit dashboard.

## Project Overview

Most basic train tracker applications focus on answering:

"When is the next train?"

This project goes a step further by combining live data with historical observations to answer questions such as:

- What trains are arriving now?
- Is the current station performing normally?
- What is the average waiting time?
- Which Underground line has the highest average wait?
- Which hours have longer waiting times?
- Does weekday behaviour differ from weekend behaviour?
- What is the best historical time to travel?

## Features

- Live TfL Underground arrival data
- Multiple station selection
- Underground line filtering
- Historical data collection
- SQLite database
- Average waiting-time analysis
- Average wait by Underground line
- Average wait by hour
- Weekday vs weekend analysis
- Delay detection
- Simple reliability score
- Best-time-to-travel analysis
- Interactive Plotly charts
- Automatic data refresh

## Technology Stack

- Python
- Requests
- Pandas
- SQLite
- Streamlit
- Plotly
- Transport for London API

## Architecture

```text
TfL API
   |
   v
pipeline.py
   |
   v
Pandas Data Cleaning
   |
   v
SQLite Database
   |
   v
analysis.py
   |
   v
Streamlit Dashboard
   |
   v
Plotly Visualizations
```
