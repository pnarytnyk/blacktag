import logging
import os
import datetime
from flask import Flask, request, session, g, jsonify,  redirect, url_for, abort
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
        print(dir(request))
        # print(request.headers)
        # with open('sraka.txt','w+') as f:
        #     f.write('jopen')

        # entity = datastore.Entity(key=ds.key('sraka'))
        # entity.update({
        #     'user_ip': ass,
        #     'timestamp': datetime.datetime.utcnow()
        # })
        # ds.put(entity)
        # return str(dir(request))
        return str(request.args) + '\n\n'+ '\n\n' + str(request.data) + "\n\n" + str(request.headers)

    elif request.method == 'DELETE':
        # with open('sraka.txt','w+') as f:
        #     f.write('')    
        return str(['written \'\''])
    else:
        # qu = ds.query(kind='sraka', order=('-timestamp',))
        # with open('sraka.txt','r') as f:
        #     s=f.read()
        return 's'
    return 'hello {}'.format("ass")


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
