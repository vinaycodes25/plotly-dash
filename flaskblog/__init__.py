from flask import Flask


app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'

with app.app_context():
        # Import parts of our core Flask app
        from . import routes
        

        # Import Dash application
        from .plotlydash.dashboard import init_dashboard,init_choropleth,init_two_pie_charts,init_neat_dash_board

        app = init_dashboard(app)
        app = init_choropleth(app)
        app = init_two_pie_charts(app)
        app  = init_neat_dash_board(app)

        # Compile static assets
        

        #return app

#from flaskblog import routes