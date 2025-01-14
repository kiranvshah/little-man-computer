"""Functions:
    validate_label_name(label: str, line_number: int) -> None
    compile_assembly(user_written_code: str) -> result
    check_assembly(user_written_code: str) -> bool"""

instructions_0_args = {"INP", "OUT", "HLT", "DAT"}
instructions_1_arg_is_label = {"ADD", "SUB", "STA", "LDA", "BRA", "BRZ", "BRP"}
instructions_1_arg_is_value = {"DAT"}
instructions_1_arg = instructions_1_arg_is_label | instructions_1_arg_is_value
instructions = instructions_0_args | instructions_1_arg

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
    # ensure label is not an instruction
    if label in instructions:
        raise ValueError(
            f"Label \"{label}\" cannot be an instruction",
            line_number,
        )

# todo: could this function benefit from more decomposition?
def compile_assembly(user_written_code: str):
    """Compile user-written assembly into cleaned-up code and memory/register contents.

    Parameters
    ----------
    user_written_code : str
        The original assembly code as written by user.

    Returns
    -------
    dict
        The result dictionary, containing cleaned-up code and memory/register contents.

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
            if line in instructions_0_args:
                lines.append({ "instruction": line })
            else:
                # received a line with only 1 word, but it is not an instruction that takes no args
                if line in instructions:
                    raise ValueError("Missing an argument for instruction", original_line_number)
                raise ValueError(f"Invalid instruction \"{line}\"", original_line_number)

        elif len(words) == 2:
            if words[0] in instructions_1_arg_is_label:
                # process instruction
                lines.append({
                    "uses_label": words[1],
                    "instruction": words[0],
                })
            elif words[1] in instructions_0_args:
                # line has structure <label> <instruction>
                label = words[0]
                instruction = words[1]
                validate_label_name(label, original_line_number)
                lines.append({
                    "create_label": label,
                    "instruction": instruction,
                })
            else:
                raise ValueError("Invalid line. Could not find instruction.", original_line_number)

        else:
            # len(words) is 3
            # words[1] must be the instruction
            if words[1] not in instructions_1_arg:
                if words[1] in instructions_0_args:
                    raise ValueError(
                        "Instruction does not take arguments, received one.",
                        original_line_number
                    )
                raise ValueError(
                    "Line with 3 words should have structure: <label>, <instruction>, <value>.",
                    original_line_number
                )
            # process label in words[0] and value in words[2]
            label = words[0]
            instruction = words[1]
            arg = words[2]

            # validate label
            validate_label_name(label, original_line_number)

            if instruction == "DAT":
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
                    "instruction": words[1],
                    "value": arg.zfill(3),
                })
            else:
                lines.append({
                    "create_label": label,
                    "instruction": words[1],
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
                # todo: consider passing original line numbers to intermediate obj so they can be displayed in this error message?
                raise ValueError(
                    f"Label \"{line["uses_label"]}\" used without being created.\
 Create labels by putting a label name at start of line.",
                )

    if len(lines) > 100:
        raise ValueError("Too many lines to fit in memory.")

    result = {
        "compiled_code": [],
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
        cleaned_up_line = f"{line["memory_address"]} {line["instruction"]}"
        line_in_memory = ""

        # add opcode to line_in_memory
        # todo: use dictionary of functions instead of match case? use functools.partial for all but DAT to have function with arg for num to put in memory.
        match line["instruction"]:
            case "ADD":
                line_in_memory += "1"
            case "SUB":
                line_in_memory += "2"
            case "STA":
                line_in_memory += "3"
            case "LDA":
                line_in_memory += "5"
            case "BRA":
                line_in_memory += "6"
            case "BRZ":
                line_in_memory += "7"
            case "BRP":
                line_in_memory += "8"
            case "INP":
                line_in_memory += "901"
            case "OUT":
                line_in_memory += "902"
            case "HLT":
                line_in_memory += "000"
            case "DAT":
                val = line["value"] if "value" in line else "000"
                line_in_memory += val
                cleaned_up_line += " " + val
            case _:
                pass

        if "uses_label" in line:
            used_label_loc = created_labels[line["uses_label"]]
            cleaned_up_line += f" {used_label_loc}"
            # add operand (label address) to line_in_memory
            line_in_memory += used_label_loc

        result["compiled_code"].append(cleaned_up_line)
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
