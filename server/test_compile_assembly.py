from compile_assembly import compile_assembly

def test_user_written_program():
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

// use the DAT command to create to 'variables' called first and second, and set them both to 0
first DAT 000
second DAT 000"""

    expected_result = {
        "compiled_code": [ 
            "00 INP",
            "01 STA 08",
            "02 INP",
            "03 STA 09",
            "04 LDA 08",
            "05 SUB 09",
            "06 OUT",
            "07 HLT",
            "08 DAT 00",
            "09 DAT 00",
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
                # locations 12-98 omitted for brevity
                "99": "000",
            },
            "registers": {
                # all registers start at 0
                "PC": "00",
                "ACC": "000",
                "IR": "0",
                "MAR": "00",
                "MDR": "000",
            },
        },
    }
    assert compile_assembly(user_written_code) == expected_result
