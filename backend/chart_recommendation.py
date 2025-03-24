import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

# Global variables for recommendations
chart_memory = [
    "Graph type Treemap data used: col1 = Common Varieties col2 = None col3 = None",
    "Graph type Treemap data used: col1 = Vegetable ID col2 = None col3 = None"
]

CHART_OPTIONS = ["Line", "Bar", "Histogram", "Scatterplot", "Boxplot", "Piechart", "Treemap"]
invalid_chart_types = []
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
"""
    Recommends an appropriate graph type for the given data using OpenAI's API.

    Parameters:
        data: The input data (e.g., a DataFrame) for which a graph is to be recommended.

    Returns:
        A string representing the recommended graph type.

    The function constructs a prompt with available chart options, calls the OpenAI API,
    validates the recommended graph type using validate_graph_type, and returns the valid graph type.
    """
def get_graph_recommendation(data):
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
    rec = response.choices[0].message.content
    print(rec)
    print("wow")
    if validate_graph_type(data, rec):
        print("I validated " + rec)
        return rec
    elif len(invalid_chart_types) == len(CHART_OPTIONS):
        print("I guess I chose " + invalid_chart_types[0])
        return invalid_chart_types[0]
    else:
        invalid_chart_types.append(rec)
        print(invalid_chart_types)
        return get_graph_recommendation(data)

def validate_graph_type(data, graph_type):
    """
    Validates if the provided graph type meets predefined requirements.
    """
    def get_chart_requirements_inner(chart_type):
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
    requirements = get_chart_requirements_inner(graph_type)
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
    """
    return chart_requirements.get(chart_type, "Invalid Chart Type")

def find_best_columns(data, graph_type):
    """
    Determines the best columns from the data based on graph requirements.
    """
    if graph_type is None:
        print("Graph type is None")
        return None, None
    req = get_chart_requirements(graph_type.lower())
    if req == "Invalid Chart Type":
        return None, None
    prompt = (
        f"Given the data {data} and the graph type {graph_type}, which columns out of these {data.columns} "
        f"should be used based on these requirements: {req}? Do not choose columns that match in the following list: {chart_memory}. "
        "Provide only the column names in a comma-separated format."
    )
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=150
    )
    rec = response.choices[0].message.content.strip()
    if rec.lower() == "none":
        return None, None
    print(rec)
    columns_list = rec.split(", ")
    return columns_list
