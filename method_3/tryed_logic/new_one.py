from flask import Flask, Response, request
from gevent import sleep
from gevent.queue import Queue

app = Flask(__name__)
users = []
messages = []

#
# @app.route('/')
# def index():
#     return 'Server-Sent Events Example'


@app.route('/sse-server/user', methods=['POST'])
def add_user():
    name = request.args.get("name")
    print(f"the name is {name}")
    users.append(name)
    return "User {} added !".format(name)


@app.route('/sse-server/user/message', methods=['POST'])
def send_user_message():
    message = {
        'from': request.form.get('from'),
        'to': request.form.get('to'),
        'text': request.form.get('text')
    }
    messages.append(message)
    return f"Message sent from {message['from']} to {message['to']}"


@app.route('/sse-server/users')
def stream_users():
    name = request.args.get('name')

    def generate():
        while True:
            data = f"data: {', '.join(users)}\n\n"
            yield data
            sleep(1)

    return Response(generate(), mimetype='text/event-stream')


@app.route('/sse-server/user/messages')
def stream_last_message():
    name = request.args.get('name')

    def generate():
        while True:
            last_message = next((msg for msg in reversed(messages) if msg['from'] == name), None)
            if last_message:
                data = f"data: {last_message}\n\n"
            else:
                data = f"data: No messages\n\n"
            yield data
            sleep(1)

    return Response(generate(), mimetype='text/event-stream')


@app.route('/sse-server/user/messages/all')
def stream_messages():
    name = request.args.get('name')

    def generate():
        while True:
            user_messages = [msg for msg in messages if msg['from'] == name]
            data = f"data: {user_messages}\n\n"
            yield data
            sleep(1)

    return Response(generate(), mimetype='text/event-stream')


if __name__ == '__main__':
    app.run(port=4000, debug=True)
