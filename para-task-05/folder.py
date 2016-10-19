from jat.model import *
from jat.printer import *


class ConstantFolder:

    def visit(self, obj):
        return obj.visit(self)

    def accept_list(self, args):
        res = []
        if args:
            for expr in args:
                res.append(expr.visit(self))
        return res

    def accept_number(self, number):
        return number

    def accept_reference(self, reference):
        return reference

    def accept_binaryOperation(self, binary):
        right = binary.rhs.visit(self)
        left = binary.lhs.visit(self)
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

    def accept_unaryOperation(self, unary):
        expr = unary.expr.visit(self)
        if isinstance(expr, Number):
            return UnaryOperation(unary.op, expr).evaluate(None)
        return UnaryOperation(unary.op, expr)

    def accept_conditional(self, cond):
        new_condition = cond.condition.visit(self)
        new_true = self.accept_list(cond.if_true)
        new_false = self.accept_list(cond.if_false)
        return Conditional(new_condition, new_true, new_false)

    def accept_print(self, pr):
        res = pr.expr.visit(self)
        return Print(res)

    def accept_read(self, read):
        return read

    def accept_functionDefinition(self, defin):
        body = self.accept_list(defin.function.body)
        function = Function(defin.function.args, body)
        return FunctionDefinition(defin.name, function)

    def accept_functionCall(self, call):
        new_args = self.accept_list(call.args)
        new_fun_expr = call.fun_expr.visit(self)
        return FunctionCall(new_fun_expr, new_args)
