class Computer:
    """A `Computer` object is instantiated with memory and register contents every time the client
    asks to step."""
    def __init__(self, memory_and_registers):
        self.memory_and_registers = memory_and_registers

    def __fetch(self):
        transfers = []

        # copy value from program counter to MAR
        pc_value = self.memory_and_registers["registers"]["PC"]
        self.memory_and_registers["registers"]["MAR"] = pc_value
        transfers.append({
            "start_reg": "PC",
            "end_reg": "MAR",
            "value": pc_value,
        })

        # copy assembly instruction from memory (at address in MAR) to MDR
        mar_value = self.memory_and_registers["registers"]["MAR"]
        assembly_instruction = self.memory_and_registers["memory"][mar_value]
        self.memory_and_registers["registers"]["MDR"] = assembly_instruction
        transfers.append({
            "start_mem": mar_value,
            "end_reg": "MDR",
            "value": assembly_instruction,
        })

        # increment program counter by 1
        pc_value = self.memory_and_registers["registers"]["PC"]
        self.memory_and_registers["registers"]["PC"] = str(int(pc_value) + 1)
        # todo: should i have a transfer for this?

        # copy assembly instruction from MDR to IR and MAR
        mdr_value = self.memory_and_registers["registers"]["MDR"]
        # copy opcode from MDR to IR
        opcode = mdr_value[0]
        self.memory_and_registers["registers"]["IR"] = opcode
        transfers.append({
            "start_reg": "MDR",
            "end_reg": "IR",
            "value": opcode,
        })
        # copy operand from MDR to MAR
        operand = mdr_value[1:]
        self.memory_and_registers["registers"]["MAR"] = operand
        transfers.append({
            "start_reg": "MDR",
            "end_reg": "MAR",
            "value": operand,
        })
        return transfers

    def __decode(self):
        transfers = []


        opcode = self.memory_and_registers["registers"]["IR"]
        operand = self.memory_and_registers["registers"]["MAR"]
        if opcode not in ("9", "0"):
            # direct addressing
            # fetch required data (from memory location stored in MAR, i.e. the operand)
            argument = self.memory_and_registers["memory"][operand]
            self.memory_and_registers["registers"]["MDR"] = argument
            transfers.append({
                "start_mem": "LOC",
                "end_reg": "MDR",
                "value": argument,
            })
        return transfers

    def __execute(self):
        reached_hlt = False
        reached_inp = False
        transfers = []

        opcode = self.memory_and_registers["registers"]["IR"]
        operand = self.memory_and_registers["registers"]["MAR"]
        if opcode in ("9", "0"):
            # INP, OUT, or HLT. opcode should not be treated as memory address.
            if opcode == "0" and operand == "00":
                # todo: HLT
                reached_hlt = True
                ...
            elif opcode == "9" and operand == "01":
                # todo: INP
                reached_inp = True
                ...
            elif opcode == "9" and operand == "02":
                # todo: OUT
                ...
            else:
                raise ValueError("Invalid instruction beginning in 0 or 9")

        return reached_hlt, reached_inp, transfers

    def step(self):
        """Runs one FDE cycle and returns new memory/registers and list of transfers (changes)

        Returns:
            _type_: _description_
        """
        # fetch
        transfers = self.__fetch()

        # decode
        transfers.extend(self.__decode())

        # execute
        reached_hlt, reached_inp, new_transfers = self.__execute()
        transfers.extend(new_transfers)

        if reached_hlt:
            # todo: tell client that HLT was reached. stop run loop if run called
            ...
        elif reached_inp:
            # todo: tell client that INP was reached, get input and handle it. stop run loop if run called
            ...

        return {
            "memory_and_registers": self.memory_and_registers,
            "transfers": transfers,
        }

    def run(self):
        """Keeps running FDE cycles until a HLT or INP instruction is reached

        Returns:
            _type_: _description_
        """
        # todo: repeatedly call step until HLT or INP
        return ...

if __name__ == "__main__":
    from compile_assembly import compile_assembly
    compile_assembly_result = compile_assembly("""// store an input
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
second DAT 000""")
    comp = Computer(compile_assembly_result["memory_and_registers"])
    print(comp.step())
