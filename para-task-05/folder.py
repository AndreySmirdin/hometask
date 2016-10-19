from jat.model import *
from jat.printer import *


class ConstantFolder:

    def visit(self, obj):
        return obj.accept(self)

    def visit_list(self, args):
        res = []
        if args:
            for expr in args:
                res.append(expr.accept(self))
        return res

    def visit_number(self, number):
        return number

    def visit_reference(self, reference):
        return reference

    def visit_binaryOperation(self, binary):
        right = binary.rhs.accept(self)
        left = binary.lhs.accept(self)
        if binary.op == '*':
            if isinstance(left, Number) or isinstance(right, Number):
                if isinstance(left, Reference) or isinstance(right, Reference):
                    return Number(0)
        if isinstance(left, Number) and isinstance(right, Number):
            return BinaryOperation(left, binary.op, right).evaluate(None)
        if binary.op == '-' and isinstance(left, Reference):
            if isinstance(right, Reference) and left.name == right.name:
                return Number(0)
        return BinaryOperation(left, binary.op, right)

    def visit_unaryOperation(self, unary):
        expr = unary.expr.accept(self)
        if isinstance(expr, Number):
            return UnaryOperation(unary.op, expr).evaluate(None)
        return UnaryOperation(unary.op, expr)

    def visit_conditional(self, cond):
        new_condition = cond.condition.accept(self)
        new_true = self.visit_list(cond.if_true)
        new_false = self.visit_list(cond.if_false)
        return Conditional(new_condition, new_true, new_false)

    def visit_print(self, pr):
        res = pr.expr.accept(self)
        return Print(res)

    def visit_read(self, read):
        return read

    def visit_functionDefinition(self, defin):
        body = self.visit_list(defin.function.body)
        function = Function(defin.function.args, body)
        return FunctionDefinition(defin.name, function)

    def visit_functionCall(self, call):
        new_args = self.visit_list(call.args)
        new_fun_expr = call.fun_expr.accept(self)
        return FunctionCall(new_fun_expr, new_args)

scope = Scope()
scope['a'] = 239
b1 = BinaryOperation(Reference('a'), '/', Number(2))
b2 = BinaryOperation(Reference('a'), '-', Reference('a'))
b3 = BinaryOperation(Number(4), '*', Number(2))
b4 = BinaryOperation(Reference('a'), '*', Number(0))
b5 = BinaryOperation(Number(0), '*', Reference('a'))
b6 = BinaryOperation(
    Number(4),
    '*',
    BinaryOperation(
        Number(3),
        '+',
        Reference('a')))
printer = PrettyPrinter()
folder = ConstantFolder()
printer.visit(folder.visit(b1))
printer.visit(folder.visit(b2))
printer.visit(folder.visit(b3))
printer.visit(folder.visit(b4))
printer.visit(folder.visit(b5))
printer.visit(folder.visit(b6))
