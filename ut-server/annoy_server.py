from flask import Flask, request, Response

app = Flask(__name__)

@app.route('/')
def hello():
    return 'hello world'


@app.route("/ann/recall/v2", methods=['POST'])
def proto_recall_v2():
    return Response(request.get_data(), mimetype='application/x-protobuf')