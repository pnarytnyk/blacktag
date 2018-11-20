import logging
import os
import json
import datetime
from flask import Flask, request, session, g, jsonify,  redirect, url_for, abort
import urllib
# from flask_api import FlaskAPI, status, exceptions

shook=os.environ.get('s_hc',None)
s_toc=os.environ.get('s_toc',None)


app = Flask(__name__)

def parse_args(a):
    a=a.decode('utf-8')
    a=a.split('&')
    a=dict(list(map(lambda x: x.split('='), a)))
    b=dict(a)
    if b.get('text', None):
        b['text'] = b['text'].split('+')
    b['response_url'] = urllib.parse.unquote(b['response_url'])
    return b

def write_to_file(a):
    with open ('sraka.txt','a') as f:
        f.write(a)

def read_from_file():
    with open ('sraka.txt','r') as f:
        return f.read()

# @app.route('/')
# def hello():
#     """Return a friendly HTTP greeting."""
#     return 'Hello World!'

def send_message(shook=shook):
    some_url = f"https://picsum.photos/1000/100/?image={random.randint(1,1050)}"
    payload = {
          "attachments": [
            {
              "link_names": 1,
              "fallback": "Whos turn will it be today? \nFind out in a message!",
              "color": "#36a64f",
              "title": f"List :D",
              # "image_url": some_url,
              "channel": 'D6V49LV1S'
            }
          ]
        }
    response = requests.post(
        shook, data=json.dumps(payload),
        headers={'Content-Type': 'application/json'}
    )
    return response


@app.route('/', methods=['POST', 'DELETE'])
def hello1():
    """Return a friendly HTTP greeting."""
    # return f'Get the hell out of here {ass}'
    # return request.json if request.json else 'sraka'
    # ds = datastore.Client()
    if request.method == 'POST':
        params = parse_args(request.get_data())
        if params.get('token',None) == s_toc:
            send_message(shook=params['response_url'])


        return str(request.args) + '\n\n'+str(request.view_args) + '\n\n'+ '\n\n' + str(request.get_data()) + "\n\n" + str(request.parameter_storage_class)+ "\n\n" + str(request.parameter_storage_class)+ "\n\n"+ str(request.headers)

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
