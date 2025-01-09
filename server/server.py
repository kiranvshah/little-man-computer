"""This script is responsible for the running of the Flask server and handling of each request."""

from flask import Flask, request, jsonify
import flask_cors
import compile_assembly
import computer as computer_module


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

        try:
            compile_assembly.compile_assembly(req_body["uncompiledCode"])
            return jsonify({"valid": True})

        except ValueError as error:
            return jsonify({
                "valid": False,
                "reason": error.args[1],
                "line_number": error.args[0] or "unknown"
            })
    return "Expected JSON request", 415

@app.post("/api/compile")
def post_compile():
    if request.is_json:
        req_body = request.get_json()
        # todo: ALL RESPONSES SHOULD BE JSON

        if "uncompiledCode" not in req_body:
            return "Could not find uncompiledCode", 400
        if not isinstance(req_body["uncompiledCode"], str):
            return "uncompiledCode was not string", 400

        try:
            compiled_assembly = compile_assembly.compile_assembly(req_body["uncompiledCode"])
            return jsonify({"valid": True, "result": compiled_assembly})
        except ValueError as error:
            return jsonify({
                "valid": False,
                "reason": error.args[1],
                "line_number": error.args[0] or "unknown"
            })
    return "Expected JSON request", 415 # Unsupported Media Type

@app.post("/api/step")
def post_step():
    if request.is_json:
        req_body = request.get_json()
        print(req_body)
        computer = computer_module.Computer(req_body)
        response = jsonify(computer.step()) # todo: catch errors
        return response
    return "Expected JSON request", 415

@app.post("/api/after-input")
def post_after_input():
    if request.is_json:
        req_body = request.get_json()
        if not (req_body["input"] and req_body["state"]):
            return "Invalid request body. Need input and state.", 400
        # todo: process request
        computer = computer_module.Computer(req_body["state"])
        response = jsonify(computer.finish_after_input(req_body["input"]))
        return response
    return "Expected JSON request", 415


@app.post("/api/run")
def post_run():
    if request.is_json:
        req_body = request.get_json()
        # todo: process request
        response = jsonify({'received': True})
        return response
    return "Expected JSON request", 415
