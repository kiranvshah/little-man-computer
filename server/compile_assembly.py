instructions_1_word = {"INP", "OUT", "HLT", "DAT"} # command at words[0]
instructions_2_words = {"ADD", "SUB", "LDA", "BRA", "BRZ", "BRP", "STA"} # command at words[0]
instructions_3_words = {"DAT"} # command at words[1]
instructions = instructions_1_word | instructions_2_words | instructions_3_words

def compile_assembly(user_written_code: str):
    """Return the compiled the user-written assembly code as cleaned-up code and memory and register contents."""
    lines = []
    for index, line in enumerate(user_written_code.split("\n")):
        original_line_number = index + 1
        print(f"testing line {original_line_number}")
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
                raise ValueError(original_line_number, f"Expected number 0-999, received {value} (not a number)")
            if not 0 <= int(value) <= 999:
                raise ValueError(original_line_number, f"Expected number 0-999, received {value} (out of range)")

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
                    "uses_label": words[1],
                    "command": words[0],
                })
            else:
                raise ValueError(original_line_number, f"Invalid instruction. Received {words[0]}")
    
    # todo: process code from intermediate object to finished form
    return lines

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