"""Tests for compile_assembly.py"""

import pytest
from compile_assembly import compile_assembly, check_assembly

with open("../example_assembly_program.txt", "r", encoding="utf-8") as f:
    example_assembly_program = f.read()

def test_check_example_program():
    """Test check_assembly() with the example assembly program."""
    assert check_assembly(example_assembly_program)

def test_assemble_example_program():
    """Test compile_assembly() with the example assembly program."""
    user_written_code = example_assembly_program

    expected_result = {
        "object_code": [ 
            "00 INP",
            "01 ADD 12",
            "02 STA 13",
            "03 BRZ 06",
            "04 BRP 08",
            "05 BRA 10",
            "06 LDA 14",
            "07 BRA 10",
            "08 LDA 15",
            "09 BRA 10",
            "10 OUT",
            "11 HLT",
            "12 DAT 200",
            "13 DAT 999",
            "14 DAT 002",
            "15 DAT 003",
        ],
        "memory_and_registers": {
            "memory": {
                # entire program compiled into memory
                "00": "901",
                "01": "112",
                "02": "313",
                "03": "706",
                "04": "808",
                "05": "610",
                "06": "514",
                "07": "610",
                "08": "515",
                "09": "610",
                "10": "902",
                "11": "000", # note the code for HLT is 000

                # variables (created with DAT):
                "12": "200",
                "13": "999",
                "14": "002",
                "15": "003",

                # remaining memory locations: all start at 000
                "16": "000",
                "17": "000",
                "18": "000",
                "19": "000",
                "20": "000",
                "21": "000",
                "22": "000",
                "23": "000",
                "24": "000",
                "25": "000",
                "26": "000",
                "27": "000",
                "28": "000",
                "29": "000",
                "30": "000",
                "31": "000",
                "32": "000",
                "33": "000",
                "34": "000",
                "35": "000",
                "36": "000",
                "37": "000",
                "38": "000",
                "39": "000",
                "40": "000",
                "41": "000",
                "42": "000",
                "43": "000",
                "44": "000",
                "45": "000",
                "46": "000",
                "47": "000",
                "48": "000",
                "49": "000",
                "50": "000",
                "51": "000",
                "52": "000",
                "53": "000",
                "54": "000",
                "55": "000",
                "56": "000",
                "57": "000",
                "58": "000",
                "59": "000",
                "60": "000",
                "61": "000",
                "62": "000",
                "63": "000",
                "64": "000",
                "65": "000",
                "66": "000",
                "67": "000",
                "68": "000",
                "69": "000",
                "70": "000",
                "71": "000",
                "72": "000",
                "73": "000",
                "74": "000",
                "75": "000",
                "76": "000",
                "77": "000",
                "78": "000",
                "79": "000",
                "80": "000",
                "81": "000",
                "82": "000",
                "83": "000",
                "84": "000",
                "85": "000",
                "86": "000",
                "87": "000",
                "88": "000",
                "89": "000",
                "90": "000",
                "91": "000",
                "92": "000",
                "93": "000",
                "94": "000",
                "95": "000",
                "96": "000",
                "97": "000",
                "98": "000",
                "99": "000",
            },
            "registers": {
                # all registers start at 0
                "PC": "00",
                "ACC": "000",
                "IR": "0",
                "MAR": "00",
                "MDR": "000",
                "CARRY": "0",
            },
        },
    }
    assert compile_assembly(user_written_code) == expected_result

def test_invalid_label():
    """Test check_assembly() and compile_assembly() with a program that has an invalid label
    name."""
    user_written_code = "1nvalidlabel HLT" # begins with number so should throw error
    with pytest.raises(ValueError):
        compile_assembly(user_written_code)
    assert check_assembly(user_written_code) is False

def test_invalid_instruction():
    """Test check_assembly() and compile_assembly() with a program that has an invalid
    instruction mnenomic."""
    user_written_code = """INP
    OUT
    ABC"""
    with pytest.raises(ValueError):
        compile_assembly(user_written_code)
    assert check_assembly(user_written_code) is False
