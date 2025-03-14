"""Tests for compile_assembly.py"""

import pytest
from compile_assembly import compile_assembly

def test_subtraction_program():
    """Test compile_assembly() with a program that subtracts two numbers."""
    user_written_code = """// store an input
// at position first
INP
STA first
// store an input at
// position second
INP
STA second
// load the first value
LDA first
// subtract the
// second
SUB second
// output the difference
// and halt execution
OUT
HLT

// use the DAT instruction to create two 'variables' called first and second, and set them both to 0
first DAT 000
second DAT 000"""

    expected_result = {
        "object_code": [ 
            "00 INP",
            "01 STA 08",
            "02 INP",
            "03 STA 09",
            "04 LDA 08",
            "05 SUB 09",
            "06 OUT",
            "07 HLT",
            "08 DAT 000",
            "09 DAT 000",
        ],
        "memory_and_registers": {
            "memory": {
                # entire program compiled into memory
                "00": "901",
                "01": "308",
                "02": "901",
                "03": "309",
                "04": "508",
                "05": "209",
                "06": "902",
                "07": "000", # note the code for HLT is 000

                # variables (created with DAT):
                "08": "000", # this is the `first` variable
                "09": "000", # this is the `second` variable

                # remaining memory locations: all start at 000
                "10": "000",
                "11": "000",
                "12": "000",
                "13": "000",
                "14": "000",
                "15": "000",
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
    user_written_code = "1nvalidlabel HLT"
    with pytest.raises(ValueError):
        compile_assembly(user_written_code)
