

# Copyright 2015 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START gae_flex_quickstart]
import logging

import datetime
from flask import Flask, request, session, g, jsonify,  redirect, url_for, abort
# from google.cloud import datastore
# from flask_api import FlaskAPI, status, exceptions

app = Flask(__name__)

def write_to_file(a):
    with open ('sraka.txt','a') as f:
        f.write(a)

def read_from_file():
    with open ('sraka.txt','r') as f:
        return f.read()

@app.route('/')
def hello():
    """Return a friendly HTTP greeting."""
    return 'Hello World!'

@app.route('/<ass>/', methods=['GET', 'POST', 'DELETE'])
def hello1(ass):
    """Return a friendly HTTP greeting."""
    # return f'Get the hell out of here {ass}'
    # return request.json if request.json else 'sraka'
    # ds = datastore.Client()
    if request.method == 'POST':
        # entity = datastore.Entity(key=ds.key('sraka'))
        # entity.update({
        #     'user_ip': ass,
        #     'timestamp': datetime.datetime.utcnow()
        # })
        # ds.put(entity)
        return 'write OK'
    elif request.method == 'DELETE':    
        return str(['sraka'])
    else:
        # qu = ds.query(kind='sraka', order=('-timestamp',))
        return str(['HZZZ'])
    return 'hello {}'.format(ass)


@app.errorhandler(500)
def server_error(e):
    logging.exception('An error occurred during a request.')
    return """
    An internal error occurred: <pre>{}</pre>
    See logs for full stacktrace.
    """.format(e), 500


if __name__ == '__main__':
    # This is used when running locally. Gunicorn is used to run the
    # application on Google App Engine. See entrypoint in app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
# [END gae_flex_quickstart]
