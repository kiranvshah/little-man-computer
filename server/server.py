from flask import Flask, request, jsonify
import flask_cors


app = Flask(__name__)
flask_cors.CORS(app)

@app.post("/api/compile")
def post_compile():
    print(request.get_data())
    print(request.mimetype)
    print(request.is_json)
    # todo: request.is_json appearing as true but request.get_json() throwing 400 error
    # if request.is_json:
    #     print("is json, getting body")
    #     body = request.get_json()
    #     print("body", body)
    response = jsonify({'received': True})
    return response
    return "Expected JSON request", 415 # Unsupported Media Type
