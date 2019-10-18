import sys
################# Central Processing Unit ###########################
class CPU:
    def __init__(self):
        self.ram = [0] * 256          # makes a list for the 256 bytes of memory
        self.register = [0] * 8       # makes a list for the 8 wires/registeres available
        self.PC = 0                   # program counter - think sing along 
        self.SPL = 7                  # stack pointer initialized 
        self.flags = 0b00000000


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

    def ram_read(self, MAR):
        return self.ram[MAR]

    def ram_write(self, MDR, MAR):
        self.ram[MAR] = MDR

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