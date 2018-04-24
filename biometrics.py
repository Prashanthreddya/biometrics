#! /usr/bin/python

import sys
import os
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "../"))

try:
    import web_api.biometric_server as biometric_server
    application = biometric_server.create_app()
except Exception, e:
    print e
