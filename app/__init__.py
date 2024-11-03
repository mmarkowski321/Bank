from flask import Flask
from app.config import Config
from app.routes import initialize_routes
from app.db_utils import close_db

app = Flask(__name__, static_folder='static', template_folder='templates')
app.config.from_object(Config)


initialize_routes(app)


@app.teardown_appcontext
def close_connection(exception):
    close_db()
