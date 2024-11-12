from flask import Flask, request


app = Flask(__name__)

@app.post("/api/compile")
def post_compile():
    print(request.get_data())
    if request.is_json:
        body = request.get_json()
        print(body)
    return "Expected JSON request", 415 # Unsupported Media Type
