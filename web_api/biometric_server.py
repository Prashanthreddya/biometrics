#! /usr/bin/python

import collections
import os

from jinja2 import Environment, FileSystemLoader
from werkzeug.exceptions import HTTPException
from werkzeug.routing import Map, Rule
from werkzeug.wrappers import Request, Response
from pymongo import MongoClient

from extract_features import *
from logi import *
from config import *
from tqdm import tqdm

import sys
sys.path.append(os.environ['HOME'])


def convert(data):
    if isinstance(data, basestring):
        return str(data)
    elif isinstance(data, collections.Mapping):
        return dict(map(convert, data.iteritems()))
    elif isinstance(data, collections.Iterable):
        return type(data)(map(convert, data))
    else:
        return str(data)


class BiometricServer(object):
    def __init__(self):
        self.url_map = Map([
            Rule('/biometrics', endpoint='biometrics_api'),
            Rule('/view-<any(train, validation):type>', endpoint='view_dataset'),
            Rule('/retrain-model', endpoint='retrain_model'),
            Rule('/run-validation', endpoint='validate_model')
        ])

        template_path = os.path.join(os.path.dirname(__file__), 'templates')
        self.jinja_env = Environment(loader=FileSystemLoader(template_path), autoescape=True)

    def __call__(self, environ, start_response):
        response = self.dispatch_request(Request(environ))
        return response(environ, start_response)

    def dispatch_request(self, request):
        adapter = self.url_map.bind_to_environ(request.environ)
        try:
            endpoint, values = adapter.match()
            return getattr(self, endpoint)(request, **values)
        except HTTPException as e:
            return e

    def render_template(self, template_name, **context):
        t = self.jinja_env.get_template(template_name)
        return Response(t.render(context), mimetype='text/html')

    # application specific code
    def biometrics_api(self, request):
        print
        print "Method: %s" % request.method
        print "Args: %s" % (str(request.form))

        return self.render_template('index.html')

    def view_dataset(self, request, type):
        path = 'static/assets/dataset/' + type
        data = []
        client = MongoClient(host=CONNECTION_STRING)
        db = client.biometric

        if type == 'train':
            collection = db.train_set
        else:
            collection = db.test_set

        for img in tqdm(sorted(os.listdir(path))):
            if img.endswith('.jpg') or img.endswith('.png'):
                imgpath = os.path.join(path,img)
                id = int(img.split('_')[0])
                name = collection.find_one({'sample_class': id})["sample_name"]
                data.append((name, imgpath))

        return self.render_template('ui-grids.html', data=data, type=type)

    def retrain_model(self, request):
        score = train_new_model()

        return self.render_template('complete.html', message="Training complete", score=score*100.0)

    def validate_model(self, request):
        score = validate()

        return self.render_template('complete.html', message="Validation complete", score=score*100.0)


def create_app():
    server = BiometricServer()
    return server


if __name__ == '__main__':
    from werkzeug.serving import run_simple

    server = BiometricServer()
    run_simple('0.0.0.0', 4004, server, static_files={'/': os.path.dirname(__file__)}, use_debugger=True)