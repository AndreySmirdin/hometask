from yat.model import *


class PrettyPrinter():
    tabs = 0

    def visit(self, expr):
        expr.visit(self)
        print(";")

    def print_tabbed(self, exprs):
        self.tabs += 1
        for expr in exprs:
            print("    " * self.tabs, end='')
            expr.visit(self)
            print(';')
        self.tabs -= 1

    def visitNumber(self, number):
        print(number.value, end='')

    def visitReference(self, reference):
        print(reference.name, end='')

    def visitBinaryOperation(self, binary):
        print('(', end='')
        binary.lhs.visit(self)
        print(binary.op, end='')
        binary.rhs.visit(self)
        print(')', end='')

    def visitUnaryOperation(self, unary):
        print('({}'.format(unary.op), end='')
        unary.expr.visit(self)
        print(')', end='')

    def visitConditional(self, cond):
        print("if (", end='')
        cond.condition.visit(self)
        print(") {")
        if cond.if_true:
            self.print_tabbed(cond.if_true)
        print("    " * self.tabs, "} else {")
        if cond.if_false:
            self.print_tabbed(cond.if_false)
        print("    " * self.tabs, "}", end='')

    def visitPrint(self, Print):
        print("print ", end='')
        Print.expr.visit(self)

    def visitRead(self, read):
        print("read ", read.name, end='')

    def visitFunctionDefinition(self, defin):
        print("def ", defin.name, end='')
        print ("(", ', '.join(defin.function.args), ")  {")
        self.print_tabbed(defin.function.body)
        print("    " * self.tabs, "}", end='')

    def visitFunctionCall(self, call):
        call.fun_expr.visit(self)
        print("(", end='')
        not_first = False
        for expr in call.args:
            if not_first:
                print(", ", end='')
            expr.visit(self)
            not_first = True
        print(")", end='')
