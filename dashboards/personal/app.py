"""Personal dashboard starter: replace the placeholder before submission."""
from pathlib import Path
import pandas as pd
from dash import Dash, html


def build_dashboard(data):
    # Replace this entire function with your checked notebook function.
    # Copy its required imports to the top of this file.
    app = Dash(__name__)
    app.layout = html.Div([
        html.H1('Personal dashboard starter'),
        html.P('Replace this placeholder with your four-figure dashboard before submitting.')
    ])
    return app


# After copying your original dataset into data/, replace None below:
# data = pd.read_csv(Path(__file__).resolve().parent / 'data' / 'your_dataset.csv')
# Use the loader appropriate for your actual file format.
data = None
app = build_dashboard(data)
server = app.server

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8055, debug=False)
