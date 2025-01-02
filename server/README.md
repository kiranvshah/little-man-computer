# LMC Backend

The Little Man Computer has a backend written in Python. A Flask server is responsible for handling API requests from the frontend, to do tasks with more complex logic, such as assembling and running programs.

## Setup

In a terminal in the `server` directory:
```sh
python -m venv .venv
pip install -r requirements.txt
```

## Running

In a terminal in the `server` directory:
```sh
./run_server.sh
```

This will run the Flask server.

## Testing

In a terminal in the `server` directory, run `pytest .`.
