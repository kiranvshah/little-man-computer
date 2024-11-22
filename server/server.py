from flask import Flask, request, jsonify
import flask_cors
from compile_assembly import check_assembly


app = Flask(__name__)
flask_cors.CORS(app)

@app.post("/api/check")
def post_check():
    if request.is_json:
        req_body = request.get_json()
        if "uncompiledCode" not in req_body:
            return "Could not find uncompiledCode", 400
        if not isinstance(req_body["uncompiledCode"], str):
            return "uncompiledCode was not string", 400
        valid = check_assembly(req_body["uncompiledCode"])
        response = jsonify({'valid': valid})
        return response
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

@app.post("/api/step")
def post_step():
    if request.is_json:
        req_body = request.get_json()
        # todo: process request
        response = jsonify({'received': True})
        return response
    return "Expected JSON request", 415
