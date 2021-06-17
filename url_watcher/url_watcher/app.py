import re
import string
from urllib.parse import urlparse

import numpy as np
import tensorflow as tf
from flask import Flask
from flask import request
from tensorflow.keras import layers
from tensorflow.keras.layers.experimental.preprocessing import TextVectorization

MODEL_FOLDER = "/home/wawann/PycharmProjects/url_watcher/IA_models/model-best.h5"


def custom_standardization(input_data):
    lowercase = tf.strings.lower(input_data)
    stripped_html = tf.strings.regex_replace(lowercase, "<br />", " ")
    return tf.strings.regex_replace(
        stripped_html, "[%s]" % re.escape(string.punctuation), ""
    )


batch_size = 64
seed = 42
max_features = 20000
embedding_dim = 128
sequence_length = 150

vectorize_layer = TextVectorization(
    standardize=custom_standardization,
    max_tokens=max_features,
    output_mode="int",
    output_sequence_length=sequence_length,
)
raw_test_data = tf.keras.preprocessing.text_dataset_from_directory("./data/combined_set_folder/",
                                                                   batch_size=batch_size)

text_ds = raw_test_data.map(lambda x, y: x, num_parallel_calls=tf.data.AUTOTUNE)
# Let's call `adapt`:
vectorize_layer.adapt(text_ds)

model_loaded = tf.keras.models.load_model(MODEL_FOLDER)

export_model = tf.keras.Sequential([
    vectorize_layer,
    model_loaded,
    layers.Activation("sigmoid")
])


def adapt(url: str):
    return url.ljust(75, " ").replace("", " ")[1: 151]


# ALTERNATIVE MODEL FUNCTION
def url2features(url):
    features = {}
    features['url'] = url
    features['url_length'] = len(url)
    features['hostname_length'] = len(urlparse(url).path)
    features['path_length'] = len(urlparse(url).path)
    try:
        features['fd_length'] = len(urlparse(url).path.split('/')[1])
    except:
        features['fd_length'] = 0
    features['count-'] = url.count('-')
    features['count@'] = url.count('@')
    features['count?'] = url.count('?')
    features['count%'] = url.count('%')
    features['count.'] = url.count('.')
    features['count='] = url.count('=')
    features['count-http'] = url.count('http')
    features['count-https'] = url.count('https')
    features['count-www'] = url.count('www')
    digits = 0
    for i in url:
        if i.isnumeric():
            digits += 1
    features['count-digits'] = digits
    letters = 0
    for i in url:
        if i.isalpha():
            letters += 1
    features['count-letters'] = letters
    urldir = urlparse(url).path
    features['count-dir'] = urldir.count('/')
    match = re.search(
        '(([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\.([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\.([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\.'
        '([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\/)|'  # IPv4
        '((0x[0-9a-fA-F]{1,2})\\.(0x[0-9a-fA-F]{1,2})\\.(0x[0-9a-fA-F]{1,2})\\.(0x[0-9a-fA-F]{1,2})\\/)'  # IPv4 in hexadecimal
        '(?:[a-fA-F0-9]{1,4}:){7}[a-fA-F0-9]{1,4}', url)  # Ipv6
    if match:
        features['use-of-ip'] = -1
    else:
        features['use-of-ip'] = 1
    match = re.search('bit\.ly|goo\.gl|shorte\.st|go2l\.ink|x\.co|ow\.ly|t\.co|tinyurl|tr\.im|is\.gd|cli\.gs|'
                      'yfrog\.com|migre\.me|ff\.im|tiny\.cc|url4\.eu|twit\.ac|su\.pr|twurl\.nl|snipurl\.com|'
                      'short\.to|BudURL\.com|ping\.fm|post\.ly|Just\.as|bkite\.com|snipr\.com|fic\.kr|loopt\.us|'
                      'doiop\.com|short\.ie|kl\.am|wp\.me|rubyurl\.com|om\.ly|to\.ly|bit\.do|t\.co|lnkd\.in|'
                      'db\.tt|qr\.ae|adf\.ly|goo\.gl|bitly\.com|cur\.lv|tinyurl\.com|ow\.ly|bit\.ly|ity\.im|'
                      'q\.gs|is\.gd|po\.st|bc\.vc|twitthis\.com|u\.to|j\.mp|buzurl\.com|cutt\.us|u\.bb|yourls\.org|'
                      'x\.co|prettylinkpro\.com|scrnch\.me|filoops\.info|vzturl\.com|qr\.net|1url\.com|tweez\.me|v\.gd|'
                      'tr\.im|link\.zip\.net',
                      url)
    if match:
        features['short_url'] = -1
    else:
        features['short-url'] = 1

    return features


def url2vec(url):
    features = url2features(url)
    x = []
    x.append(features['hostname_length'])
    x.append(features['path_length'])
    x.append(features['fd_length'])
    x.append(features['count-'])
    x.append(features['count@'])
    x.append(features['count?'])
    x.append(features['count%'])
    x.append(features['count.'])
    x.append(features['count='])
    x.append(features['count-http'])
    x.append(features['count-https'])
    x.append(features['count-www'])
    x.append(features['count-digits'])
    x.append(features['count-letters'])
    x.append(features['count-dir'])
    x.append(features['use-of-ip'])

    return np.asarray(x)


# Server
app = Flask(__name__)


def answer(request_data) -> str:
    print(request_data)
    return str(float(export_model.predict([adapt(request_data["url"])])))
    # ALTERNATIVE
    # x=url2vec(request_data["url"])
    # return str(model_loaded.predict(np.array([x,]))[0][0])


@app.route('/', methods=["POST"])
def api_root():
    return answer(request.json)


@app.route("/test")
def hello():
    return "<h1 style='color:blue'>IT WORKS!</h1>"


def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()


if __name__ == "__main__":
    app.run(host="0.0.0.0")
