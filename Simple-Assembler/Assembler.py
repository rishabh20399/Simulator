import sys


def TypeA(instruction, reg1, reg2, reg3):
    dic1 = {"add": "00000", "sub": "00001", "mul": "00110", "xor": "01010", "or": "01011", "and": "01100"}

    dic2 = {"R0": "000", "R1": "001", "R2": "010", "R3": "011", "R4": "100", "R5": "101", "R6": "110", "FLAGS": "111"}

    return dic1[instruction] + "00" + dic2[reg1] + dic2[reg2] + dic2[reg3]


def TypeB(instruction, reg1, immediateValue):
    dic1 = {"mov": "00010", "rs": "01000", "ls": "01001"}

    dic2 = {"R0": "000", "R1": "001", "R2": "010", "R3": "011", "R4": "100", "R5": "101", "R6": "110", "FLAGS": "111"}

    return dic1[instruction] + dic2[reg1] + format(immediateValue, '08b')


def TypeC(instruction, reg1, reg2):
    dic1 = {"mov": "00011", "div": "00111", "not": "01101", "cmp": "01110"}

    dic2 = {"R0": "000", "R1": "001", "R2": "010", "R3": "011", "R4": "100", "R5": "101", "R6": "110", "FLAGS": "111"}

    return dic1[instruction] + "00000" + dic2[reg1] + dic2[reg2]


def TypeD(instruction, reg1, mem_addr):
    dic1 = {"ld": "00100", "st": "00101"}

    dic2 = {"R0": "000", "R1": "001", "R2": "010", "R3": "011", "R4": "100", "R5": "101", "R6": "110", "FLAGS": "111"}

    return dic1[instruction] + dic2[reg1] + format(mem_addr, '08b')


def TypeE(instruction, mem_addr):
    dic1 = {"jmp": "01111", "jlt": "10000", "jgt": "10001", "je": "10010"}

    return dic1[instruction] + "000" + format(mem_addr, '08b')


def mem_address(list1, list2, f):
    for i in range(len(list2)):
        if list2[i][1] == f:
            return len(list1) + i
    return 0


def error_identifier(list1, list2, labels, label_addr):
    code = []
    code.extend(list2)
    code.extend(list1)

    var = []
    for i in range(len(list2)):
        var.append(list2[i][1])

    list_typeA = ['add', 'sub', 'mul', 'xor', 'or', 'and']
    list_typeB = ['mov', 'rs', 'ls']
    list_typeC = ["mov", "div", "not", "cmp"]
    list_typeD = ["ld", "st"]
    list_typeE = ["jmp", "jlt", "jgt", "je"]
    list_register = ['R0', 'R1', 'R2', 'R3', 'R4', 'R5', 'R6', 'FLAGS']

    checker = False
    temp = True
    tempvar = True
    end = len(code) - 1
    count_hlt = 0
    s = 0

    if len(var) != len(list(set(var))):
        checker = True
        sys.stdout.write("Error>> Misuse of variables\n")

    if len(labels) != len(list(set(labels))):
        checker = True
        sys.stdout.write("Error>> Misuse of labels\n")

    for k in range(len(code)):
        if code[k][0] != "var":
            tempvar = False

        if s < len(label_addr) and k == label_addr[s]:
            temp1 = True
            for i in range(len(labels[s])):
                if not labels[s][i].isalnum() and labels[s][i] != "_":
                    temp1 = False
                    break
            if not temp1:
                checker = True
                sys.stdout.write("Error>> Line:" + str(k + 1) + " not a correct label name\n")
            s += 1

        if len(code[k]) > 4:
            checker = True
            sys.stdout.write("Error>> Line: " + str(k + 1) + " Wrong syntax used for instructions\n")

        elif (len(code[k])) == 4:
            if code[k][0] not in list_typeA and code[k][0][-1] != ":":
                checker = True
                sys.stdout.write("Error>> Line: " + str(k + 1) + " Typos in instruction name\n")

            if code[k][0] in list_typeA:
                if (code[k][1] not in list_register) or (code[k][2] not in list_register) or (code[k][3] not in list_register):
                    checker = True
                    sys.stdout.write("Error>> Line: " + str(k + 1) + " Typos in register name\n")

                if code[k][1] == "FLAGS":
                    checker = True
                    sys.stdout.write("Error>> Line: " + str(k + 1) + " Illegal use of FLAGS register\n")

        elif (len(code[k])) == 3:
            if (code[k][0] not in list_typeB) and (code[k][0] not in list_typeC) and (code[k][0] not in list_typeD):
                checker = True
                sys.stdout.write("Error>> Line: " + str(k + 1) + " Wrong syntax used for instructions\n")

            if code[k][0] in list_typeB:
                if code[k][1] == "FLAGS":
                    checker = True
                    sys.stdout.write("Error>> Line: " + str(k + 1) + " Illegal use of FLAGS register\n")

                if code[k][1] not in list_register:
                    checker = True
                    sys.stdout.write("Error>> Line: " + str(k + 1) + " Typos in register name\n")

                if code[k][2][0] == "$":
                    if int(code[k][2][1:]) > 255 or int(code[k][2][1:]) < 0:
                        checker = True
                        sys.stdout.write("Error>> Line: " + str(k + 1) + " Illegal Immediate values (less than 0 or more than 255)\n")

                if code[k][2][0] != "F" and code[k][2][0] != "R" and code[k][2][0] != "$":
                    checker = True
                    sys.stdout.write("Error>> Line: " + str(k + 1) + " Wrong syntax for Immediate values\n")

            if (code[k][0] in list_typeC) and code[k][2][0] != "$":
                if (code[k][1] not in list_register) or (code[k][2] not in list_register):
                    checker = True
                    sys.stdout.write("Error>> Line: " + str(k + 1) + " Typos in register name\n")

            if code[k][0] in list_typeC:
                if code[k][1] == "FLAGS":
                    if code[k][2][0] != "$":
                        checker = True
                        sys.stdout.write("Error>> Line: " + str(k + 1) + " Illegal use of FLAGS register\n")

            if code[k][0] in list_typeD:
                if code[k][1] not in list_register:
                    checker = True
                    sys.stdout.write("Error>> Line: " + str(k + 1) + " Typos in register name\n")

                if (code[k][0] == "ld") and (code[k][1] == "FLAGS"):
                    checker = True
                    sys.stdout.write("Error>> Line: " + str(k + 1) + " Illegal use of FLAGS register\n")

                if code[k][2] not in var:
                    checker = True
                    sys.stdout.write("Error>> Line: " + str(k + 1) + " Use of undefined variables\n")

                if code[k][2] in labels:
                    checker = True
                    sys.stdout.write("Error>> Line: " + str(k + 1) + " Misuse of labels as variables or vice-versa\n")

        elif (len(code[k])) == 2:
            if code[k][0] not in list_typeE and code[k][0] != "var":
                checker = True
                sys.stdout.write("Error>> Line: " + str(k + 1) + " Wrong syntax used for instructions\n")

            if code[k][0] in list_typeE:
                if code[k][1] not in labels:
                    checker = True
                    sys.stdout.write("Error>> Line: " + str(k + 1) + " Use of undefined labels\n")

                if code[k][1] in var:
                    checker = True
                    sys.stdout.write("Error>> Line: " + str(k + 1) + " Misuse of labels as variables or vice-versa\n")

            if code[k][0] == "var":
                if not tempvar:
                    checker = True
                    sys.stdout.write("Error>> Line: " + str(k + 1) + " Variable not defined at the beginning\n")

        elif code[k][0] == 'hlt':
            count_hlt += 1
            temp = False
        else:
            checker = True
            sys.stdout.write("Error>> Line: " + str(k + 1) + " Wrong syntax used for instructions\n")

    if temp:
        checker = True
        sys.stdout.write("Error>> Missing hlt instruction\n")

    if not temp and code[end][0] != "hlt":
        checker = True
        sys.stdout.write("Error>> hlt not being used as the last instruction\n")
    if count_hlt > 1:
        checker = True
        sys.stdout.write("Error>> Wrong syntax used for instructions\n")

    return checker


def ans(list1, list2, labels, labels_addr):
    for i in list1:
        if i[0] == "hlt":
            sys.stdout.write("1001100000000000" + "\n")
            break

        if len(i) == 4:
            if i[0] == "add" or i[0] == "mul" or i[0] == "and" or i[0] == "sub" or i[0] == "xor" or i[0] == "or":
                sys.stdout.write(TypeA(i[0], i[1], i[2], i[3]) + "\n")

        elif len(i) == 3:
            if i[0] == "mov":
                if i[2][0] == "$":
                    sys.stdout.write(TypeB(i[0], i[1], int(i[2][1:])) + "\n")
                else:
                    sys.stdout.write(TypeC(i[0], i[1], i[2]) + "\n")

            elif i[0] == "rs" or i[0] == "ls":
                sys.stdout.write(TypeB(i[0], i[1], int(i[2][1:])) + "\n")

            elif i[0] == "div" or i[0] == "not" or i[0] == "cmp":
                sys.stdout.write(TypeC(i[0], i[1], i[2]) + "\n")

            elif i[0] == "ld" or i[0] == "st":
                sys.stdout.write(TypeD(i[0], i[1], mem_address(list1, list2, i[2])) + "\n")

        elif len(i) == 2:
            if i[0] == "jmp" or i[0] == "jlt" or i[0] == "jgt" or i[0] == "je":
                label_addr = 0
                for j in range(len(labels)):
                    if i[1] == labels[j]:
                        label_addr = labels_addr[j]
                sys.stdout.write(TypeE(i[0], label_addr) + "\n")


def main():
    list1 = []
    list2 = []
    labels = []
    labels_addr = []
    count = 0
    temp_var_main = False
    while True:
        try:
            s = input()
            if s == "":
                continue
            else:
                p = s.split(" ")
                if p[0] != "var":
                    temp_var_main = True

                if (p[0] == "var") and not temp_var_main and len(p) == 2:
                    list2.append(p)

                if p[0] == "var" and temp_var_main:
                    list1.append(p)

                elif len(p) > 1:
                    if p[0][-1] == ":" and p[1] == "hlt":
                        labels.append(p[0][:-1])
                        labels_addr.append(count)
                        list1.append([p[1]])
                        count += 1

                    elif p[0][-1] == ":":
                        labels.append(p[0][:-1])
                        labels_addr.append(count)
                        p.remove(p[0])
                        list1.append(p)
                        count += 1
                    elif p[0] != "var":
                        list1.append(p)
                        count += 1
                elif len(p) == 1:
                    list1.append(p)

        except EOFError:
            break

    if not error_identifier(list1, list2, labels, labels_addr):
        ans(list1, list2, labels, labels_addr)


if __name__ == '__main__':
    main()
