from model import *


class PrettyPrinter:

    def __init__(self):
        self.tabs = 0

    def visit(self, expr):
        expr.accept(self)
        print(';')

    def print_indented(self, exprs):
        self.tabs += 1
        for expr in exprs:
            print('    ' * self.tabs, end='')
            expr.accept(self)
            print(';')
        self.tabs -= 1

    def visit_number(self, number):
        print(number.value, end='')

    def visit_reference(self, reference):
        print(reference.name, end='')

    def visit_binaryOperation(self, binary):
        print('(', end='')
        binary.lhs.accept(self)
        print(' ', binary.op, end=' ', sep='')
        binary.rhs.accept(self)
        print(')', end='')

    def visit_unaryOperation(self, unary):
        print('({}'.format(unary.op), end='')
        unary.expr.accept(self)
        print(')', end='')

    def visit_conditional(self, cond):
        print('if (', end='')
        cond.condition.accept(self)
        print(') {')
        if cond.if_true:
            self.print_indented(cond.if_true)
        print('    ' * self.tabs, '} else {', sep='')
        if cond.if_false:
            self.print_indented(cond.if_false)
        print('    ' * self.tabs, '}', end='', sep='')

    def visit_print(self, Print):
        print('print ', end='')
        Print.expr.accept(self)

    def visit_read(self, read):
        print('read ', read.name, end='', sep='')

    def visit_functionDefinition(self, defin):
        print('def ', defin.name, end='', sep='')
        print('(', ', '.join(defin.function.args), ') {', sep='')
        self.print_indented(defin.function.body)
        print('    ' * self.tabs, '}', end='', sep='')

    def visit_functionCall(self, call):
        call.fun_expr.accept(self)
        print('(', end='')
        not_first = False
        for expr in call.args:
            if not_first:
                print(', ', end='')
            expr.accept(self)
            not_first = True
        print(')', end='')
