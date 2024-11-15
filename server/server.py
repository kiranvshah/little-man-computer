from flask import Flask, request, jsonify
import flask_cors


app = Flask(__name__)
flask_cors.CORS(app)

@app.post("/api/check")
def post_check():
    if request.is_json:
        req_body = request.get_json()
        print(req_body, type(req_body))
        # todo: handle request - check code
        valid = True
        response = jsonify({'valid': valid})
    return "Expected JSON request", 415

@app.post("/api/compile")
def post_compile():
    if request.is_json:
        req_body = request.get_json()
        print(req_body)
        # todo: process request
        response = jsonify({'received': True})
        return response
    return "Expected JSON request", 415 # Unsupported Media Type
