# Flask application instance 'app' is a member of the 'app' package
from app import app
from app.models import User


# Invoked by 'flask shell' command
@app.shell_context_processor
def make_shell_context():
    return {
        'User': User,
        }