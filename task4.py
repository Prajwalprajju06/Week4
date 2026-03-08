''' Task 4: Business Dashboard with Dash
Objective: Create an interactive dashboard to visualize restaurant business data using Dash. '''

import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import numpy as np
import plotly.express as px

# -----------------------------
# Generate Sample Sales Data
# -----------------------------
np.random.seed(42)

regions = ["North", "South", "East", "West"]
categories = ["Electronics", "Clothing", "Groceries", "Furniture"]
months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]

data = []

for month in months:
    for region in regions:
        for category in categories:
            data.append([
                month,
                region,
                category,
                np.random.randint(10000, 50000),
                np.random.randint(50, 300)
            ])

df = pd.DataFrame(data, columns=["Month", "Region", "Category", "Sales", "Orders"])

# -----------------------------
# Initialize Dash App
# -----------------------------
app = dash.Dash(__name__)
app.title = "Sales Dashboard"

app.layout = html.Div([

    html.H1("Business Sales Dashboard", style={"textAlign": "center"}),

    dcc.Dropdown(
        id="region_filter",
        options=[{"label": r, "value": r} for r in df["Region"].unique()],
        value="North",
        clearable=False
    ),

    html.Div(id="kpi_cards", style={"display": "flex", "justifyContent": "space-around"}),

    dcc.Graph(id="sales_trend"),
    dcc.Graph(id="category_sales")

])

# -----------------------------
# Callback
# -----------------------------
@app.callback(
    [Output("kpi_cards", "children"),
     Output("sales_trend", "figure"),
     Output("category_sales", "figure")],
    [Input("region_filter", "value")]
)
def update_dashboard(selected_region):

    filtered_df = df[df["Region"] == selected_region]

    total_sales = filtered_df["Sales"].sum()
    avg_sales = filtered_df["Sales"].mean()
    total_orders = filtered_df["Orders"].sum()

    # KPI Cards
    kpis = [
        html.Div([
            html.H3("Total Sales"),
            html.H2(f"{total_sales}")
        ]),
        html.Div([
            html.H3("Average Sales"),
            html.H2(f"{round(avg_sales,2)}")
        ]),
        html.Div([
            html.H3("Total Orders"),
            html.H2(f"{total_orders}")
        ])
    ]

    # Sales Trend
    trend = filtered_df.groupby("Month")["Sales"].sum().reset_index()
    fig_trend = px.line(trend, x="Month", y="Sales",
                        title="Monthly Sales Trend")

    # Category Sales
    category = filtered_df.groupby("Category")["Sales"].sum().reset_index()
    fig_category = px.bar(category, x="Category", y="Sales",
                          title="Category-wise Sales")

    return kpis, fig_trend, fig_category


if __name__ == "__main__":
    app.run_server(debug=True)