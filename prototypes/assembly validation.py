ins_no_args = {'INP', 'OUT', 'HLT', 'DAT'}
ins_one_arg_uses_label = {'ADD', 'SUB', 'LDA', 'BRA', 'BRZ', 'BRP'}
ins_one_arg_creates_label = {'STA'}
ins_one_arg_uses_value = {'DAT'}
ins_one_arg = ins_one_arg_uses_label | ins_one_arg_creates_label | ins_one_arg_uses_value
ins_all = ins_no_args | ins_one_arg


def validate_line(line: str, allowable_labels = []):
    line = line.strip()
    if len(line) < 3:
        raise ValueError('Line must contain at least 3 characters')
    line = line.upper()
    words = line.split()

    
    instruction_indices = [i for i in range(len(words)) if words[i] in ins_all]
    num_of_instructions = len(instruction_indices)
    if num_of_instructions > 1:
        raise ValueError('More than one instruction in a line. Labels cannot be mnemonics.')
    if num_of_instructions == 0:
        raise ValueError('Line with no valid mnemonic.')
    instruction_index = instruction_indices[0]
    instruction = words[instruction_index]

    if instruction_index == 1:
        # words[0] is the name for a label representing the memory address of this instruction
        label_to_create = words[0]
        allowable_labels.append(label_to_create)
    if instruction_index > 1:
        raise ValueError('More than one left-hand argument given.')
    
    if instruction not in ins_one_arg and len(words) > instruction_index + 1:
        raise ValueError('Right-hand argument passed to an instruction that cannot take it.')
    if instruction not in ins_no_args and len(words) == instruction_index + 1:
        raise ValueError('Right-hand argument expected for an instruction; none given.')

    if instruction in ins_one_arg:
        if len(words) > instruction_index + 2:
            raise ValueError('More than one right-hand argument given; only one expected.')
        if len(words) == instruction_index + 2:
            # argument given
            right_arg = words[instruction_index + 1]
            if instruction in ins_one_arg_uses_label:
                if right_arg not in allowable_labels:
                    raise ValueError('Right-hand argument should be a label, but this label has not been created.')
            elif instruction in ins_one_arg_creates_label:
                allowable_labels.append(right_arg)
            elif instruction in ins_one_arg_uses_value:
                # ensure provided value is valid
                if not right_arg.isnumeric():
                    raise ValueError('Provided value is not numeric')


def validate_assembly(code: str):
    labels: list[str] = []
    for line_num, line in enumerate(code.split('\n')):
        try:
            validate_line(line, labels)
        except Exception as err:
            raise ValueError(f'Line {line_num+1}: {err}')



validate_assembly('''INP
  STA first
  INP
  STA second
  LDA first
  SUB second
  OUT
  HLT
first DAT 0
second DAT 0''')