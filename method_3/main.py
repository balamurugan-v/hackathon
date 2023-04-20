from gevent import monkey

from messenger import Messenger

monkey.patch_all()
from flask import Flask, Response, render_template, request
from gevent.pywsgi import WSGIServer
import json
import psutil

app = Flask(__name__)


def format_sse(data: str, event=None) -> str:
    print(f"the data is {data}")
    _data = json.dumps(data)
    print(f"the data is {_data}")
    msg = f'data: {_data}\n\n'
    if event is not None:
        msg = f'event: {event}\n{msg}'
    return msg


messenger = Messenger()


@app.route('/new/message', methods=['POST'])
def ping():
    print(request.get_json())
    msg = format_sse(data=request.get_json(), event='message')
    print(f"the new message is {request.get_json()}")
    messenger.publish(msg=msg)
    return {}, 200


@app.route("/")
def render_index():
    return render_template("index.html")


@app.route("/listen")
def listen():
    def stream():
        # num_connections = get_num_connections(5003)
        # print("Number of active connections on port 5000:", num_connections)
        # msg = {'message': 'hello! it is old message'}
        # msg = format_sse(data=msg, event='message')
        # print(f"the old message data is {msg}")
        # messenger.publish(msg=msg)
        messages = messenger.listen()
        print(f"the messages is {messages}")  # returns a queue.Queue
        while True:
            msg = messages.get()
            print(f"msg is {msg}")  # blocks until a new message arrives
            yield msg

    return Response(stream(), mimetype='text/event-stream')


def get_num_connections(port):
    connections = psutil.net_connections()
    num_connections = 0
    for c in connections:
        if c.status == "LISTEN" and c.laddr.port == port:
            num_connections += 1
    return num_connections


# @app.before_request
# def before_request():
#     pass


if __name__ == "__main__":
    app.run(port=5002, debug=True)