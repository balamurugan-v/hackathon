# import time
#
# from flask import Flask, request, Response
# from flask_sse import sse
# from flask_cors import CORS
# from flask_sse import sse
#
# from method_3.server import SSEService, Message
#
# # from flask_cors import CORS
#
# app = Flask(__name__)
# CORS(app)
# # app.config["REDIS_URL"] = "redis://localhost"
# # app.register_blueprint(sse, url_prefix='/stream')
# users = []
#
#
# def get_users(name):
#     def generate():
#         sequence = 0
#         while True:
#             if name and name.strip():
#                 users_list = get_all_users()
#                 _users = [u for u in users_list if u != name]
#             else:
#                 _users = []
#             sse.publish({"users": _users}, type='user-list-event', event_id=str(sequence))
#             sequence += 1
#             time.sleep(1)
#
#     return Response(generate(), mimetype="text/event-stream")
#
#
# def get_all_users():
#     # Implement your logic to get all users here
#     # This is a dummy function, replace it with actual code to fetch users
#     # For example, you can fetch users from a database or an API
#     return users
#
#
# @app.route('/users/<name>', methods=['GET'])
# def users(name):
#     return get_users(name)
#
#
# @app.route('/sse-server/user', methods=['POST'])
# def stream_users():
#     name = request.args.get('name')
#     return Response(generate_users(name), content_type='text/event-stream')
#
#
# def generate_users(name):
#     def generate():
#         # Replace this with your logic for getting users as a list of strings
#         user_list = get_users_from_service(name)
#         for _user in user_list:
#             yield f'data: {_user}\n\n'
#
#     return generate()
#
#
# def get_users_from_service(name):
#     # Replace this with your logic for getting users as a list of strings
#     # based on the given name parameter
#     users.append(name)
#     # Implement your logic here
#     return users
#
#
# if __name__ == '__main__':
#     app.run(port=4000, debug=True)

from flask import Flask, request
from flask_cors import CORS
from flask_sse import sse

app = Flask(__name__)
CORS(app)
app.register_blueprint(sse, url_prefix='/sse-server')
try:
 from server import SSEService, Message
except ImportError:
    from server import SSEService

sse_service = SSEService()


@app.route('/sse-server/user', methods=['POST'])
def add_user():
    name = request.args['name']
    print(f"the name is {name}")
    sse_service.add_user(name)
    return "User {} added !".format(name)


@app.route('/sse-server/user/message', methods=['POST'])
def send_user_message():
    from server import Message
    message = Message(
        from_=request.json['from'],
        to=request.json['to'],
        message=request.json['text']
    )
    sse_service.send_user_message(message)
    return "Message sent from {} to {}".format(message.from_, message.to)


@app.route('/sse-server/users', methods=['POST'])
def stream_users():
    name = request.args.get('name')
    return sse.stream(sse_service.get_users(name))


@app.route('/sse-server/user/messages', methods=['GET'])
def stream_last_message():
    name = request.args.get('name')
    last_message = sse_service.get_last_user_message(name)
    print(f"the last messages is {last_message.__str__()}")
    return sse.stream(last_message)


@app.route('/sse-server/user/messages/all', methods=['GET'])
def stream_messages():
    name = request.args.get('name')
    all_messages = sse_service.get_all_user_messages(name)
    print(f"the all messages is {all_messages}")
    return all_messages


if __name__ == '__main__':
    app.run(port=4000, debug=True)
