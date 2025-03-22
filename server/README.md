# LMC Backend

The Little Man Computer has a backend written in Python. A Flask server is responsible for handling API requests from the frontend, to do tasks with more complex logic, such as assembling and running programs.

## Structure

- `compile_assembly.py` contains the logic for processing user-written assembly code into cleaned-up assembly code (known as object code), and also the contents of the LMC's memory and registers before running (machine code).
- `test_compile_assembly.py` contains unit tests for `compile_assembly.py`.
- `computer.py` contains the logic for running programs, including the fetch-decode-execute cycle.
- `test_computer.py` contains unit tests for `computer.py`.
- `server.py` contains the code for the Flask server.
- `run_server.sh` is a script that runs the Flask server.

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

> [!NOTE]  
> The port that the server runs on will need to be opened up to outside traffic (made public) if the requests are being made from a different machine, i.e. if the website is being accessed from a different machine.

## Testing

In a terminal in the `server` directory, run `pytest .`.
