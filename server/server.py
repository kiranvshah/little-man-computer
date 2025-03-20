"""This script is responsible for the running of the Flask server and handling of each request."""

from flask import Flask, request, jsonify
import flask_cors
import compile_assembly
import computer as computer_module


app = Flask(__name__)
flask_cors.CORS(app)

@app.post("/api/check")
def post_check():
    """Handles the POST /api/check endpoint.
    Receives user-written assembly code and checks if it is valid."""
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
                "reason": error.args[0],
                "line_number": error.args[1] if len(error.args) > 1 else "unknown"
            })
    return "Expected JSON request", 415

@app.post("/api/compile")
def post_compile():
    """Handles the POST /api/compile endpoint.
    Receives user-written assembly and compiles it to object code and machine code."""
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
                "reason": error.args[0],
                "line_number": error.args[1] or "unknown"
            })
    return "Expected JSON request", 415 # Unsupported Media Type

@app.post("/api/step")
def post_step():
    """Handles the POST /api/step endpoint. Receives state of LMC and runs one
    fetch-decode-execute cycle. Returns list of transfers."""
    if request.is_json:
        req_body = request.get_json()
        try:
            computer = computer_module.Computer(req_body)
            response = jsonify(computer.step())
            return response
        except ValueError as err:
            return f"Error when trying to step: {err.args[0]}", 500
    return "Expected JSON request", 415

@app.post("/api/after-input")
def post_after_input():
    """Handles the POST /api/after-input endpoint. This is called after frontend has been
    collected from user, and updates the LMC accordingly. Returns one transfer."""
    if request.is_json:
        req_body = request.get_json()
        if not (req_body["input"] and req_body["state"]):
            return "Invalid request body. Need input and state.", 400
        computer = computer_module.Computer(req_body["state"])
        response = jsonify(computer.finish_after_input(req_body["input"]))
        return response
    return "Expected JSON request", 415


@app.post("/api/run")
def post_run():
    """Handles the POST /api/run endpoint. Receives state of LMC and runs fetch-decode-execute
    cycles until HLT or INP reached. Returns list of transfers."""
    if request.is_json:
        req_body = request.get_json()
        try:
            computer = computer_module.Computer(req_body)
            response = jsonify(computer.run())
        except ValueError as err:
            return f"Error when trying to run: {err.args[0]}", 500
        return response
    return "Expected JSON request", 415
