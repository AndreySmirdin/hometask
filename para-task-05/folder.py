from yat.model import *
from yat.printer import *


class ConstantFolder:

    def visit(self, obj):
        return obj.visit(self)

    def checkAll(self, args):
        res = []
        if args:
            for expr in args:
                res.append(expr.visit(self))
        return res

    def visitNumber(self, number):
        return number

    def visitReference(self, reference):
        return reference

    def visitBinaryOperation(self, binary):
        right = binary.rhs.visit(self)
        left = binary.lhs.visit(self)
        if binary.op == "*":
            if isinstance(left, Number) or isinstance(right, Number):
                if isinstance(left, Reference) or isinstance(right, Reference):
                    return Number(0)
        if isinstance(left, Number) and isinstance(right, Number):
            return BinaryOperation(left, binary.op, right).evaluate(None)
        if binary.op == '-' and isinstance(left, Reference):
            if isinstance(right, Reference) and left.name == right.name:
                return Number(0)
        return BinaryOperation(left, binary.op, right)

    def visitUnaryOperation(self, unary):
        expr = unary.visit(self)
        if isinstance(expr, Number):
            return UnaryOperation(unary.op, expr).evaluate(None)
        return UnaryOperation(unary.op, expr)

    def visitConditional(self, cond):
        new_condition = cond.condition.visit(self)
        new_true = self.checkAll(cond.if_true)
        new_false = self.checkAll(cond.if_false)
        return Conditional(new_condition, new_true, new_false)

    def visitPrint(self, pr):
        res = pr.expr.visit(self)
        return Print(res)

    def visitRead(self, read):
        return read

    def visitFunctionDefinition(self, defin):
        body = self.checkAll(defin.function.body)
        function = Function(defin.function.args, body)
        return FunctionDefinition(defin.name, function)

    def visitFunctionCall(self, call):
        new_args = self.checkAll(call.args)
        new_fun_expr = call.fun_expr.visit(self)
        return FunctionCall(new_fun_expr, new_args)
