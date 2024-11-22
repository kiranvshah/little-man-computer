class Computer:
    """A `Computer` object is instantiated with memory and register contents every time the client
    asks to step."""
    def __init__(self, memory_and_registers):
        self.memory_and_registers = memory_and_registers

    def step(self):
        """Runs one FDE cycle and returns new memory/registers and list of transfers (changes)

        Returns:
            _type_: _description_
        """
        return {
            "memory_and_registers": self.memory_and_registers,
            "transfers": [],
        }

    def run_till_hlt(self):
        """Keeps running FDE cycles until a HLT instruction is reached

        Returns:
            _type_: _description_
        """
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
    print(comp)
