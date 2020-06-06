from flask import Flask

app = Flask(__name__)

# Before running with `flask run` we must put ourselves in development mode:
# Mac/Linux: export FLASK_ENV=development
# Windows: set FLASK_ENV=development

@app.route('/')
def root():
    """
    (0) The most basic web app in the world.
    """
    return "Hello world!"
