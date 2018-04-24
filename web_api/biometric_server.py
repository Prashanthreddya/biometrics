#! /usr/bin/python

import collections
import os

from jinja2 import Environment, FileSystemLoader
from werkzeug.exceptions import HTTPException
from werkzeug.routing import Map, Rule
from werkzeug.wrappers import Request, Response

from extract_features import *
from logi import *

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
            Rule('/biometrics', endpoint='biometrics_api')
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

        if request.method == 'POST' and len(request.form) > 0:
            print "Posting...."

            img_path = request.form.get('imgpath', None)

            id, features = extract_features(img_path)
            (prediction,score) = predict(features)

            name = get_name_from_id(prediction)

            # response_data = json.dumps(response_data)
            # response_data = convert(response_data)

            return self.render_template('index.html',
                                        prediction=prediction,
                                        confidence=score,
                                        name=name)

        else:
            print "Getting...."
            return self.render_template('index.html',
                                        search_hits=search_hits,
                                        query_string=query_string,
                                        hit_count=hit_count,
                                        user_query=user_query)


def create_app():
    server = BiometricServer()
    return server


if __name__ == '__main__':
    from werkzeug.serving import run_simple

    server = BiometricServer()
    run_simple('0.0.0.0', 4004, server, static_files={'/': os.path.dirname(__file__)}, use_debugger=True)
