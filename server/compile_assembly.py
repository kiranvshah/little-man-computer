"""Functions:
    compile_assembly(user_written_code) -> result"""

instructions_0_args = {"INP", "OUT", "HLT", "DAT"}
instructions_1_arg_is_label = {"ADD", "SUB", "STA", "LDA", "BRA", "BRZ", "BRP"}
instructions_1_arg_is_value = {"DAT"}
instructions_1_arg = instructions_1_arg_is_label | instructions_1_arg_is_value
instructions = instructions_0_args | instructions_1_arg

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
            raise ValueError(original_line_number, "There cannot be more than 3 words on one line")

        if len(words) == 1:
            if line in instructions_0_args:
                lines.append({ "command": line })
            else:
                # received a line with only 1 word, but it is not an instruction that takes no args
                if line in instructions:
                    raise ValueError(original_line_number, "Missing an argument for instruction")
                raise ValueError(original_line_number, "Invalid instruction")

        elif len(words) == 3:
            # words[1] must be the command
            if words[1] not in instructions_1_arg:
                if words[1] in instructions_0_args:
                    raise ValueError(
                        original_line_number,
                        "Instruction does not take arguments, received one."
                    )
                raise ValueError(
                    original_line_number,
                    "Line with 3 words should have structure: <label>, <command>, <value>."
                )
            # process label in words[0] and value in words[2]
            label = words[0]
            instruction = words[1]
            arg = words[2]

            # validate label
            # ensure label has valid chars (only alpha?)
            if not (label.isalnum() and label[0].isalpha()):
                raise ValueError(
                    original_line_number,
                    f"Label \"{label}\" must begin with a letter and be completely alphanumeric"
                )
            # ensure label is not a command word
            if label in instructions:
                raise ValueError(
                    original_line_number,
                    f"Label \"{label}\" cannot be an instruction"
                )

            if instruction == "DAT":
                # validate value
                if not arg.isdigit():
                    raise ValueError(
                        original_line_number,
                        f"Expected number 0-999, received {arg} (not a number)"
                    )
                if not 0 <= int(arg) <= 999:
                    raise ValueError(
                        original_line_number,
                        f"Expected number 0-999, received {arg} (out of range)"
                    )

                lines.append({
                    "create_label": label,
                    "command": words[1],
                    "value": arg,
                })
            else:
                # todo: validate arg as label
                lines.append({
                    "create_label": label,
                    "command": words[1],
                    "uses_label": arg,
                })


        else:
            # len(words) is 2
            if words[0] in instructions_1_arg_is_label:
                # process command
                lines.append({
                    "uses_label": words[1],
                    "command": words[0],
                })
            else:
                raise ValueError(original_line_number, f"Invalid instruction. Received {words[0]}")

    # process code from intermediate object to finished form

    # get labels created
    created_labels = {} # {<name>: <memory address>}
    for line in lines:
        if line["command"] == "DAT":
            created_labels[line["create_label"]] = None

    # ensure all used labels have been created
    for line in lines:
        if "uses_label" in line:
            if line["uses_label"] not in created_labels:
                raise ValueError(
                    f"""Label \"{
                        line["uses_label"]
                    }\" used without being created. Create labels with DAT.""",
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
        cleaned_up_line = f"{line["memory_address"]} {line["command"]}"
        line_in_memory = ""

        # add opcode to line_in_memory
        match line["command"]:
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
                line_in_memory += line["value"]
            case _:
                pass

        if "uses_label" in line:
            used_label_loc = created_labels[line["uses_label"]]
            cleaned_up_line += f" {used_label_loc}"
            # add operand (label address) to line_in_memory
            line_in_memory += used_label_loc

        if "create_label" in line:
            arg = line["value"]
            cleaned_up_line += f" {arg}"

        result["compiled_code"].append(cleaned_up_line)
        result["memory_and_registers"]["memory"][line["memory_address"]] = line_in_memory

    return result


if __name__ == "__main__":
    print(compile_assembly("""        lda space
        sta char
loop    lda char
        out
        lda space
        lda char
        add one
        sta char
        sub max
        brz end
        bra loop
end     hlt
space   dat 32
one     dat 1
max     dat 97
char    dat
// start of ASCII character table
"""))
