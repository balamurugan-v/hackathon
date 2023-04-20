from gevent import monkey

monkey.patch_all()
from flask import Flask, Response, render_template, stream_with_context
from gevent.pywsgi import WSGIServer
import json
import time

app = Flask(__name__)


##############################
@app.route("/")
def render_index():
    return render_template("index.html")


##############################
@app.route("/listen")
def listen():
    def respond_to_client():
        counter = 1
        while True:
            with open("color.txt", "r") as f:
                color = f.read()
                print(f"****************** the color is {color}")
            if color != "white":
                counter += 1
                print(counter)
                _data = json.dumps({"color": color, "counter": counter, "message": str(counter)})
                return f"id: 1\ndata: {_data}\nevent: online\n\n"
            time.sleep(1)

    return Response(respond_to_client(), mimetype='text/event-stream')


##############################
if __name__ == "__main__":
    # app.run(port=80, debug=True)
    http_server = WSGIServer(('localhost', 5001), app)
    http_server.serve_forever()
