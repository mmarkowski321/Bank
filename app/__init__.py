from flask import Flask
from app.config import Config
from app.routes import initialize_routes
from app.db_utils import close_db

app = Flask(__name__, static_folder='static', template_folder='templates')
app.config.from_object(Config)

# Inicjalizacja endpointów
initialize_routes(app)

# Zamykanie połączenia z bazą po zakończeniu żądania
@app.teardown_appcontext
def close_connection(exception):
    close_db()
