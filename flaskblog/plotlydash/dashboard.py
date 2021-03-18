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

#for third init_two_pie_charts

import dash_bootstrap_components as dbc







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



def init_two_pie_charts(server):
    app = dash.Dash(__name__,server=server,
        routes_pathname_prefix="/two_pie_charts/",external_stylesheets=[dbc.themes.DARKLY])

    df = pd.read_csv("https://raw.githubusercontent.com/Coding-with-Adam/Dash-by-Plotly/master/Bootstrap/Berlin_crimes.csv")
    df = df.groupby('District')[['Street_robbery', 'Drugs']].median()

    app.layout = html.Div([
            dbc.Row(dbc.Col(html.H3("Our Beautiful App Layout"),
                            width={'size': 6, 'offset': 3},
                            ),
                    ),
            dbc.Row(dbc.Col(html.Div("One column is all we need because there ain't no room for the "
                                    "both of us in this raggedy town"),
                            width=4
                            )
                    ),
            dbc.Row(
                [
                    dbc.Col(dcc.Dropdown(id='c_dropdown', placeholder='last dropdown',
                                        options=[{'label': 'Option A', 'value': 'optA'},
                                                {'label': 'Option B', 'value': 'optB'}]),
                            width={'size': 3, "offset": 2, 'order': 3}
                            ),
                    dbc.Col(dcc.Dropdown(id='a_dropdown', placeholder='first dropdown',
                                        options=[{'label': 'Option A', 'value': 'optA'},
                                                {'label': 'Option B', 'value': 'optB'}]),
                            width={'size': 4, "offset": 1, 'order': 1}
                            ),
                    dbc.Col(dcc.Dropdown(id='b_dropdown', placeholder='middle dropdown',
                                        options=[{'label': 'Option A', 'value': 'optA'},
                                                {'label': 'Option B', 'value': 'optB'}]),
                            width={'size': 2,  "offset": 0, 'order': 2}
                            ),
                ], no_gutters=True
            ),
            dbc.Row(
                [
                    dbc.Col(dcc.Graph(id='pie_chart1', figure={}),
                            width=8, lg={'size': 6,  "offset": 0, 'order': 'first'}
                            ),
                    dbc.Col(dcc.Graph(id='pie_chart2', figure={}),
                            width=4, lg={'size': 6,  "offset": 0, 'order': 'last'}
                            ),
                ]
            )
    ])


    @app.callback(
        [Output('pie_chart1', 'figure'),
        Output('pie_chart2', 'figure')],
        [Input('a_dropdown', 'value'),
        Input('b_dropdown', 'value'),
        Input('c_dropdown', 'value')]
    )
    def update_graph(dpdn_a, dpdn_b, dpdn_c):
        dff = df[:200]
        if dpdn_a is None or dpdn_b is None or dpdn_c is None:
            pie_fig = px.pie(dff, names=dff.index, values='Street_robbery', title='Street Robbery Berlin')\
                .update_layout(showlegend=False, title_x=0.5).update_traces(textposition='inside',  textinfo='label+percent')
            pie_fig2 = px.pie(dff, names=dff.index, values='Drugs', title='Drugs Berlin')\
                .update_layout(showlegend=False, title_x=0.5).update_traces(textposition='inside', textinfo='label+percent')
            return pie_fig, pie_fig2
        else:
            raise dash.exceptions.PreventUpdate

    return app.server

def init_neat_dash_board(server):#video 3
    df = pd.read_csv("https://raw.githubusercontent.com/Coding-with-Adam/Dash-by-Plotly/master/Bootstrap/Berlin_crimes.csv")

    app = dash.Dash(__name__,server=server,routes_pathname_prefix="/neat_dash_board/",external_stylesheets=[dbc.themes.BOOTSTRAP]) # https://bootswatch.com/default/

    modal = html.Div(
        [
            dbc.Button("Add comment", id="open"),

            dbc.Modal([
                dbc.ModalHeader("All About Berlin"),
                dbc.ModalBody(
                    dbc.Form(
                        [
                            dbc.FormGroup(
                                [
                                    dbc.Label("Name", className="mr-2"),
                                    dbc.Input(type="text", placeholder="Enter your name"),
                                ],
                                className="mr-3",
                            ),
                            dbc.FormGroup(
                                [
                                    dbc.Label("Email", className="mr-2"),
                                    dbc.Input(type="email", placeholder="Enter email"),
                                ],
                                className="mr-3",
                            ),
                            dbc.FormGroup(
                                [
                                    dbc.Label("Comment", className="mr-2"),
                                    dbc.Input(type="text", placeholder="Enter comment"),
                                ],
                                className="mr-3",
                            ),
                            dbc.Button("Submit", color="primary"),
                        ],
                        inline=True,
                    )
                ),
                dbc.ModalFooter(
                    dbc.Button("Close", id="close", className="ml-auto")
                ),

            ],
                id="modal",
                is_open=False,    # True, False
                size="xl",        # "sm", "lg", "xl"
                backdrop=True,    # True, False or Static for modal to not be closed by clicking on backdrop
                scrollable=True,  # False or True if modal has a lot of text
                centered=True,    # True, False
                fade=True         # True, False
            ),
        ]
    )

    alert = dbc.Alert("Please choose Districts from dropdown to avoid further disappointment!", color="danger",
                    dismissable=True),  # use dismissable or duration=5000 for alert to close in x milliseconds

    image_card = dbc.Card(
        [
            dbc.CardBody(
                [
                    html.H4("The Lovely City of Berlin", className="card-title"),
                    dbc.CardImg(src="/assets/berlinwall.jpg", title="Graffiti by Gabriel Heimler"),
                    html.H6("Choose Berlin Districts:", className="card-text"),
                    html.Div(id="the_alert", children=[]),
                    dcc.Dropdown(id='district_chosen', options=[{'label': d, "value": d} for d in df["District"].unique()],
                                value=["Lichtenberg", "Pankow", "Spandau"], multi=True, style={"color": "#000000"}),
                    html.Hr(),
                    modal
                ]
            ),
        ],
        color="light",
    )

    graph_card = dbc.Card(
        [
            dbc.CardBody(
                [
                    html.H4("Graffiti in Berlin 2012-2019", className="card-title", style={"text-align": "center"}),
                    dbc.Button(
                        "About Berlin", id="popover-bottom-target", color="info"
                    ),
                    dbc.Popover(
                        [
                            dbc.PopoverHeader("All About Berlin:"),
                            dbc.PopoverBody(
                                "Berlin (/bɜːrˈlɪn/; German: [bɛʁˈliːn] is the capital and largest city of Germany by both area and population. Its 3,769,495 (2019) inhabitants make it the most populous city proper of the European Union. The city is one of Germany's 16 federal states. It is surrounded by the state of Brandenburg, and contiguous with Potsdam, Brandenburg's capital. The two cities are at the center of the Berlin-Brandenburg capital region, which is, with about six million inhabitants and an area of more than 30,000 km2, Germany's third-largest metropolitan region after the Rhine-Ruhr and Rhine-Main regions. (Wikipedia)"),
                        ],
                        id="popover",
                        target="popover-bottom-target",  # needs to be the same as dbc.Button id
                        placement="bottom",
                        is_open=False,
                    ),
                    dcc.Graph(id='line_chart', figure={}),

                ]
            ),
        ],
        color="light",
    )


    # *********************************************************************************************************
    app.layout = html.Div([
        dbc.Row([dbc.Col(image_card, width=3), dbc.Col(graph_card, width=8)], justify="around")
    ])
    # *********************************************************************************************************


    @app.callback(
        Output("popover", "is_open"),
        [Input("popover-bottom-target", "n_clicks")],
        [State("popover", "is_open")],
    )
    def toggle_popover(n, is_open):
        if n:
            return not is_open
        return is_open


    @app.callback(
        [Output("line_chart", "figure"),
        Output("the_alert", "children")],
        [Input("district_chosen", "value")]
    )
    def update_graph_card(districts):
        if len(districts) == 0:
            return dash.no_update, alert
        else:
            df_filtered = df[df["District"].isin(districts)]
            df_filtered = df_filtered.groupby(["Year", "District"])[['Graffiti']].median().reset_index()
            fig = px.line(df_filtered, x="Year", y="Graffiti", color="District",
                        labels={"Graffiti": "Graffiti incidents (avg)"}).update_traces(mode='lines+markers')
            return fig, dash.no_update


    @app.callback(
        Output("modal", "is_open"),
        [Input("open", "n_clicks"), Input("close", "n_clicks")],
        [State("modal", "is_open")],
    )
    def toggle_modal(n1, n2, is_open):
        if n1 or n2:
            return not is_open
        return is_open

    return app.server
