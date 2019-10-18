import sys
################# Central Processing Unit ###########################
class CPU:
    def __init__(self):
        self.ram = [0] * 256          # makes a list for the 256 bytes of memory
        self.register = [0] * 8       # makes a list for the 8 wires/registeres available
        self.PC = 0                   # program counter - think sing along 
        self.SPL = 7                  # stack pointer initialized 
        self.flags = 0b00000000       # flags bits set to false


    def load(self):
        address = 0
        try:
            with open(sys.argv[1]) as program:
                for line in program:
                    if line[0] != "#" and line != "\n":
                        self.ram[address] = int(line[:8], 2)  # convert to integer base-2
                        address += 1
                program.closed
        except ValueError:
            print(f"file not found")

    def trace(self):
        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.PC,
            #self.fl,
            #self.ie,
            self.ram_read(self.PC),
            self.ram_read(self.PC + 1),
            self.ram_read(self.PC + 2)
        ), end='')
        for i in range(8):
            print(" %02X" % self.register[i], end='')
        print()

    def ram_read(self, address):   # MAR = address in memory
        return self.ram[address]

    def ram_write(self, address, data):   # MAR = address, MDR = data at address
        self.ram[address] = data

    def ldi(self, address, data):  # load
        self.register[address] = data

    def prnt(self, address):   # print
        print(self.register[address])

    def halt(self):
        self.running = False
        sys.exit()

    ############ Arithmetic Logic Unit  ###########################
    def alu(self, op, reg_a, reg_b):
        if op == "ADD":
            self.register[reg_a] += self.register[reg_b]
        elif op == "SUB":
            self.register[reg_a] -= self.register[reg_b]
        elif op == "MUL":
            self.register[reg_a] *= self.register[reg_b]
        elif op == "DIV":
            self.register[reg_a] /= self.register[reg_b]
        elif op == "CMP":  #compare flags bits: 0b00000LGE (less, greater, equal)
            if reg_a < reg_b:
                self.flags == 0b00000100
            elif reg_a > reg_b:
                self.flags == 0b00000010
            elif reg_a == reg_b:
                self.flags == 0b00000001
        else:
            raise Exception("Unsupported ALU operation")

    def run(self):
        """Run the CPU."""
        PRN = 0b01000111
        HLT = 0b00000001
        LDI = 0b10000010
        ADD = 0b10100000
        SUB = 0b10100001
        MUL = 0b10100010
        DIV = 0b10100011
        PUSH = 0b01000101
        POP = 0b01000110
        CALL = 0b01010000
        RET = 0b00010001
        CMP = 0b10100111
        JMP = 0b01010100
        JEQ = 0b01010101
        JNE = 0b01010110
        running = True
        while running:
            IR = self.ram[self.PC]    # instruction register
            operandA = self.ram_read(self.PC + 1)   
            operandB = self.ram_read(self.PC + 2)
            if IR == LDI:
                print("load", operandA)
                self.ldi(operandA, operandB)
                self.PC += 3
            elif IR == PRN:
                self.prnt(operandA)
                self.PC += 2
            elif IR == HLT:
                print("halt")
                self.halt()
                self.PC += 1
            elif IR == ADD:
                self.alu("ADD", operandA, operandB)
                self.PC += 3
                print("add", operandA)
            elif IR == SUB:
                self.alu("SUB", operandA, operandB)
                self.PC += 3
            elif IR == MUL:
                print("multiply", operandA)
                self.alu("MUL", operandA, operandB)
                self.PC += 3
            elif IR == DIV:
                self.alu("DIV", operandA, operandB)
                self.PC += 3
            elif IR == CMP:
                print("compare", operandA)
                self.alu("CMP", operandA, operandB)
                self.PC += 3
            elif IR == POP:
                print("pop", operandA)
                # copy the value from the address pointed to by the SP, to the given register
                self.register[operandA] = self.ram[self.SPL]
                # increment pointer location
                self.SPL += 1
                self.PC += 2
            elif IR == PUSH:
                print("push", operandA)
                self.SPL -= 1
                self.ram[self.SPL] = self.register[operandA]
                self.PC += 2
            elif IR == CALL:
                print("call", operandA)
                self.register[self.SPL] -= 1
                self.ram[self.SPL] = self.PC +2
                self.PC = self.register[operandA]
            elif IR == RET:
                print("return")
                self.PC = self.ram[self.SPL]
                self.register[self.SPL] += 1
            elif IR == JMP:
                print("jump", operandA)
                self.PC = self.register[operandA]
            # flags 00000LGE
            elif IR == JEQ:
                print("jump equal", operandA)
                # If `equal` flag is set (true)
                if self.flags == 0b00000001:
                    # jump to the address stored in the given register
                    self.PC = self.register[operandA]
                #otherwise, skip to the next instruction PC += 2
                else:
                    self.PC += 2
                
            elif IR == JNE:
                print("jump not equal", operandA)
                # If `E` flag is clear (false, 0)
                if ((self.flags == 0b00000001) == 0):
                    #jump to the address stored in the given register
                    self.PC = self.register[operandA]
                # otherwise, skip to the next instruction PC += 2
                else:
                    self.PC += 2

            else:
                print(f"Wait, what? {IR}")
                sys.exit(1)