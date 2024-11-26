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

        # copy assembly instruction from MDR to IR
        mdr_value = self.memory_and_registers["registers"]["MDR"]
        self.memory_and_registers["registers"]["IR"] = mdr_value
        transfers.append({
            "start_reg": "MDR",
            "end_reg": "IR",
            "value": mdr_value,
        })
        return transfers

    def __decode(self):
        # todo
        ...

    def __execute(self):
        # todo
        ...

    def step(self):
        """Runs one FDE cycle and returns new memory/registers and list of transfers (changes)

        Returns:
            _type_: _description_
        """
        # fetch
        transfers = self.__fetch()

        # todo: decode
        # todo: execute

        return {
            "memory_and_registers": self.memory_and_registers,
            "transfers": transfers,
        }

    def run(self):
        """Keeps running FDE cycles until a HLT or INP instruction is reached

        Returns:
            _type_: _description_
        """
        # todo: repeatedly call step
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
