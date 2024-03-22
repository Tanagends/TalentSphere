from app import app
from app import db


@app.route('/')
def index():
    """Landing page"""
    return f"Hello talentsphere"

