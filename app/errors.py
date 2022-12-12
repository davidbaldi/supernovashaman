from flask import render_template
from app import app
# from app import db # What is 'db'?


@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    # Miguel issues a SQLAlchemy session rollback here.
    # Is something similar needed with PyMySQL?
    return render_template('500.html'), 500