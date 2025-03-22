"""This file is responsible for the fetch-decode-execute cycle. The Computer class represents the
entire LMC in a specific state, and has step and run methods which are triggered by the user.
Classes:
    Computer"""

import re

class Computer:
    """A `Computer` object is instantiated with memory and register contents every time the client
    asks to step or run."""
    def __init__(self, memory_and_registers):
        self.memory_and_registers = memory_and_registers

    def __fetch(self):
        """Runs the fetch stage of the FDE cycle on the Computer object.

        Returns
        -------
        list[Transfer]
            A list of transfer dictionaries.
        """
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
        if pc_value == "99":
            raise RuntimeError("Can't increment PC to a value above 99.")
        self.memory_and_registers["registers"]["PC"] = str(int(pc_value) + 1).zfill(2)
        transfers.append({
            "start_reg": "PC",
            "end_reg": "PC",
            "value": self.memory_and_registers["registers"]["PC"],
        })

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
        """Runs the decode stage of the FDE cycle on the Computer object.

        Returns
        -------
        list[Transfer]
            A list of transfer dictionaries.
        """
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
        """Runs the execute stage of the FDE cycle on the Computer object.

        Returns
        -------
        set(bool, bool, list[Transfer])
            First boolean: whether HLT was called and program needs to stop execution.
            Second boolean: whether INP was called and user input needs to be collected.
            Finally: A list of transfer dictionaries
        """
        reached_hlt = False
        reached_inp = False
        output = ""
        transfers = []

        opcode = self.memory_and_registers["registers"]["IR"]
        operand = self.memory_and_registers["registers"]["MAR"]
        if opcode in ("9", "0"):
            # INP, OUT, or HLT. operand should not be treated as memory address.
            if opcode == "0" and operand == "00":
                reached_hlt = True
            elif opcode == "9" and operand == "01":
                reached_inp = True
            elif opcode == "9" and operand == "02":
                # OUT
                output = self.memory_and_registers["registers"]["ACC"]
            else:
                raise RuntimeError("Invalid instruction beginning in 0 or 9")
        elif opcode in ("1", "2", "5"):
            # we are using the value in the MDR to modify the value in the ACC

            argument = self.memory_and_registers["registers"]["MDR"]
            # this is the contents of the memory location referred to by
            # the operand, and will be the argument passed to the instruction

            # execute instruction
            match opcode:
                case "1":
                    # add
                    # add from MDR to ACC
                    arithmetic_result = int(
                        self.memory_and_registers["registers"]["ACC"]
                    ) + int(argument)
                    self.memory_and_registers["registers"]["ACC"] = str(
                        arithmetic_result % 1000
                    ).zfill(3)
                    transfers.append({
                        "start_mem": operand,
                        "end_reg": "ACC",
                        "value": self.memory_and_registers["registers"]["ACC"],
                    })
                    if int(arithmetic_result) > 999:
                        self.memory_and_registers["registers"]["CARRY"] = "1"
                    else:
                        self.memory_and_registers["registers"]["CARRY"] = "0"
                    transfers.append({
                        "start_reg": "ACC",
                        "end_reg": "CARRY",
                        "value": self.memory_and_registers["registers"]["CARRY"],
                    })
                case "2":
                    # sub
                    # subtract MDR value from ACC
                    arithmetic_result = int(
                        self.memory_and_registers["registers"]["ACC"]
                    ) - int(argument)
                    self.memory_and_registers["registers"]["ACC"] = str(
                        arithmetic_result % 1000
                    ).zfill(3)
                    transfers.append({
                        "start_mem": operand,
                        "end_reg": "ACC",
                        "value": self.memory_and_registers["registers"]["ACC"],
                    })
                    if int(arithmetic_result) < 0:
                        self.memory_and_registers["registers"]["CARRY"] = "1"
                    else:
                        self.memory_and_registers["registers"]["CARRY"] = "0"
                    transfers.append({
                        "start_reg": "ACC",
                        "end_reg": "CARRY",
                        "value": self.memory_and_registers["registers"]["CARRY"],
                    })
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
                    # set PC to operand
                    self.memory_and_registers["registers"]["PC"] = operand
                    transfers.append({
                        "end_reg": "PC",
                        "value": self.memory_and_registers["registers"]["PC"],
                    })
                case "7":
                    # brz
                    # set PC to operand if ACC is 0
                    if self.memory_and_registers["registers"]["ACC"] == "000":
                        # set IR to operand
                        self.memory_and_registers["registers"]["PC"] = operand
                        transfers.append({
                            "end_reg": "PC",
                            "value": self.memory_and_registers["registers"]["PC"],
                        })
                case "8":
                    # brp
                    # set PC to operand if CARRY is 1
                    if self.memory_and_registers["registers"]["CARRY"] == "1":
                        self.memory_and_registers["registers"]["PC"] = operand
                        transfers.append({
                            "end_reg": "PC",
                            "value": self.memory_and_registers["registers"]["PC"],
                        })

        return reached_hlt, reached_inp, output, transfers

    def step(self):
        """Runs one FDE cycle and returns new memory/registers and list of transfers (changes)

        Returns:
            dict: A dictionary containing a list of transfers and the new state of the LMC
        """
        return_obj = {
            "memory_and_registers": None,
            "transfers": None,
            "reached_HLT": False,
            "reached_INP": False,
            "output": "",
        }

        # fetch
        return_obj["transfers"] = self.__fetch()

        # decode
        return_obj["transfers"].extend(self.__decode())

        # execute
        (   return_obj["reached_HLT"],
            return_obj["reached_INP"],
            return_obj["output"],
            new_transfers
        ) = self.__execute()
        return_obj["transfers"].extend(new_transfers)

        return_obj["memory_and_registers"] = self.memory_and_registers
        return return_obj

    def finish_after_input(self, input_value: str):
        """Finishes one FDE cycle after an input value has been retrieved from the user.

        Parameters
        ----------
        input_value : str
            The number inputted by the user

        Returns
        -------
        dict
            One transfer object describing the action to be taken as a result of this input.
        """
        # check input value is valid
        # this validation is also done client-side, but server shouldn't be broken by bad requests
        input_is_invalid = re.fullmatch(r"^\d{1,3}$", input_value) is None
        if input_is_invalid:
            raise ValueError("Invalid input value. Must be an integer 0-999.")
        # put input value into accumulator
        self.memory_and_registers["registers"]["ACC"] = input_value.zfill(3)
        transfer = {
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

        while not (
            reached_hlt # if HLT is reached we should stop
            or reached_inp # if INP is reached we should stop
            or len(all_results) > 100 # timeout due to possibility of infinite loop
        ):
            result = self.step()
            reached_hlt = result["reached_HLT"]
            reached_inp = result["reached_INP"]
            all_results.append(result)

        if len(all_results) > 100:
            raise RuntimeError("Timed out due to too many fetch-decode-execute cycles.")

        return all_results
