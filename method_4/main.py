from gevent import monkey

from messenger import Messenger

monkey.patch_all()
from flask import Flask, Response, render_template, request
from gevent.pywsgi import WSGIServer
import json
import psutil

app = Flask(__name__)
last_messages = []


def format_sse(data: str, event=None) -> str:
    print(f"the data is {data}")
    _data = json.dumps(data)
    print(f"the data is {_data}")
    msg = f'data: {_data}\n\n'
    if event is not None:
        msg = f'event: {event}\n{msg}'
    return msg


messenger = Messenger()


@app.route('/send_message', methods=['POST'])
def ping():
    print(request.get_json())
    msg = format_sse(data=request.get_json(), event='message')
    print(f"the new message is {request.get_json()}")
    messenger.publish(msg=msg)
    return {}, 200


@app.route("/")
def render_index():
    return render_template("index.html")
@app.route("/message")
def render_message():
    return render_template("message.html")

@app.route("/chat")
def listen():
    def stream():
        messages = messenger.listen()
        print(f"the messages is {messages}")  # returns a queue.Queue
        while True:
            msg = messages.get()
            print(f"msg is {msg}")  # blocks until a new message arrives
            yield msg

    return Response(stream(), mimetype='text/event-stream')


def get_last_messages():
    """
    This function will get the last messages from groups or users
    :return:
    """
    pass


if __name__ == "__main__":
    app.run(port=5004, debug=True)
