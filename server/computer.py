"""This file is responsible for the fetch-decode-execute cycle. The Computer class represents the
entire LMC in a specific state, and has step and run methods which are triggered by the user.
Classes:
    Computer"""

class Computer:
    """A `Computer` object is instantiated with memory and register contents every time the client
    asks to step or run."""
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
        self.memory_and_registers["registers"]["PC"] = str(int(pc_value) + 1).zfill(2)
        # todo: should i have a transfer for this?
        # todo: raise error if trying to increment to 100

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

        if opcode in ("1", "2", "5"):
            # direct addressing
            # fetch required data (from memory location stored in MAR, i.e. the operand)
            argument = self.memory_and_registers["memory"][operand]
            self.memory_and_registers["registers"]["MDR"] = argument
            transfers.append({
                "start_mem": operand,
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
                reached_hlt = True
            elif opcode == "9" and operand == "01":
                # todo: INP
                reached_inp = True
            elif opcode == "9" and operand == "02":
                # todo: OUT
                ...
            else:
                raise ValueError("Invalid instruction beginning in 0 or 9")
        elif opcode in ("1", "2", "5"):
            # we are using the value in the MDR to modify the value in the ACC

            argument = self.memory_and_registers["registers"]["MDR"]
            # todo: does this need a better name? it is the contents of the memory location referred
            # to by the operand, and will be the argument passed to the instruction

            # execute instruction
            match opcode:
                case "1":
                    # add
                    # add from MDR to ACC
                    self.memory_and_registers["registers"]["ACC"] += argument
                    if self.memory_and_registers["registers"]["ACC"] > 999:
                        self.memory_and_registers["registers"]["CARRY"] = 1
                    else:
                        self.memory_and_registers["registers"]["CARRY"] = 0
                    # todo: transfer
                case "2":
                    # sub
                    # subtract MDR value from ACC
                    self.memory_and_registers["registers"]["ACC"] -= argument
                    if self.memory_and_registers["registers"]["ACC"] < 0:
                        self.memory_and_registers["registers"]["CARRY"] = 1
                    else:
                        self.memory_and_registers["registers"]["CARRY"] = 0
                    # todo: transfer
                case "5":
                    # lda
                    # set ACC value to value stored in MDR
                    self.memory_and_registers["registers"]["ACC"] = argument

            transfers.append({
                "start_reg": "MDR",
                "end_reg": "ACC",
                "value": argument,
            })

        else:
            match opcode:
                case "3":
                    # sta
                    # copy from ACC to memory location stored in MAR
                    acc_value = self.memory_and_registers["registers"]["ACC"]
                    self.memory_and_registers["memory"][operand] = acc_value
                    transfers.append({
                        "start_reg": "ACC",
                        "end_mem": operand,
                        "value": acc_value,
                    })
                case "6":
                    # bra
                    # set IR to operand
                    self.memory_and_registers["registers"]["IR"] = operand
                    # todo: transfer? coming from actual operand
                case "7":
                    # brz
                    # set IR to operand if ACC is 0
                    if self.memory_and_registers["registers"]["ACC"] == 0:
                        # set IR to operand
                        self.memory_and_registers["registers"]["IR"] = operand
                        # todo: transfer? coming from actual operand
                case "8":
                    # brp
                    # set IR to operand if CARRY is 1
                    if self.memory_and_registers["registers"]["CARRY"] == 1:
                        self.memory_and_registers["registers"]["IR"] = operand
                        # todo: transfer? coming from actual operand

        return reached_hlt, reached_inp, transfers

    def step(self):
        """Runs one FDE cycle and returns new memory/registers and list of transfers (changes)

        Returns:
            _type_: _description_
        """
        return_obj = {
            "memory_and_registers": None,
            "transfers": None,
            "reached_HLT": False,
            "reached_INP": False,
        }

        # fetch
        return_obj["transfers"] = self.__fetch()

        # decode
        return_obj["transfers"].extend(self.__decode())

        # execute
        return_obj["reached_HLT"], return_obj["reached_INP"], new_transfers = self.__execute()
        return_obj["transfers"].extend(new_transfers)

        return_obj["memory_and_registers"] = self.memory_and_registers
        return return_obj

    def finish_step_after_input(self, input_value: str):
        # todo: param/return detail in docstring
        """Finishes one FDE cycle after an input value has been retrieved from the user."""
        # todo: should input value be validated here? maybe think about this once more structure
        # put input value into accumulator
        self.memory_and_registers["registers"]["ACC"] = input_value
        transfer = {
            # todo: start location: from input?
            "end_reg": "ACC",
            "value": input_value,
        }
        return transfer

    def run(self):
        """Keeps running FDE cycles until a HLT or INP instruction is reached

        Returns:
            _type_: _description_
        """
        reached_hlt = False
        reached_inp = False

        # store list of results from every FDE cycle (step call) we do, and return all
        all_results = []

        while not any((reached_hlt, reached_inp)):
            result = self.step()
            reached_hlt = result["reached_HLT"]
            reached_inp = result["reached_INP"]
            all_results.append(result)

        return all_results

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
    print(comp.step())
    print(comp.step())
    print(comp.step())
    print(comp.step())
