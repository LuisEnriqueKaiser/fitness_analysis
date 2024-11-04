import dash
from dash import dcc, html, Input, Output
import plotly.express as px
from dash.dependencies import Input, Output
import pandas as pd


app = dash.Dash(__name__)

# Callback to update the histogram based on the slider input
@app.callback(
    Output('histogram-graph', 'figure'),
    Input('days-slider', 'value')
)
def update_histogram(days):
    # Filter data based on the selected number of days
    subset_df = df[df['date'] > pd.to_datetime('today') - pd.DateOffset(days=days)]
    
    # Create the histogram
    fig = px.histogram(
        subset_df, 
        x='distance_meters', 
        nbins=20,
        title=f"Distance Covered per Day in the Last {days} Days",
        labels={'distance_meters': 'Distance Covered (meters)'}
    )
    
    # Update layout for better aesthetics
    fig.update_layout(
        title={
            'text': f"Histogram of Distance Covered Per Day (Last {days} Days)",
            'y': 0.9,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'
        },
        xaxis_title="Distance (meters)",
        yaxis_title="Frequency",
        template="plotly_white",
        bargap=0.1,
    )
    
    # Customize bar color to dark green
    fig.update_traces(marker_color='#006400', opacity=0.7)
    
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)