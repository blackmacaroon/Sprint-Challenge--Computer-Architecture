class CPU:
    def __init__(self):
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.PC = 0
        self.SPL = 7