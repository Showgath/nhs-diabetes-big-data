import streamlit as st
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler

# Define scaling parameters
scaling_params = {
    "TOTAL_QUANTITY": {"mean": 1000.0, "std": 300.0, "min": 0.0, "max": 5000.0},
    "NIC": {"mean": 50.0, "std": 10.0, "min": 10.0, "max": 100.0},
    "ADQUSAGE": {"mean": 200.0, "std": 50.0, "min": 50.0, "max": 500.0},
    "QUANTITY": {"min": 10.0, "max": 200.0},
    "YEAR": {"min": 2020.0, "max": 2023.0},
    "MONTH": {"min": 1.0, "max": 12.0},
}

# Reverse transformation function
def reverse_transform_data(data):
    """
    Reverse transformations for scaled and log-transformed data.
    :param data: Transformed pandas DataFrame
    :return: Original DataFrame
    """
    if "LOG_ACTUAL_COST" in data.columns:
        data["ACTUAL_COST"] = np.exp(data["LOG_ACTUAL_COST"]) - 1

    if "TOTAL_QUANTITY_scaled" in data.columns:
        params = scaling_params["TOTAL_QUANTITY"]
        data["TOTAL_QUANTITY"] = (data["TOTAL_QUANTITY_scaled"] * params["std"]) + params["mean"]

    if "NIC_scaled" in data.columns:
        params = scaling_params["NIC"]
        data["NIC"] = (data["NIC_scaled"] * params["std"]) + params["mean"]

    if "ADQUSAGE_scaled" in data.columns:
        params = scaling_params["ADQUSAGE"]
        data["ADQUSAGE"] = (data["ADQUSAGE_scaled"] * params["std"]) + params["mean"]

    if "QUANTITY_scaled" in data.columns:
        params = scaling_params["QUANTITY"]
        data["QUANTITY"] = (data["QUANTITY_scaled"] * (params["max"] - params["min"])) + params["min"]

    if "YEAR_scaled" in data.columns:
        params = scaling_params["YEAR"]
        data["YEAR"] = (data["YEAR_scaled"] * (params["max"] - params["min"])) + params["min"]

    if "MONTH_scaled" in data.columns:
        params = scaling_params["MONTH"]
        data["MONTH"] = (data["MONTH_scaled"] * (params["max"] - params["min"])) + params["min"]

    return data

# Dashboard function
def dashboard(data):
    st.title("Machine Learning Dashboard")

    st.header("Original and Transformed Data")
    view_original = st.checkbox("View Original Data")
    
    if view_original:
        original_data = reverse_transform_data(data.copy())
        st.dataframe(original_data)
    else:
        st.dataframe(data)

    st.header("Visualizations")
    st.write("Choose columns to visualize:")
    columns = st.multiselect("Select columns for visualization", data.columns)

    if len(columns) > 1:
        st.line_chart(data[columns])
    elif len(columns) == 1:
        st.bar_chart(data[columns])

    st.header("Search and Filter")
    search_column = st.selectbox("Select a column to search", data.columns)
    search_value = st.text_input("Enter a value to filter")
    if search_value:
        filtered_data = data[data[search_column].astype(str).str.contains(search_value)]
        st.dataframe(filtered_data)

# Main Streamlit app function
def main():
    # Load the transformed dataset
    uploaded_file = st.file_uploader("Upload your transformed CSV file", type=["csv"])
    if uploaded_file is not None:
        data = pd.read_csv(uploaded_file)
        st.write("Data Loaded Successfully!")
        dashboard(data)
    else:
        st.write("Please upload a CSV file to continue.")

if __name__ == "__main__":
    main()
