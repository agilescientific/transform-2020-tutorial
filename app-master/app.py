from io import BytesIO
import base64
import joblib

from flask import Flask, request, render_template, jsonify
from PIL import Image

import utils


app = Flask(__name__)

# Before running with `flask run` we must put ourselves in development mode:
# Mac/Linux: export FLASK_ENV=development
# Windows: set FLASK_ENV=development

CLF = joblib.load('rf.gz')

@app.route('/')
def root():
    """
    (0, 1, 2) The most basic web app in the world.
    """
    # print(request.headers)

    # name = request.args.get('name')

    # vp = float(request.args.get('vp') or 0)
    # rho = float(request.args.get('rho') or 0)
    # return "Impedance: {}".format(vp * rho)
    return "Hello world"

@app.route('/impedance')
def impedance():
    """
    (2) A ridiculously simple calculator.
    """
    vp = float(request.args.get('vp') or 0)
    rho = float(request.args.get('rho') or 0)
    imp = vp * rho
    return "Impedance: {}".format(imp)


@app.route('/hello/<name>')
def hello(name):
    """
    (aside)
    Getting resources from the path. This is good for querying databases:
    path parameters represent entities (tables in your DB, more or less).
    """
    return "Hello {}".format(name)


@app.route('/predict')
def predict():
    """
    (3) Make a prediction from a URL given via GET request.
    
    Using a URL means we can still just accept a string as an arg.

    There's still no human interface.
    """
    url = request.args.get('url')
    img = utils.fetch_image(url)
    result = utils.predict_from_image(CLF, img)

    # Deal with not getting a URL.
    # if url:
    #     img = utils.fetch_image(url)
    #     result = utils.predict_from_image(CLF, img)
    # else:
    #     result = 'Please provide a URL'

    return jsonify(result)

## We can also do that GET from a Python script!

@app.route('/simple', methods=['GET'])
def simple():
    """
    (4a) Render a template. 
    """
    return render_template('simple_page.html')

## You could add an About page as an exercise.

## A real website should also have a Terms page, especially
## if users are uploading anything or creating user instances.
## Check out https://www.termsfeed.com/

@app.route('/form', methods=['GET'])
def form():
    """
    (4b) Make a prediction from a URL given via a GET form.
    """
    url = request.args.get('url')
    if url:
        img = utils.fetch_image(url)
        result = utils.predict_from_image(CLF, img)
        result['url'] = url  # If we add this back, we can display it.
    else:
        result = {}

    return render_template('form.html', result=result)


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    """
    (5) Make a prediction from an image uploaded via a form.

    Bonus: on a mobile device, there will automatically be an option to
    capture via the camera.
    """
    if request.method == 'POST':
        data = request.files['image'].read()
        img = Image.open(BytesIO(data))
        result = utils.predict_from_image(CLF, img)
        result['image'] = base64.b64encode(data).decode('utf-8')
    else:
        result = {}

    return render_template('upload.html', result=result)

## Can you combine both forms into one, letting the user upload an image
## or provide a URL?

@app.route('/plot', methods=["GET", "POST"])
def plot():
    """
    (6) This time we'll also send back a plot of the probabilities.

    We'll use the exact same code as (3), except we'll add the plot.
    """
    if request.method == 'POST':
        data = request.files.get('image').read()
        img = Image.open(BytesIO(data))
        result = utils.predict_from_image(CLF, img)
        result['image'] = base64.b64encode(data).decode('utf-8')

        # This is the only new line.
        result['plot'] = utils.plot(result['probs'], CLF.classes_)
    else:
        result = {}

    return render_template('plot.html', result=result)


@app.route('/post', methods=['POST'])
def post():
    """
    (7) Make a prediction from a URL provided via POST request.
    """
    url = request.json.get('url')
    img = utils.fetch_image(url)
    result = utils.predict_from_image(CLF, img)
    return jsonify(result)


@app.route('/api/v0.1', methods=['POST'])
def api():
    """
    (8) Make a prediction from a base64-encoded image via POST request.

    If accessing the web API from code, you may not have a URL to pass to
    the service, and there is no form for doing a file upload. So we need
    a way to pass the image as data. There are lots of ways to do this; one
    way is to encode as base64.
    """
    data = request.json.get('image')
    if data.startswith('http'):
        img = utils.fetch_image(data)
    else:
        img = Image.open(BytesIO(base64.b64decode(data)))
    result = utils.predict_from_image(CLF, img)
    return jsonify(result)
