from flask import Flask

app = Flask(__name__)
from app import views, database

# Remove database session when application shuts down

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()
