import pandas as pd #(version 0.24.2)
import datetime as dt
import dash         #(version 1.0.0)
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import plotly       #(version 4.4.1)
import plotly.express as px


#for choropleth graph

from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate







def init_dashboard(server):

    external_scripts = [
    {
        'src': 'https://code.jquery.com/jquery-3.2.1.slim.min.js',
        'integrity': 'sha256-Qqd/EfdABZUcAxjOkMi8eGEivtdTkh3b65xCZL4qAQA=',
        'crossorigin': 'anonymous'
    },
    {
        'src':'https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.12.9/umd/popper.min.js' ,'integrity':'sha384-ApNbgh9B+Y1QKtv3Rn7W3mgPxhU9K/ScQsAP7hUibX39j7fakFPskvXusvfa0b4Q','crossorigin':'anonymous'
    },
    {
        'src':'https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js','integrity':'sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl', 'crossorigin':'anonymous'
    }
    ]
    external_stylesheets = [
    
    {
        'rel':'stylesheet','href':'https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css','integrity':'sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm','crossorigin':'anonymous'
    }
    ]

    
    """Create a Plotly Dash dashboard."""
    dash_app = dash.Dash(
        server=server,
        routes_pathname_prefix="/dashapp/",external_scripts=external_scripts,
        external_stylesheets=external_stylesheets,
        
        
        
    )

    

    

    dash_app.index_string = '''
    {% extends "layout.html" %}
    <!DOCTYPE html>
    <html>
        <head>
         {%metas%}
            
                

            <title>{%title%}</title>
            {%favicon%}
            {%css%}
                
        </head>
        <body>
        
        <div>
            <header class="site-header">
                <nav class="navbar navbar-expand-md navbar-dark bg-steel fixed-top">
                    <div class="container">
                    <a class="navbar-brand mr-4" href="/">SAP db-dashboard</a>
                    <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarToggle" aria-controls="navbarToggle" aria-expanded="false" aria-label="Toggle navigation">
                        <span class="navbar-toggler-icon"></span>
                    </button>
                    <div class="collapse navbar-collapse" id="navbarToggle">
                        <div class="navbar-nav mr-auto">
                        <a class="nav-item nav-link" href="{{ url_for('/choropleth/') }}">choropleth graph</a>
                        
                        </div>
                        <!-- Navbar Right Side -->
                        <div class="navbar-nav">
                        
                            <a class="nav-item nav-link" href="/choropleth/">choropleth graph</a>
                            
                            <a class="nav-item nav-link" href="/dashapp/">Bar graph</a>
                        
                        </div>
                    </div>
                    </div>
                </nav>
            </header>
            <div>
            {%app_entry%}
            <footer>
                {%config%}
                {%scripts%}
                {%renderer%}
            </footer>
            <div>My Custom footer</div>

            
        </body>
    </html>
    '''


    df = pd.read_csv("Urban_Park_Ranger_Animal_Condition_Response.csv")

    #-------------------------------------------------------------------------------------
    # Drop rows w/ no animals found or calls w/ varied age groups
    df = df[(df['# of Animals']>0) & (df['Age']!='Multiple')]

    # Extract month from time call made to Ranger
    df['Month of Initial Call'] = pd.to_datetime(df['Date and Time of initial call'])
    df['Month of Initial Call'] = df['Month of Initial Call'].dt.strftime('%m')

    # Copy columns to new columns with clearer names
    df['Amount of Animals'] = df['# of Animals']
    df['Time Spent on Site (hours)'] = df['Duration of Response']
    #-------------------------------------------------------------------------------------



    #-------------------------------------------------------------------------------------
    dash_app.layout = html.Div([

           

            html.Div([
                html.Pre(children= "NYC Calls for Animal Rescue",
                style={"text-align": "center", "font-size":"100%", "color":"black"})
            ]),

            html.Div([
                html.Label(['X-axis categories to compare:'],style={'font-weight': 'bold'}),
                dcc.RadioItems(
                    id='xaxis_raditem',
                    options=[
                            {'label': 'Month Call Made', 'value': 'Month of Initial Call'},
                            {'label': 'Animal Health', 'value': 'Animal Condition'},
                    ],
                    value='Animal Condition',
                    style={"width": "50%"}
                ),
            ]),

            html.Div([
                html.Br(),
                html.Label(['Y-axis values to compare:'], style={'font-weight': 'bold'}),
                dcc.RadioItems(
                    id='yaxis_raditem',
                    options=[
                            {'label': 'Time Spent on Site (hours)', 'value': 'Time Spent on Site (hours)'},
                            {'label': 'Amount of Animals', 'value': 'Amount of Animals'},
                    ],
                    value='Time Spent on Site (hours)',
                    style={"width": "50%"}
                ),
            ]),

        html.Div([
            dcc.Graph(id='the_graph')
        ]),

    ])

    #-------------------------------------------------------------------------------------
    @dash_app.callback(
        Output(component_id='the_graph', component_property='figure'),
        [Input(component_id='xaxis_raditem', component_property='value'),
        Input(component_id='yaxis_raditem', component_property='value')]
    )

    def update_graph(x_axis, y_axis):

        dff = df
        # print(dff[[x_axis,y_axis]][:1])

        barchart=px.bar(
                data_frame=dff,
                x=x_axis,
                y=y_axis,
                title=y_axis+': by '+x_axis,
                # facet_col='Borough',
                # color='Borough',
                # barmode='group',
                )

        barchart.update_layout(xaxis={'categoryorder':'total ascending'},
                            title={'xanchor':'center', 'yanchor': 'top', 'y':0.9,'x':0.5,})

        return (barchart)

    return dash_app.server



def init_choropleth(server):
    
    
    dash_app = dash.Dash(
        server=server,
        routes_pathname_prefix="/choropleth/",
        external_stylesheets=[
            "/static/dist/css/styles.css",
            "https://fonts.googleapis.com/css?family=Lato",
        ],
        
        
    )
    dash_app.layout = html.Div([
    html.Br(),
    html.Div([
        dcc.Graph(id='the_graph')
    ]),

    html.Div([
        dcc.Input(id='input_state', type='number', inputMode='numeric', value=2007,
                  max=2007, min=1952, step=5, required=True),
        html.Button(id='submit_button', n_clicks=0, children='Submit'),
        html.Div(id='output_state'),
    ],style={'text-align': 'center'}),

    ])

    #---------------------------------------------------------------
    @dash_app.callback(
        [Output('output_state', 'children'),
        Output(component_id='the_graph', component_property='figure')],
        [Input(component_id='submit_button', component_property='n_clicks')],
        [State(component_id='input_state', component_property='value')]
    )

    def update_output(num_clicks, val_selected):
        if val_selected is None:
            raise PreventUpdate
        else:
            df = px.data.gapminder().query("year=={}".format(val_selected))
            # print(df[:3])

            fig = px.choropleth(df, locations="iso_alpha",
                                color="lifeExp",
                                hover_name="country",
                                projection='natural earth',
                                title='Life Expectancy by Year',
                                color_continuous_scale=px.colors.sequential.Plasma)

            fig.update_layout(title=dict(font=dict(size=28),x=0.5,xanchor='center'),
                            margin=dict(l=60, r=60, t=50, b=50))

            return ('The input value was "{}" and the button has been \
                    clicked {} times'.format(val_selected, num_clicks), fig)

    return dash_app.server



