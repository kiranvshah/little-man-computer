instructions_1_word = {"INP", "OUT", "HLT", "DAT"} # command at words[0]
instructions_2_words = {"ADD", "SUB", "STA", "LDA", "BRA", "BRZ", "BRP"} # command at words[0]
instructions_3_words = {"DAT"} # command at words[1]
instructions = instructions_1_word | instructions_2_words | instructions_3_words

def compile_assembly(user_written_code: str):
    """Return the compiled user-written assembly as cleaned-up code and memory/register contents."""
    lines = []
    for index, line in enumerate(user_written_code.split("\n")):
        original_line_number = index + 1
        line = line.split("//")[0] # remove comment from line
        line = line.strip().upper()
        words = line.split()
        if line == "":
            # this is an empty line, we can ignore it but not raise an error
            continue
        if len(words) > 3:
            raise ValueError(original_line_number, "There cannot be more than 3 words on one line")

        if len(words) == 1:
            if line in instructions_1_word:
                lines.append({ "command": line })
            else:
                # received a line with only 1 word, but it is not an instruction that takes no args
                if line in instructions:
                    raise ValueError(original_line_number, "Missing an argument for instruction")
                raise ValueError(original_line_number, "Invalid instruction")

        elif len(words) == 3:
            if words[1] != "DAT":
                raise ValueError(
                    original_line_number,
                    "Line with 3 words should have structure: <label>, DAT, <value>"
                )
            # process label in words[0] and value in words[2]
            label = words[0]
            value = words[2]

            # validate value
            if not value.isdigit():
                raise ValueError(
                    original_line_number,
                    f"Expected number 0-999, received {value} (not a number)"
                )
            if not 0 <= int(value) <= 999:
                raise ValueError(
                    original_line_number,
                    f"Expected number 0-999, received {value} (out of range)"
                )

            lines.append({
                "create_label": label,
                "command": words[1],
                "value": value,
            })

        else:
            # len(words) is 2
            if words[0] in instructions_2_words:
                # process command
                lines.append({
                    "uses_label": words[1], # todo: ensure label has valid chars (only alpha?)
                    "command": words[0],
                })
            else:
                raise ValueError(original_line_number, f"Invalid instruction. Received {words[0]}")

    # process code from intermediate object to finished form

    # get labels created by DAT
    created_labels = {} # {<name>: <memory address>}
    for line in lines:
        if line["command"] == "DAT":
            created_labels[line["create_label"]] = None

    # ensure all used labels have been created
    for line in lines:
        if "uses_label" in line:
            if line["uses_label"] not in created_labels.keys():
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
            value = line["value"]
            cleaned_up_line += f" {value}"

        result["compiled_code"].append(cleaned_up_line)
        result["memory_and_registers"]["memory"][line["memory_address"]] = line_in_memory

    return result

if __name__ == "__main__":
    print(compile_assembly("""// store an input
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
second DAT 000"""))
