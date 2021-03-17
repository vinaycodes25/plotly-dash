from flask import Flask


app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'

with app.app_context():
        # Import parts of our core Flask app
        from . import routes
        

        # Import Dash application
        from .plotlydash.dashboard import init_dashboard,init_choropleth

        app = init_dashboard(app)
        app = init_choropleth(app)

        # Compile static assets
        

        #return app

#from flaskblog import routes