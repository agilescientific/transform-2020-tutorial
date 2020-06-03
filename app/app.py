from io import BytesIO
import base64

from flask import Flask, request, render_template, jsonify
# from flask import make_response
# from flask_cors import CORS, cross_origin

import joblib
from PIL import Image

import utils


app = Flask(__name__)
# cors = CORS(app)
# app.config['CORS_HEADERS'] = 'Content-Type'

CLF = joblib.load('data/rf.gz')

@app.route('/')
def root():
    """
    (0, 1, 2) The most basic web app in the world.
    """
    vp = float(request.args.get('vp') or 0)
    rho = float(request.args.get('rho') or 0)
    return f"Impedance: {vp * rho}"


@app.route('/predict')
def predict():
    """
    (3) Make a prediction from a URL given via GET request.
    
    Using a URL means we can still just accept a string as an arg.

    There's still no human interface.
    """
    url = request.args.get('url')
    # img = utils.fetch_image(url)
    # result = utils.predict_from_image(CLF, img)

    # Deal with not getting a URL.
    if url:
        img = utils.fetch_image(url)
        result = utils.predict_from_image(CLF, img)
    else:
        result = 'Please provide a URL'

    return jsonify(result)

## We can also do that GET from a Python script!

@app.route('/simple', methods=['GET'])
def simple():
    """
    (4a) Render a template.
    """
    return render_template('simple_page.html')

## You could add an About page as an exercise.

@app.route('/form', methods=['GET', 'POST'])
def form():
    """
    (4b) Make a prediction from a URL given via a form.
    """
    if request.method == 'POST':
        url = request.form.get('url')
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

## Can you combine both forms into one, letting the use upload an image
## or provide a URL?

@app.route('/plot', methods=["GET", "POST"])
def plot():
    """
    (6) This time we'll also send back a plot of the probabilities.

    We'll use the exact same code as (3), except we'll add the plot.
    """
    if request.method == 'POST':
        data = request.files['image'].read()
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


@app.route('/base64', methods=['POST'])
def b64():
    """
    (8) Make a prediction from a base64-encoded image via POST request.

    If accessing the web API from code, you may not have a URL to pass to
    the service, and there is no form for doing a file upload. So we need
    a way to pass the image as data. There are lots of ways to do this; one
    way is to encode 
    """
    data = request.json.get('image')
    img = Image.open(BytesIO(base64.b64decode(data)))
    result = utils.predict_from_image(CLF, img)
    return jsonify(result)


####################################################
# Just ignore all this. We probably won't need it.

@app.route('/api/v1.0', methods=['POST', 'OPTIONS'])
def api():
    """
    Make a prediction from a base64-encoded image via POST request.
    """
    if request.method == "OPTIONS": # CORS preflight
        return _build_cors_preflight_response()
    else:
        print("POST it is!")

    url = request.form.get('url')
    if url is not None:
        img = utils.fetch_image(url)
        result = utils.predict_from_image(CLF, img)
    else:
        result = {}

    print(jsonify(result))

    return _corsify_actual_response(jsonify(result))

# def _build_cors_preflight_response():
#     response = make_response()
#     response.headers.add("Access-Control-Allow-Origin", "*")
#     response.headers.add('Access-Control-Allow-Headers', "*")
#     response.headers.add('Access-Control-Allow-Methods', "*")
#     return response

# def _corsify_actual_response(response):
#     response.headers.add("Access-Control-Allow-Origin", "*")
#     return response
