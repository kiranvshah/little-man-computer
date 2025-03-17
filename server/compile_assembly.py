"""This script contains the logic to compile user-written assembly code into object code (labels
made numerical and comments removed) and machine code (instructions become three-digit numbers in
base 10).
Functions:
    validate_label_name(label: str, line_number: int) -> None
    compile_assembly(user_written_code: str) -> result
    check_assembly(user_written_code: str) -> bool"""

mnemonic_operations_0_args = {"INP", "OUT", "HLT", "DAT"}
mnemonic_operations_1_arg_is_label = {"ADD", "SUB", "STA", "LDA", "BRA", "BRZ", "BRP"}
mnemonic_operations_1_arg_is_value = {"DAT"}
mnemonic_operations_1_arg = mnemonic_operations_1_arg_is_label | mnemonic_operations_1_arg_is_value
mnemonic_operations = mnemonic_operations_0_args | mnemonic_operations_1_arg

def validate_label_name(label: str, line_number: int):
    """Validate the name of a label to be created and raise error if invalid.

    Parameters
    ----------
    label : str
        The name of the label to validate.
    line_number : int
        The line number on which this label name was written in the user-written code.
    """
    # ensure label has valid chars (only alpha?)
    if not (label.isalnum() and label[0].isalpha()):
        raise ValueError(
            f"Label \"{label}\" must begin with a letter and be completely alphanumeric",
            line_number,
        )
    # ensure label is not an mnemonic operation
    if label in mnemonic_operations:
        raise ValueError(
            f"Label \"{label}\" cannot be an operation",
            line_number,
        )

def compile_assembly(user_written_code: str):
    """Compile user-written assembly into object code and machine code (memory/register contents).

    Parameters
    ----------
    user_written_code : str
        The original assembly code as written by user.

    Returns
    -------
    dict
        The result dictionary, containing object and machine code.

    Raises
    ------
    ValueError
        Incorrect assembly code written by user.
    """
    lines = []
    for index, line in enumerate(user_written_code.split("\n")):
        original_line_number = index + 1
        line = line.split("//")[0] # remove comment from line
        line = line.strip().upper()
        words = line.split()
        if line == "":
            # this is an empty line, we can ignore it without raising an error
            continue
        if len(words) > 3:
            raise ValueError("There cannot be more than 3 words on one line", original_line_number)

        if len(words) == 1:
            if line in mnemonic_operations_0_args:
                lines.append({ "operation": line })
            else:
                # received a line with only 1 word, but it is not an operation that takes no args
                if line in mnemonic_operations:
                    raise ValueError("Missing an argument for operation", original_line_number)
                raise ValueError(f"Invalid operation \"{line}\"", original_line_number)

        elif len(words) == 2:
            if words[0] in mnemonic_operations_1_arg_is_label:
                lines.append({
                    "uses_label": words[1],
                    "operation": words[0],
                })
            elif words[1] in mnemonic_operations_0_args:
                # line has structure <label> <operation>
                label = words[0]
                operation = words[1]
                validate_label_name(label, original_line_number)
                lines.append({
                    "create_label": label,
                    "operation": operation,
                })
            else:
                raise ValueError("Invalid line. Could not find operation.", original_line_number)

        else:
            # len(words) is 3
            # words[1] must be the operation
            if words[1] not in mnemonic_operations_1_arg:
                if words[1] in mnemonic_operations_0_args:
                    raise ValueError(
                        "Operation does not take arguments, received one.",
                        original_line_number
                    )
                raise ValueError(
                    "Line with 3 words should have structure: <label>, <operation>, <value>.",
                    original_line_number
                )
            # process label in words[0] and value in words[2]
            label = words[0]
            operation = words[1]
            arg = words[2]

            # validate label
            validate_label_name(label, original_line_number)

            if operation == "DAT":
                # validate value
                if not arg.isdigit():
                    raise ValueError(
                        f"Expected number 0-999, received {arg} (not a number)",
                        original_line_number,
                    )
                if not 0 <= int(arg) <= 999:
                    raise ValueError(
                        f"Expected number 0-999, received {arg} (out of range)",
                        original_line_number,
                    )

                lines.append({
                    "create_label": label,
                    "operation": words[1],
                    "value": arg.zfill(3),
                })
            else:
                # line has structure <label being created> <operation> <label being used as opcode>
                lines.append({
                    "create_label": label,
                    "operation": words[1],
                    "uses_label": arg,
                })


    # process code from intermediate object to finished form

    # get labels created
    created_labels = {} # {<name>: <memory address>}
    for line in lines:
        if "create_label" in line:
            created_labels[line["create_label"]] = None

    # ensure all used labels have been created
    for line in lines:
        if "uses_label" in line:
            if line["uses_label"] not in created_labels:
                raise ValueError(
                    f"Label \"{line["uses_label"]}\" used without being created.\
 Create labels by putting a label name at start of line.",
                )

    if len(lines) > 100:
        raise ValueError("Too many lines to fit in memory.")

    result = {
        "object_code": [],
        "memory_and_registers": {
            "memory": {},
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

    # fill in every memory location as 0 to start
    for i in range(100):
        result["memory_and_registers"]["memory"][str(i).zfill(2)] = "000"

    # assign memory address to every line
    address = 0
    for line in lines:
        line["memory_address"] = str(address).zfill(2)
        # if line creates label, store memory address in created_labels
        if "create_label" in line:
            created_labels[line["create_label"]] = line["memory_address"]
        address += 1

    # loop through lines to populate result
    for line in lines:
        cleaned_up_line = f"{line["memory_address"]} {line["operation"]}"
        line_in_memory = ""

        # add opcode to line_in_memory
        if line["operation"] == "DAT":
            val = line["value"] if "value" in line else "000"
            line_in_memory += val
            cleaned_up_line += " " + val
        else:
            line_in_memory += {
                "ADD": "1",
                "SUB": "2",
                "STA": "3",
                "LDA": "5",
                "BRA": "6",
                "BRZ": "7",
                "BRP": "8",
                "INP": "901",
                "OUT": "902",
                "HLT": "000",
            }[line["operation"]]

        if "uses_label" in line:
            used_label_loc = created_labels[line["uses_label"]]
            cleaned_up_line += f" {used_label_loc}"
            # add operand (label address) to line_in_memory
            line_in_memory += used_label_loc

        result["object_code"].append(cleaned_up_line)
        result["memory_and_registers"]["memory"][line["memory_address"]] = line_in_memory

    return result

def check_assembly(user_written_code: str):
    """Check if user-written assembly code is valid (will get compiled) successfully.

    Args:
        user_written_code (str): The original assembly code as written by user.

    Returns:
        bool: True if the code is valid, False otherwise.
    """
    try:
        compile_assembly(user_written_code)
    except ValueError:
        return False
    return True
