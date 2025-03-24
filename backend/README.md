# Backend Service

This is a Flask-based backend service that processes CSV data, generates summaries, answers queries, and creates graphical visualizations using Plotly, OpenAI, and Pandas.

## Features

- **CSV Upload & Summary Generation**
  The `/upload` endpoint accepts a CSV file, reads it into a pandas DataFrame, generates a summary using OpenAI, and stores the data for further processing.

- **Data Details & Graph Visualization**
  The `/details` endpoint uses the dataset description to generate an HTML table and a graph visualization. Graphs are created based on recommendations from OpenAI and rendered using Plotly.

- **Question Answering**
  The `/ask` endpoint accepts a question related to the uploaded CSV data and returns a concise answer generated via OpenAI.

- **Message Processing**
  The `/process_message` endpoint prepends 'hi ' to any provided message and returns the modified message.

## Setup and Running

1. **Dependencies**
   Install the required Python packages listed in `requirements.txt`.

2. **Environment Variables**
   Create a `.env` file in the project root with the following variable:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   ```

3. **Running the Application**
   Start the Flask application by executing:
   ```
   python app.py
   ```

## Endpoints

- **GET /**
  Health check endpoint. Returns a success message indicating the backend is running.

- **GET /details**
  Generates an HTML table and a graph visualization from the dataset description.

- **POST /upload**
  Upload a CSV file using form-data with the key `datafile`. Processes the file, generates a summary, and stores the data.

- **POST /ask**
  Accepts a JSON payload with a key `question` and returns an answer based on the uploaded CSV data.

- **POST /process_message**
  Accepts a JSON payload with a key `message` and returns the message prefixed with "hi".

## Graph Generation

Graph generation logic is implemented in `graph.py` which:
- Recommends an appropriate graph type using OpenAI's chat completion.
- Validates and selects graph types based on dataset characteristics.
- Generates various graphs (Line, Bar, Histogram, Scatterplot, Boxplot, Piechart, Treemap) using Plotly.

## Dependencies

- Flask
- Pandas
- OpenAI Python Client
- Plotly
- Flask-CORS
- python-dotenv

For more information, refer to the source code in `app.py` and `graph.py`.
