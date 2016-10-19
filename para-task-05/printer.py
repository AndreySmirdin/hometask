from jat.model import *


class PrettyPrinter():

    def __init__(self):
        self.tabs = 0

    def visit(self, expr):
        expr.visit(self)
        print(';')

    def print_indented(self, exprs):
        self.tabs += 1
        for expr in exprs:
            print('    ' * self.tabs, end='')
            expr.visit(self)
            print(';')
        self.tabs -= 1

    def accept_number(self, number):
        print(number.value, end='')

    def accept_reference(self, reference):
        print(reference.name, end='')

    def accept_binaryOperation(self, binary):
        print('(', end='')
        binary.lhs.visit(self)
        print(' ', binary.op, end=' ', sep='')
        binary.rhs.visit(self)
        print(')', end='')

    def accept_unaryOperation(self, unary):
        print('({}'.format(unary.op), end='')
        unary.expr.visit(self)
        print(')', end='')

    def accept_conditional(self, cond):
        print('if (', end='')
        cond.condition.visit(self)
        print(') {')
        if cond.if_true:
            self.print_indented(cond.if_true)
        print('    ' * self.tabs, '} else {', sep='')
        if cond.if_false:
            self.print_indented(cond.if_false)
        print('    ' * self.tabs, '}', end='', sep='')

    def accept_print(self, Print):
        print('print ', end='')
        Print.expr.visit(self)

    def accept_read(self, read):
        print('read ', read.name, end='', sep='')

    def accept_functionDefinition(self, defin):
        print('def ', defin.name, end='', sep='')
        print ('(', ', '.join(defin.function.args), ') {', sep='')
        self.print_indented(defin.function.body)
        print('    ' * self.tabs, '}', end='', sep='')

    def accept_functionCall(self, call):
        call.fun_expr.visit(self)
        print('(', end='')
        not_first = False
        for expr in call.args:
            if not_first:
                print(', ', end='')
            expr.visit(self)
            not_first = True
        print(')', end='')
