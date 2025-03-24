import plotly.express as px
import pandas as pd
from openai import OpenAI


import os
from dotenv import load_dotenv
import plotly.graph_objects as go
import numpy as np

"""
This module handles graph recommendations and generation based on input data.
It uses OpenAI's API to recommend appropriate chart types and Plotly to generate charts.
"""

# Load environment variables from .env file
load_dotenv()

# Initialize OpenAI API key from environment variables
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)


# A list to remember graph types and data columns used in previous charts.
chart_memory = [
    "Graph type Treemap data used: col1 = Common Varieties col2 = None col3 = None",
    "Graph type Treemap data used: col1 = Vegetable ID col2 = None col3 = None"
]

# List of acceptable chart options for recommendation.
CHART_OPTIONS = ["Line", "Bar", "Histogram", "Scatterplot", "Boxplot", "Piechart", "Treemap"]

# List to store invalid chart types encountered during recommendation.
invalid_chart_types = []

# Dictionary containing chart requirements for different chart types.
chart_requirements = {
    "piechart": {
        "Required Columns": ["1 Categorical column that has repeated values that will be calculated later"]
    },
    "treemap": {
        "Required Columns": [
            "1 Categorical column that has repeated values that will be calculated later",
            "choose the column with values that repeat more",
            "try to pick a column that has less that 20 unique values"
        ]
    },
    "Stacked Bar Chart": {
        "Required Columns": ["2 Categorical", "1 Numerical"]
    },
    "bar": {
        "Required Columns": ["1 Categorical", "1 Numerical"]
    },
    "Grouped Bar Chart": {
        "Required Columns": ["2 Categorical", "1 Numerical"]
    },
    "line": {
        "Required Columns": ["1 Numerical (Y)", "1 Categorical (time-based X)"]
    },
    "histogram": {
        "Required Columns": ["1 Numerical"]
    },
    "scatterplot": {
        "Required Columns": ["2 Numerical"]
    },
    "boxplot": {
        "Required Columns": ["1 Numerical", "1 Categorical (optional, for grouping)"]
    },
    "Heatmap": {
        "Required Columns": ["3 Numerical (X, Y, Value for color scale)"]
    },
    "Bubble Chart": {
        "Required Columns": ["3 Numerical (X, Y, Bubble Size)"]
    }
}


def get_graph_recommendation(data):
    """
    Recommends an appropriate graph type for the given data using OpenAI's API.

    Parameters:
        data: The input data (e.g., a DataFrame) for which a graph is to be recommended.

    Returns:
        A string representing the recommended graph type.

    The function constructs a prompt with available chart options, calls the OpenAI API,
    validates the recommended chart type using validate_graph_type, and returns the valid chart type.
    """
    print(data)
    prompt = (
        f"Recommend a graph for this data to best represent the data: {data}. "
        f"Here are your responce options: {CHART_OPTIONS} but you cannot use these options: {invalid_chart_types}. "
        "only use one word from the list as your response"
    )
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=150
    )
    print(response.choices[0].message.content)
    print("wow")
    # Validate the recommended graph type; if valid, return it.
    if validate_graph_type(data, response.choices[0].message.content):
        print("I validated" + response.choices[0].message.content)
        return response.choices[0].message.content
    elif len(invalid_chart_types) == len(CHART_OPTIONS):
        print("I guess I chose" + invalid_chart_types[0])
        return invalid_chart_types[0]
    else:
        invalid_chart_types.append(response.choices[0].message.content)
        print(invalid_chart_types)
        # Recursively try again if validation fails.
        return get_graph_recommendation(data)


def validate_graph_type(data, graph_type):
    """
    Validates if the provided graph_type is appropriate for the given data.

    Parameters:
        data: The input data for which the graph type must be validated.
        graph_type: The graph type recommended by get_graph_recommendation.

    Returns:
        True if the data meets the requirements for the given graph type, False otherwise.

    This function uses an inner helper function get_chart_requirements to fetch
    chart-specific requirements and then asks OpenAI to verify if the data meets these requirements.
    """
    def get_chart_requirements(chart_type):
        chart_type = chart_type.lower()
        print(chart_type)

        if chart_type == "piechart":
            return {
                "Has unique categorical data column": True,
                "Have the ability to create proportions by calculating the categorical data": True,
                "More Than 8 unique categories": False
            }

        elif chart_type in ["treemap", "stacked bar chart"]:
            return {
                "Has unique categorical data column": True,
                "Have the ability to create proportions by calculating the categorical data": True,
                "More Than 8 unique categories": True
            }

        elif chart_type == "bar":
            return {
                "Data Type": "Categorical",
                "Show Proportions": False,
                "Multiple Variables Per Category": False
            }

        elif chart_type == "grouped/stacked bar chart":
            return {
                "Data Type": "Categorical",
                "Show Proportions": False,
                "Multiple Variables Per Category": True
            }

        elif chart_type == "line":
            return {
                "Data Type": "Numerical",
                "Number of Numerical Variables": 1,
                "Exists Over Time or Sequential variable": True
            }

        elif chart_type == "histogram":
            return {
                "Data Type": "Numerical",
                "Number of Numerical Variables": 1,
                "Exists Over Time or Sequential variable": False
            }

        elif chart_type == "scatterplot":
            return {
                "Data Type": "Numerical",
                "Number of Numerical Variables": 2,
                "Compare Relationship": True
            }

        elif chart_type == "boxplot":
            return {
                "Data Type": "Numerical",
                "Number of unique categorical types": 2,
                "Compare Relationship": False
            }

        elif chart_type in ["heatmap", "bubble chart"]:
            return {
                "Data Type": "Numerical",
                "Number of Variables": "More than 2"
            }

        else:
            return "Invalid Chart Type"

    requirements = get_chart_requirements(graph_type)
    print(requirements)

    if requirements == "Invalid Chart Type":
        return False

    prompt = (
        f"Does the data meet these requirements for a {graph_type}: {requirements}? "
        f"Here is the data {data}. Provide a yes or no answer without extra characters, do not put a period."
    )
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=150
    )
    answer = response.choices[0].message.content.strip().lower()
    print("is it valid? " + answer)
    return answer == "yes"


def get_chart_requirements(chart_type):
    """
    Retrieves the predefined chart requirements for a given chart type.

    Parameters:
        chart_type: The type of chart.

    Returns:
        A dictionary containing the required columns or "Invalid Chart Type" if not defined.
    """
    return chart_requirements.get(chart_type, "Invalid Chart Type")


def find_best_columns(data, graph_type):
    """
    Determines the best columns from the data to use for the specified graph type.

    Parameters:
        data: The input data (e.g., a DataFrame).
        graph_type: The type of graph for which columns are to be determined.

    Returns:
        A list of column names that best match the graph's requirements.

    The function uses OpenAI's API to select columns based on the data's columns and chart requirements.
    """
    if graph_type is None:
        print("Graph type is None")
        return None, None
    requirements = get_chart_requirements(graph_type.lower())
    if requirements == "Invalid Chart Type":
        return None, None

    prompt = (
        f"Given the data {data} and the graph type {graph_type}, which columns out of these {data.columns} should be used for the graph "
        f"based on these requirements: {requirements}? Do not choose columns that matches in the following list: {chart_memory}, "
        "Try to pick columns that can lead to intreasting graphs. Provide ONLY the column names comma seperated format "
        "(Ex: column_name, column_name, column_name) infering that if it's only two columns that the format is x y and if there's only one needed just state the name of the column without any other characters in the answer. "
        "do not put the answer in quotes or add a period"
    )
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=150
    )
    print(response.choices[0].message.content)
    columns = response.choices[0].message.content.strip()
    if columns.lower() == "none":
        return None, None
    print(columns)
    columns_list = columns.split(", ")
    return columns_list


def generate_graph(data, graph_type):
    """
    Generates a graph using Plotly based on the provided data and graph type.

    Parameters:
        data: The input data (e.g., a DataFrame) for visualization.
        graph_type: The type of graph to generate.

    Returns:
        A Plotly figure object representing the generated graph, or None if no suitable columns are found.

    This function determines the best columns to use, generates a graph title using OpenAI's API,
    and produces the appropriate chart using Plotly based on the graph type.
    """
    columns = find_best_columns(data, graph_type)
    invalid_chart_types.clear()
    if columns is None or columns[0] is None:
        print("No suitable columns found for the graph type")
        return None

    x_axis = columns[0]
    y_axis = columns[1] if len(columns) > 1 else None
    z_axis = columns[2] if len(columns) > 2 else None

    prompt = (
        f"Generate a title for a graph of {graph_type} type with this data: {data} that has an x-axis of {x_axis} and a y-axis of {y_axis}"
    )
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=150
    )
    title = response.choices[0].message.content.strip()

    # Append the used columns to chart memory for future reference
    chart_memory.append(f"Graph type {graph_type} data used: col1 = {x_axis} col2 = {y_axis} col3 = {z_axis}")
    print("chart mem", chart_memory)

    if graph_type == "Line":
        fig = px.line(data, x=data[x_axis], y=data[y_axis], title=title)
    elif graph_type == "Bar":
        fig = px.bar(data, x=data[x_axis], y=data[y_axis], title=title)
    elif graph_type == "Histogram":
        fig = px.histogram(data, x=data[x_axis], title=title)
    elif graph_type == "Scatterplot":
        # Convert the x_axis and y_axis data to numeric values to avoid type errors
        x_data = pd.to_numeric(data[x_axis], errors='coerce')
        y_data = pd.to_numeric(data[y_axis], errors='coerce')
        # Filter out NaN values to ensure valid inputs for linear regression
        valid_mask = x_data.notna() & y_data.notna()
        x_data_valid = x_data[valid_mask]
        y_data_valid = y_data[valid_mask]
        if len(x_data_valid) < 2:
            slope, intercept = 0, 0
        else:
            slope, intercept = np.polyfit(x_data_valid, y_data_valid, 1)
        line = slope * data[x_axis] + intercept
        fig = px.scatter(data, x=data[x_axis], y=data[y_axis], title=title)
        fig.add_trace(go.Scatter(x=data[x_axis], y=line, mode="lines", name="Trendline", line=dict(color="red")))
    elif graph_type == "Boxplot":
        fig = px.box(data, x=data[x_axis], y=data[y_axis], title=title)
    elif graph_type == "Heatmap":
        fig = px.density_heatmap(data, x=data[x_axis], y=data[y_axis], z=data[z_axis], title=title)
    elif graph_type == "Bubble Chart":
        fig = px.scatter(data, x=data[x_axis], y=data[y_axis], size=data[z_axis], title=title)
    elif graph_type == "Piechart":
        counts = data[x_axis].value_counts()
        fig = px.pie(counts, names=counts.index, values=counts.values, title=title)
    elif graph_type == "Treemap":
        counts = data[x_axis].value_counts().reset_index()
        counts.columns = [x_axis, "count"]
        fig = px.treemap(counts, path=[x_axis], values="count", title=title)
    else:
        fig = px.bar(data, x=data[x_axis], y=data[y_axis], title=title)

    return fig
