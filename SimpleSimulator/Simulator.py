import sys
import matplotlib.pyplot as plt


class Memory:

    def __init__(self):
        self.mem = ["0000000000000000"] * 256
        self.programCounter = []
        self.cycle = []
        i = 0
        while True:
            try:
                s = input()
                self.mem[i] = s
                i += 1
            except EOFError:
                break

    def fetch(self, addr, cycle):
        self.programCounter.append(addr)
        self.cycle.append(cycle)
        return self.mem[addr]

    def dump(self):
        for i in self.mem:
            sys.stdout.write(i+"\n")

    def showTraces(self):

        x = self.cycle
        y = self.programCounter

        plt.scatter(x, y)
        plt.savefig('.\plot.png')

        plt.xlabel('Cycle')
        plt.ylabel('Memory Address')

        plt.title("Memory Accesses v/s Cycles")

        plt.show()



class RegisterFile:
    def __init__(self):
        self.registerList = ["0000000000000000"] * 8

    def dump(self):
        print(*self.registerList)


class ProgramCounter:

    def __init__(self, PC):
        self.PC = PC

    def getVal(self):
        return self.PC

    def update(self, nextPC):
        self.PC = nextPC

    def dump(self):
        sys.stdout.write(format(self.PC, "08b") + " ")


class ExecutionEngine:

    def __init__(self, memory, registerFile):
        self.halted = False
        self.nextPC = 0
        self.memory = memory.mem
        self.registerFile = registerFile.registerList

    def execute(self, inst, cycle):

        lstA = ["00000", "00001", "00110", "01010", "01011", "01100"]
        lstB = ["00010", "01000", "01001"]
        lstC = ["00011", "00111", "01101", "01110"]
        lstD = ["00100", "00101"]
        lstE = ["01111", "10000", "10001", "10010"]
        # registers = ["000", "001", "010", "011", "100", "101", "110", "111"]
        registersdic = {"000": 0, "001": 1, "010": 2, "011": 3, "100": 4, "101": 5, "110": 6, "111": 7}

        if inst == "1001100000000000":
            self.halted = True
            self.nextPC += 1
        else:
            if inst[:5] in lstA:
                if inst[:5] == "00000":
                    x = int(self.registerFile[registersdic[inst[10:13]]], 2) + int(self.registerFile[registersdic[inst[13:16]]], 2)
                    if (x < 0) and (x > 255):
                        self.registerFile[7] = "0000000000001000"
                        self.halted = False
                        self.nextPC += 1
                    else:
                        self.registerFile[registersdic[inst[7:10]]] = format(x, "016b")
                        self.halted = False
                        self.nextPC += 1

                if inst[:5] == "00001":
                    x = int(self.registerFile[registersdic[inst[10:13]]], 2) - int(self.registerFile[registersdic[inst[13:16]]], 2)
                    if (x < 0) and (x > 255):
                        self.registerFile[7] = "0000000000001000"
                        self.halted = False
                        self.nextPC += 1
                    else:
                        self.registerFile[registersdic[inst[7:10]]] = format(x, "016b")
                        self.halted = False
                        self.nextPC += 1

                if inst[:5] == "00110":
                    x = int(self.registerFile[registersdic[inst[10:13]]], 2) * int(self.registerFile[registersdic[inst[13:16]]], 2)
                    if (x < 0) and (x > 255):
                        self.registerFile[7] = "0000000000001000"
                        self.halted = False
                        self.nextPC += 1
                    else:
                        self.registerFile[registersdic[inst[7:10]]] = format(x, "016b")
                        self.halted = False
                        self.nextPC += 1

                if inst[:5] == "01010":
                    x = int(self.registerFile[registersdic[inst[10:13]]], 2) ^ int(self.registerFile[registersdic[inst[13:16]]], 2)
                    self.registerFile[registersdic[inst[7:10]]] = format(x, "016b")
                    self.halted = False
                    self.nextPC += 1

                if inst[:5] == "01011":
                    x = int(self.registerFile[registersdic[inst[10:13]]], 2) | int(self.registerFile[registersdic[inst[13:16]]], 2)
                    self.registerFile[registersdic[inst[8:11]]] = format(x, "016b")
                    self.halted = False
                    self.nextPC += 1

                if inst[:5] == "01100":
                    x = int(self.registerFile[registersdic[inst[10:13]]], 2) & int(self.registerFile[registersdic[inst[13:16]]], 2)
                    self.registerFile[registersdic[inst[7:10]]] = format(x, "016b")
                    self.halted = False
                    self.nextPC += 1

            if inst[:5] in lstB:
                if inst[:5] == "00010":
                    self.registerFile[registersdic[inst[5:8]]] = "00000000" + inst[8:16]
                    self.halted = False
                    self.nextPC += 1

                if inst[:5] == "01000":
                    x = int(self.registerFile[registersdic[inst[5:8]]], 2) >> int(inst[8:16], 2)
                    self.registerFile[registersdic[inst[7:10]]] = format(x, "016b")
                    self.halted = False
                    self.nextPC += 1

                if inst[:5] == "01001":
                    x = int(self.registerFile[registersdic[inst[5:8]]], 2) << int(inst[8:16], 2)
                    self.registerFile[registersdic[inst[7:10]]] = format(x, "016b")
                    self.halted = False
                    self.nextPC += 1

            if inst[:5] in lstC:

                if inst[:5] == "00011":
                    s = self.registerFile[registersdic[inst[13:16]]]
                    self.registerFile[registersdic[inst[10:13]]] = s
                    self.registerFile[registersdic[inst[13:16]]] = "0000000000000000"
                    self.halted = False
                    self.nextPC += 1

                if inst[:5] == "00111":
                    x = int(self.registerFile[registersdic[inst[10:13]]], 2) / int(self.registerFile[registersdic[inst[13:16]]], 2)
                    y = int(self.registerFile[registersdic[inst[10:13]]], 2) % int(self.registerFile[registersdic[inst[13:16]]], 2)
                    self.registerFile[0] = format(x, "016b")
                    self.registerFile[1] = format(y, "016b")
                    self.halted = False
                    self.nextPC += 1

                if inst[:5] == "01101":
                    x = ~ int(self.registerFile[registersdic[inst[13:16]]], 2)
                    self.registerFile[registersdic[inst[10:13]]] = format(x, "016b")
                    self.halted = False
                    self.nextPC += 1

                if inst[:5] == "01110":
                    if int(self.registerFile[registersdic[inst[10:13]]], 2) == int(self.registerFile[registersdic[inst[13:16]]], 2):
                        self.registerFile[7] = "0000000000000001"

                    if int(self.registerFile[registersdic[inst[10:13]]], 2) > int(self.registerFile[registersdic[inst[13:16]]], 2):
                        self.registerFile[7] = "0000000000000010"

                    if int(self.registerFile[registersdic[inst[10:13]]], 2) < int(self.registerFile[registersdic[inst[13:16]]], 2):
                        self.registerFile[7] = "0000000000000100"

                    self.halted = False
                    self.nextPC += 1
                # regis[1] = inst[11:14]
                # regis[2] = inst[14:17]

            if inst[:5] in lstD:
                # 4 var x
                # 0 mov R1 $5   var_addr = 4
                # 1 st R1 x     var_value = R1(001 : 1) = $5 = 0000000000000101
                # 2 ld R2 x
                # 3 hlt
                if inst[:5] == "00101":  # store reg1 x
                    var_addr = int(inst[8:16], 2)
                    var_value = self.registerFile[registersdic[inst[5:8]]]
                    self.memory[var_addr] = var_value
                    self.halted = False
                    self.nextPC += 1

                if inst[:5] == "00100":  # load reg2 x --> reg2==reg1
                    var_addr = int(inst[8:16], 2)
                    var_value = self.memory[var_addr]
                    self.registerFile[registersdic[inst[6:9]]] = var_value
                    self.halted = False
                    self.nextPC += 1

                # regis[0] = inst[6:9]
                # regis[1] = inst[9:17]

            if inst[:5] in lstE:
                if inst[:5] == "01111":
                    self.registerFile[7] = "0000000000000000"
                    self.halted = False
                    self.nextPC = int(inst[8:16], 2)

                if inst[:5] == "10000":
                    self.registerFile[7] = "0000000000000000"
                    self.halted = False
                    self.nextPC = int(inst[8:16], 2)

                if inst[:5] == "10001":
                    self.registerFile[7] = "0000000000000000"
                    self.halted = False
                    self.nextPC = int(inst[8:16], 2)

                if inst[:5] == "10010":
                    self.registerFile[7] = "0000000000000000"
                    self.halted = False
                    self.nextPC = int(inst[8:16], 2)

        return self.halted, self.nextPC


def main():
    memory = Memory()
    registerFile = RegisterFile()
    executionEngine = ExecutionEngine(memory, registerFile)
    PC = ProgramCounter(0)
    halted = False
    cycle = 0

    while not halted:
        inst = memory.fetch(PC.getVal(), cycle)
        halted, nextPC = executionEngine.execute(inst, cycle)
        PC.dump()
        registerFile.dump()
        PC.update(nextPC)
        cycle += 1

    memory.dump()
    memory.showTraces()


if __name__ == '__main__':
    main()