from gevent import monkey

from method_2.messenger import Messenger

monkey.patch_all()
from flask import Flask, Response, render_template, request
from gevent.pywsgi import WSGIServer
import json

app = Flask(__name__)


def format_sse(data: str, event=None) -> str:
    _data = json.dumps(data)
    msg = f'data: {_data}\n\n'
    if event is not None:
        msg = f'event: {event}\n{msg}'
    return msg


# message_queue = []


messenger = Messenger()

# def update_message(msg: str):
#     """
#     This method will update the method list
#     :param msg:
#     :return:
#     """
#     message_queue.append(msg)


@app.route('/new/message', methods=['POST'])
def ping():
    print(request.get_json())
    msg = format_sse(data=request.get_json(), event='message')
    messenger.publish(msg=msg)
    # update_message(msg=msg)
    return {}, 200


@app.route("/")
def render_index():
    return render_template("index.html")


@app.route("/listen")
def listen():
    def stream():
        messages = messenger.listen()  # returns a queue.Queue
        while True:
            msg = messages.get(timeout=10)  # blocks until a new message arrives
            # if message_queue:
            #     print(f" the message_queue is {message_queue}")
            #     msg = message_queue[-1]
            yield msg

    return Response(stream(), mimetype='text/event-stream')


if __name__ == "__main__":
    # app.run(port=5001, debug=True)
    http_server = WSGIServer(("localhost", 5002), app)
    http_server.serve_forever()
