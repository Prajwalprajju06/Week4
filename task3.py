''' projects
Business data(restuarants---locations)
insights(assume) columns '''

import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import numpy as np
import plotly.express as px

# -----------------------------
# Generate Sample Business Data
# -----------------------------
np.random.seed(42)

cities = ["Hyderabad", "Bangalore", "Chennai", "Mumbai"]
areas = ["Central", "North", "South", "East", "West"]
cuisines = ["Indian", "Chinese", "Italian", "Fast Food"]

data = {
    "restaurant_id": range(1, 201),
    "restaurant_name": ["Restaurant_" + str(i) for i in range(1, 201)],
    "city": np.random.choice(cities, 200),
    "area": np.random.choice(areas, 200),
    "cuisine": np.random.choice(cuisines, 200),
    "rating": np.round(np.random.uniform(2.5, 5.0, 200), 1),
    "average_cost": np.random.randint(200, 2000, 200),
    "total_orders": np.random.randint(50, 1000, 200),
    "delivery_time": np.random.randint(20, 60, 200)
}

df = pd.DataFrame(data)
df["revenue"] = df["average_cost"] * df["total_orders"]

# -----------------------------
# Initialize Dash App
# -----------------------------
app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Restaurant Business Dashboard", style={"textAlign": "center"}),

    dcc.Dropdown(
        id="city_filter",
        options=[{"label": city, "value": city} for city in df["city"].unique()],
        value="Hyderabad"
    ),

    dcc.Graph(id="revenue_chart"),
    dcc.Graph(id="rating_chart"),
    dcc.Graph(id="cuisine_chart")
])

# -----------------------------
# Callback for Interactivity
# -----------------------------
@app.callback(
    [Output("revenue_chart", "figure"),
     Output("rating_chart", "figure"),
     Output("cuisine_chart", "figure")],
    [Input("city_filter", "value")]
)
def update_dashboard(selected_city):
    filtered_df = df[df["city"] == selected_city]

    # Revenue by Area
    revenue_area = filtered_df.groupby("area")["revenue"].sum().reset_index()
    fig1 = px.bar(revenue_area, x="area", y="revenue",
                  title="Revenue by Area")

    # Rating Distribution
    fig2 = px.histogram(filtered_df, x="rating",
                        title="Rating Distribution")

    # Cuisine Sales
    cuisine_sales = filtered_df.groupby("cuisine")["revenue"].sum().reset_index()
    fig3 = px.pie(cuisine_sales, names="cuisine",
                  values="revenue",
                  title="Cuisine-wise Revenue")

    return fig1, fig2, fig3


if __name__ == "__main__":
    app.run_server(debug=True)