from flask import Flask, render_template, request, jsonify
import plotly.graph_objects as go
import plotly.utils  # Import plotly.utils for JSON encoding
import numpy as np
import json

app = Flask(__name__)

def create_graph(equations, x_min, x_max):
    # Define x values
    x = np.linspace(x_min, x_max, 500)

    # Create the graph using Plotly
    fig = go.Figure()

    for equation in equations:
        try:
            # Parse and evaluate the equation
            y = eval(equation)
            fig.add_trace(go.Scatter(x=x, y=y, mode='lines', name=f'y = {equation}'))
        except Exception as e:
            return f"Error in equation '{equation}': {e}"

    # Update graph layout
    fig.update_layout(
        xaxis_title="x",
        yaxis_title="y",
        template="plotly_white"
    )

    # Convert the graph to JSON using plotly.utils
    graph_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graph_json

@app.route("/")
def index():
    # Render the initial page
    return render_template("index.html")

@app.route("/update_graph", methods=["POST"])
def update_graph():
    # Get the data from the AJAX request
    data = request.get_json()
    equations = data.get("equations", ["x**2"])  # Expect a list of equations
    x_min = float(data.get("x_min", -10))
    x_max = float(data.get("x_max", 10))

    # Create the graph and return the JSON
    graph_json = create_graph(equations, x_min, x_max)
    return jsonify(graph_json)

if __name__ == "__main__":
    app.run(debug=True)
