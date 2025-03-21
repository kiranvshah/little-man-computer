"""Tests for computer.py"""

import pytest
from computer import Computer
from compile_assembly import compile_assembly

SIMPLE_ASSEMBLY_PROGRAM = """inp
sta var
hlt
var dat 000"""
INPUT_VALUE = "123"

@pytest.fixture(name="computer")
def fixture_computer():
    """Create a Computer object with a simple assembly program."""
    return Computer(compile_assembly(SIMPLE_ASSEMBLY_PROGRAM)["memory_and_registers"])

def test_computer_step(computer):
    """Test the Computer.step() method with a simple assembly program."""

    step_result_1 = computer.step()
    assert step_result_1["reached_HLT"] is False
    assert step_result_1["reached_INP"] is True
    assert {
        "start_reg": "PC",
        "end_reg": "MAR",
        "value": "00",
    } in step_result_1["transfers"] # PC -> MAR should be in transfers, with the value 00

    computer.finish_after_input(INPUT_VALUE) # give input

    step_result_2 = computer.step()
    # ACC -> var should be in transfers, with the value 123
    # var will have memory address 03
    assert {
        "start_reg": "ACC",
        "end_mem": "03",
        "value": INPUT_VALUE,
    } in step_result_2["transfers"]
    # ensure the memory location 03 has the input value too
    assert step_result_2.get("memory_and_registers", {})["memory"]["03"] == INPUT_VALUE
    # other assertions
    assert step_result_2["reached_HLT"] is False
    assert step_result_2["reached_INP"] is False

    step_result_3 = computer.step()
    assert step_result_3["reached_HLT"] is True
    assert step_result_3["reached_INP"] is False

def test_computer_run(computer):
    """Test the Computer.run() method with a simple assembly program."""

    run_result_1 = computer.run()
    assert run_result_1[-1]["reached_HLT"] is False
    assert run_result_1[-1]["reached_INP"] is True
    # PC -> MAR should be in first set of transfers, with the value 00
    assert {
        "start_reg": "PC",
        "end_reg": "MAR",
        "value": "00",
    } in run_result_1[0]["transfers"]

    computer.finish_after_input(INPUT_VALUE) # give input

    run_result_2 = computer.run()
    # ACC -> var should be in first set of next transfers, with the value 123
    # var will have memory address 03
    assert {
        "start_reg": "ACC",
        "end_mem": "03",
        "value": INPUT_VALUE,
    } in run_result_2[0]["transfers"]
    # ensure the memory location 03 has the input value too
    assert run_result_2[0]["memory_and_registers"]["memory"]["03"] == INPUT_VALUE
    # other assertions
    assert run_result_2[-1]["reached_HLT"] is True
    assert run_result_2[-1]["reached_INP"] is False
