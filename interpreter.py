#-------------------------------------------------------------------------------
# Name:        interpreter
# Purpose:     IPPe final project - Three code address interpreter
#
# Author:      Guillermo Montes Martos (xmonte03)
# Created:     April 18
#-------------------------------------------------------------------------------


import sys
import xml.etree.ElementTree as etree
from _elementtree import ParseError


class Interpreter:

    def __init__(self, input):
        try:
            self.program = etree.parse(input).getroot()
        except ParseError:
            print('Error during the parsing of XML, invalid XML input or file cannot be opened.', file=sys.stderr)
            exit(3)
        self.variables = {}
        self.labels = {}
        self.pc = 0
        self.data_stack = []
        self.call_stack = []


    def run(self):
        self.read_labels()
        self.check_args()
        while self.pc < len(self.program):
            op = self.program[self.pc].attrib['opcode']
            if op == 'MOV':
                self.mov(self.program[self.pc])
            elif op == 'ADD':
                self.add(self.program[self.pc])
            elif op == 'SUB':
                self.sub(self.program[self.pc])
            elif op == 'MUL':
                self.mul(self.program[self.pc])
            elif op == 'DIV':
                self.div(self.program[self.pc])
            elif op == 'READINT':
                self.read_int(self.program[self.pc])
            elif op == 'PRINT':
                self.print_(self.program[self.pc])
            elif op == 'LABEL':
                self.label(self.program[self.pc])
            elif op == 'JUMP':
                self.jump(self.program[self.pc])
            elif op == 'JUMPIFEQ':
                self.jumpifeq(self.program[self.pc])
            elif op == 'JUMPIFGR':
                self.jumpifgr(self.program[self.pc])
            elif op == 'CALL':
                self.call(self.program[self.pc])
            elif op == 'RETURN':
                self.return_(self.program[self.pc])
            elif op == 'PUSH':
                self.push(self.program[self.pc])
            elif op == 'POP':
                self.pop(self.program[self.pc])
            elif op == 'READSTR':
                self.readstr(self.program[self.pc])
            elif op == 'CONCAT':
                self.concat(self.program[self.pc])
            elif op == 'GETAT':
                self.getat(self.program[self.pc])
            elif op == 'LEN':
                self.len(self.program[self.pc])
            elif op == 'STRINT':
                self.strint(self.program[self.pc])
            elif op == 'INTSTR':
                self.intstr(self.program[self.pc])
            else:
                print('Semantic Error during the semantic checks: invalid operation.', file=sys.stderr)
                exit(5)
            self.pc += 1
            #print(op + ' | pc='+str(self.pc-1))
            #print(self.data_stack)
            #print(self.variables)

    def read_labels(self):
        for i in range(len(self.program)):
            if self.program[i].attrib['opcode'] == 'LABEL':
                if self.program[i].find('dst').text in self.labels:
                    print("Semantic Error during the semantic checks: label duplicated", file=sys.stderr)
                    exit(5)
                elif self.program[i].find('dst').attrib['kind'] != 'literal' or self.program[i].find('dst').attrib['type'] != 'string':
                    print("Run-time Error: Operands of incompatible type.", file=sys.stderr)
                    exit(14)
                else:
                    self.labels[self.program[i].find('dst').text] = i


    def check_args(self):
        for taci in self.program:
            if len(taci.attrib) > 3:
                print('Semantic Error during the semantic checks: more arguments than needed.', file=sys.stderr)
                exit(5)
            for arg in taci:
                if arg.tag not in ['src1', 'src2', 'dst']:
                    print("Semantic Error during the semantic checks: bad syntax for arguments.", file=sys.stderr)
                    exit(5)
                elif arg.attrib['kind'] == 'variable' and not (not arg.text[0].isdigit() and all(c.isalnum() or c == '_' for c in arg.text)):
                    print('Semantic Error during the semantic checks: invalid variable name: ' + arg.text, file=sys.stderr)
                    exit(5)


    def get_src_value(self, src):
        if src.attrib['kind'] == 'variable':
            try:
                return self.variables[src.text]
            except KeyError:
                print("Run-time Error: Read access to non-defined or non-initialized variable." + src.text, file=sys.stderr)
                exit(11)
        else:
            if src.attrib['type'] == 'integer':
                try:
                    return int(src.text)
                except ValueError:
                    print("Run-time Error: Invalid literal for a integer", file=sys.stderr)
                    exit(20)
            else:
                return src.text


    def mov(self, command):
        if command.find('dst') is None or command.find('src1') is None:
            print('Semantic Error during the semantic checks: bad syntax for arguments.', file=sys.stderr)
            exit(5)
        if command.find('dst').attrib['kind'] == 'variable':
            self.variables[command.find('dst').text] = self.get_src_value(command.find('src1'))
        else:
            print("Run-time Error: Operands of incompatible type.", file=sys.stderr)
            exit(14)


    def add(self, command):
        if command.find('dst') is None or command.find('src1') is None or command.find('src2') is None:
            print('Semantic Error during the semantic checks: bad syntax for arguments.', file=sys.stderr)
            exit(5)
        if all(arg.attrib['type'] == 'integer' for arg in command) and command.find('dst').attrib['kind'] == 'variable':
            src1 = self.get_src_value(command.find('src1'))
            src2 = self.get_src_value(command.find('src2'))
            self.variables[command.find('dst').text] = src1 + src2
        else:
            print("Run-time Error: Operands of incompatible type.", file=sys.stderr)
            exit(14)


    def sub(self, command):
        if command.find('dst') is None or command.find('src1') is None or command.find('src2') is None:
            print('Semantic Error during the semantic checks: bad syntax for arguments.', file=sys.stderr)
            exit(5)
        if all(arg.attrib['type'] == 'integer' for arg in command) and command.find('dst').attrib['kind'] == 'variable':
            src1 = self.get_src_value(command.find('src1'))
            src2 = self.get_src_value(command.find('src2'))
            self.variables[command.find('dst').text] = src1 - src2
        else:
            print("Run-time Error: Operands of incompatible type.", file=sys.stderr)
            exit(14)


    def mul(self, command):
        if command.find('dst') is None or command.find('src1') is None or command.find('src2') is None:
            print('Semantic Error during the semantic checks: bad syntax for arguments.', file=sys.stderr)
            exit(5)
        if all(arg.attrib['type'] == 'integer' for arg in command) and command.find('dst').attrib['kind'] == 'variable':
            src1 = self.get_src_value(command.find('src1'))
            src2 = self.get_src_value(command.find('src2'))
            self.variables[command.find('dst').text] = src1 * src2
        else:
            print("Run-time Error: Operands of incompatible type.", file=sys.stderr)
            exit(14)


    def div(self, command):
        if command.find('dst') is None or command.find('src1') is None or command.find('src2') is None:
            print('Semantic Error during the semantic checks: bad syntax for arguments.', file=sys.stderr)
            exit(5)
        if all(arg.attrib['type'] == 'integer' for arg in command) and command.find('dst').attrib['kind'] == 'variable':
            src1 = self.get_src_value(command.find('src1'))
            src2 = self.get_src_value(command.find('src2'))
            try:
                self.variables[command.find('dst').text] = int(src1 / src2)
            except ZeroDivisionError:
                print("Run-time Error: Division by zero using DIV instruction.", file=sys.stderr)
                exit(12)
        else:
            print("Run-time Error: Operands of incompatible type.", file=sys.stderr)
            exit(14)


    def read_int(self, command):
        if command.find('dst') is None:
            print('Semantic Error during the semantic checks: bad syntax for arguments.', file=sys.stderr)
            exit(5)
        if command.find('dst').attrib['kind'] == 'variable' and command.find('dst').attrib['type'] == 'integer':
            try:
                self.variables[command.find('dst').text] = int(input(command.find('dst').text + ' = '))
            except ValueError:
                print("Run-time Error: READINT get invalid value.", file=sys.stderr)
                exit(13)
        else:
            print("Run-time Error: Operands of incompatible type.", file=sys.stderr)
            exit(14)


    def print_(self, command):
        if command.find('src1') is None:
            print('Semantic Error during the semantic checks: bad syntax for arguments.', file=sys.stderr)
            exit(5)
        print(str( self.get_src_value(command.find('src1')) ))


    def label(self, command):
        return


    def jump(self, command):
        if command.find('dst') is None:
            print('Semantic Error during the semantic checks: bad syntax for arguments.', file=sys.stderr)
            exit(5)
        if command.find('dst').attrib['kind'] != 'literal' or command.find('dst').attrib['type'] != 'string':
            print("Run-time Error: Operands of incompatible type.", file=sys.stderr)
            exit(14)
        elif command.find('dst').text not in self.labels:
            print("Run-time Error: Jump to a non-existing label or call to non-existing function.", file=sys.stderr)
            exit(10)
        else:
            self.pc = self.labels[command.find('dst').text]


    def jumpifeq(self, command):
        if command.find('dst') is None or command.find('src1') is None or command.find('src2') is None:
            print('Semantic Error during the semantic checks: bad syntax for arguments.', file=sys.stderr)
            exit(5)
        if command.find('src1').attrib['type'] != command.find('src2').attrib['type'] or command.find('dst').attrib['type'] != 'string' or command.find('dst').attrib['kind'] != 'literal':
            print('Run-time Error: Operands of incompatible type.', file=sys.stderr)
            exit(14)
        else:
            src1 = self.get_src_value(command.find('src1'))
            src2 = self.get_src_value(command.find('src2'))
            if src1 == src2:
                try:
                    self.pc = self.labels[command.find('dst').text]
                except KeyError:
                    print('Run-time Error: Jump to a non-existing label or call to non-existing function.', file=sys.stderr)
                    exit(10)


    def jumpifgr(self, command):
        if command.find('dst') is None or command.find('src1') is None or command.find('src2') is None:
            print('Semantic Error during the semantic checks: bad syntax for arguments.', file=sys.stderr)
            exit(5)
        if command.find('src1').attrib['type'] != command.find('src2').attrib['type'] or command.find('dst').attrib['type'] != 'string' or command.find('dst').attrib['kind'] != 'literal':
            print('Run-time Error: Operands of incompatible type.', file=sys.stderr)
            exit(14)
        else:
            src1 = self.get_src_value(command.find('src1'))
            src2 = self.get_src_value(command.find('src2'))
            if src1 > src2:
                try:
                    self.pc = self.labels[command.find('dst').text]
                except KeyError:
                    print('Run-time Error: Jump to a non-existing label or call to non-existing function.', file=sys.stderr)
                    exit(10)


    def call(self, command):
        if command.find('dst') is None:
            print('Semantic Error during the semantic checks: bad syntax for arguments.', file=sys.stderr)
            exit(5)
        if command.find('dst').attrib['kind'] != 'literal' or command.find('dst').attrib['type'] != 'string':
            print("Run-time Error: Operands of incompatible type.", file=sys.stderr)
            exit(14)
        elif command.find('dst').text not in self.labels:
            print("Run-time Error: Jump to a non-existing label or call to non-existing function.", file=sys.stderr)
            exit(10)
        else:
            self.call_stack.append(self.pc)
            self.pc = self.labels[command.find('dst').text]


    def return_(self, command):
        if len(self.call_stack) == 0:
            print('Run-time Error: Pop from the empty call stack is forbidden', file=sys.stderr)
            exit(15)
        else:
            self.pc = self.call_stack.pop()


    def push(self, command):
        if command.find('src1') is None:
            print('Semantic Error during the semantic checks: bad syntax for arguments.', file=sys.stderr)
            exit(5)

        self.data_stack.append(self.get_src_value(command.find('src1')))


    def pop(self, command):
        if command.find('dst') is None:
            print('Semantic Error during the semantic checks: bad syntax for arguments.', file=sys.stderr)
            exit(5)
        if command.find('dst').attrib['kind'] != 'variable':
            print("Run-time Error: Operands of incompatible type.", file=sys.stderr)
            exit(14)
        elif len(self.data_stack) == 0:
            print('Run-time Error: Pop from the empty data stack is forbidden', file=sys.stderr)
            exit(15)
        else:
            self.variables[command.find('dst').text] = self.data_stack.pop()


    def readstr(self, command):
        if command.find('dst') is None:
            print('Semantic Error during the semantic checks: bad syntax for arguments.', file=sys.stderr)
            exit(5)
        if command.find('dst').attrib['kind'] == 'variable' and command.find('dst').attrib['type'] == 'string':
            self.variables[command.find('dst').text] = input(command.find('dst').text + ' = ')
        else:
            print("Run-time Error: Operands of incompatible type.", file=sys.stderr)
            exit(14)


    def concat(self, command):
        if command.find('dst') is None or command.find('src1') is None or command.find('src2') is None:
            print('Semantic Error during the semantic checks: bad syntax for arguments.', file=sys.stderr)
            exit(5)
        if command.find('src1').attrib['type'] == command.find('src2').attrib['type'] and command.find('src1').attrib['type'] == 'string' and command.find('dst').attrib['kind'] == 'variable':
            src1 = self.get_src_value(command.find('src1'))
            src2 = self.get_src_value(command.find('src2'))
            self.variables[command.find('dst').text] = src1 + src2
        else:
            print('Run-time Error: Operands of incompatible type.', file=sys.stderr)
            exit(14)


    def getat(self, command):
        if command.find('dst') is None or command.find('src1') is None or command.find('src2') is None:
            print('Semantic Error during the semantic checks: bad syntax for arguments.', file=sys.stderr)
            exit(5)
        if command.find('src1').attrib['type'] == 'string' and command.find('src2').attrib['type'] == 'integer' and command.find('dst').attrib['kind'] == 'variable':
            src1 = self.get_src_value(command.find('src1'))
            src2 = self.get_src_value(command.find('src2'))
            try:
                self.variables[command.find('dst').text] = src1[src2]
            except IndexError:
                print("Run-time Error: Index out of bounds.", file=sys.stderr)
                exit(20)
        else:
            print("Run-time Error: Operands of incompatible type.", file=sys.stderr)
            exit(14)


    def len(self, command):
        if command.find('dst') is None or command.find('src1') is None:
            print('Semantic Error during the semantic checks: bad syntax for arguments.', file=sys.stderr)
            exit(5)
        if command.find('src1').attrib['type'] == 'string' and command.find('dst').attrib['type'] == 'integer' and command.find('dst').attrib['kind'] == 'variable':
            self.variables[command.find('dst').text] = len( self.get_src_value(command.find('src1')) )
        else:
            print("Run-time Error: Operands of incompatible type.", file=sys.stderr)
            exit(14)


    def strint(self, command):
        if command.find('dst') is None or command.find('src1') is None:
            print('Semantic Error during the semantic checks: bad syntax for arguments.', file=sys.stderr)
            exit(5)
        if command.find('src1').attrib['type'] == 'string' and command.find('dst').attrib['type'] == 'integer' and command.find('dst').attrib['kind'] == 'variable':
            try:
                self.variables[command.find('dst').text] = int( self.get_src_value(command.find('src1')) )
            except ValueError:
                print("Run-time Error: Invalid literal for a integer", file=sys.stderr)
                exit(20)
        else:
            print("Run-time Error: Operands of incompatible type.", file=sys.stderr)
            exit(14)


    def intstr(self, command):
        if command.find('dst') is None or command.find('src1') is None:
            print('Semantic Error during the semantic checks: bad syntax for arguments.', file=sys.stderr)
            exit(5)
        if command.find('src1').attrib['type'] == 'integer' and command.find('dst').attrib['type'] == 'string' and command.find('dst').attrib['kind'] == 'variable':
            self.variables[command.find('dst').text] = str( self.get_src_value(command.find('src1')) )
        else:
            print("Run-time Error: Operands of incompatible type.", file=sys.stderr)
            exit(14)