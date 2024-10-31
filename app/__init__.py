from flask import Flask
from app.config import Config
from app.db_utils import close_db

app = Flask(__name__)
app.config.from_object(Config)

from app import routes  # import endpointów

@app.teardown_appcontext
def close_connection(exception):
    close_db()
