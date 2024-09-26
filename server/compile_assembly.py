instructions_0_args = {"INP", "OUT", "HLT", "DAT"}
instructions_1_arg_needs_label = {"ADD", "SUB", "LDA", "BRA", "BRZ", "BRP", "STA"}
instructions_1_arg_creates_label_needs_value = {"DAT"}
instructions_1_arg = instructions_1_arg_needs_label | instructions_1_arg_creates_label_needs_value
instructions = instructions_0_args | instructions_1_arg

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
            raise ValueError(original_line_number, "There cannot be more than 3 words on one line.")

        if len(words) == 1:
            if line in instructions_0_args:
                lines.append({ "command": line })
            else:
                # received a line with only 1 word, but it is not an instruction that takes no args
                if line in instructions:
                    raise ValueError(original_line_number, "Missing an argument for instruction")
                raise ValueError(original_line_number, "Invalid instruction")

        if len(words) == 3:
            if words[1] != "DAT":
                raise ValueError(
                    original_line_number,
                    "Line with 3 words should have structure: <label>, DAT, <value>"
                )
            # todo: process label in words[0] and value in words[2]
