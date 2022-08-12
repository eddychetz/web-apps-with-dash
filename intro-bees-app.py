#!/usr/bin/env python
# coding: utf-8

# # Web App with DASH

# In[2]:


from dash import *
from jupyter_dash import JupyterDash
import pandas as pd
import plotly.express as px

JupyterDash.infer_jupyter_proxy_config()


# In[3]:


app = dash.Dash(__name__)


# In[4]:


df = pd.read_csv("./intro_bees.csv")
df.head()


# In[5]:


# Import and clean data (importing csv into pandas)

df.columns = df.columns.str.lower().str.replace(" ", "_")
df = df.groupby(["state", "ansi", "affected_by", "year","state_code"])[["pct_of_colonies_impacted"]].mean()
df.reset_index(inplace=True)
df[df["affected_by"] == "Varroa_mites"].head()


# In[9]:


# App layout

app.layout = html.Div(
    [
        # Add graph
        html.H1("Web Application Dashboards with Dash", style={"text-align":"center"}),
        
        # Dropdown to select year
        dcc.Dropdown(id="select_year",
                    options = [
                        {"label":"2015","value": 2015},
                        {"label":"2016","value": 2016},
                        {"label":"2017","value": 2017},
                        {"label":"2018","value": 2018}],
                     multi=False,
                     value=2015,
                     style={"width":"40%"}
                    ),
        #
        html.Div(id="output_container", children=[]),
        html.Br(),
        
        dcc.Graph(id="my_bee_map", figure={}),
        dcc.Graph(id="my_bar_map", figure={})
    ]
)


# In[10]:


# Connect the Plotly graphs with Dash components
@app.callback(
    [Output(component_id="output_container", component_property="children"),
     Output(component_id="my_bee_map", component_property="figure"),
     Output(component_id="my_bar_map", component_property="figure")],
    
    [Input(component_id="select_year", component_property="value")]
)

def update_graph(option_selected):
    print(option_selected)
    print(type(option_selected))
    
    container = " The year chosen was:{}".format(option_selected)
    
    dff = df.copy()
    dff = dff[dff["year"] == option_selected]
    dff = dff[dff["affected_by"] == "Varroa_mites"]
    
    # Plotly express
    fig1 = px.choropleth(
        data_frame=dff,
        locationmode="USA-states",
        locations="state_code",
        scope="usa",
        color="pct_of_colonies_impacted",
        color_continuous_scale=px.colors.sequential.YlOrRd,
        labels={"Pct of Colonies Impacted": "% of Bee Colonies"},
        template="plotly_dark")
    fig2 = px.bar(
        x="state",
        y="pct_of_colonies_impacted",
        data_frame=dff)
    return container, fig1, fig2


# In[11]:


if __name__ == "__main__":
    app.run_server(debug=False)

