#! /usr/bin/env python
# -*- coding: utf-8 -*-
class Scope:

    def __init__(self, parent=None):
        self.dic = {}
        self.parent = parent

    def __getitem__(self, key):
        if key in self.dic:
            return self.dic[key]
        elif self.parent:
            return self.parent[key]

    def __setitem__(self, key, value):
        self.dic[key] = value


class Number:

    def __init__(self, value):
        self.value = value

    def evaluate(self, scope):
        return self

    def accept(self, visitor):
        return visitor.visit_number(self)


class Function:

    def __init__(self, args, body):
        self.args = args
        self.body = body

    def evaluate(self, scope):
        res = Number(0)
        for expr in self.body:
            res = expr.evaluate(scope)
        return res


class FunctionDefinition:

    def __init__(self, name, function):
        self.name = name
        self.function = function

    def evaluate(self, scope):
        scope[self.name] = self.function
        return self.function

    def accept(self, visitor):
        return visitor.visit_function_definition(self)


class Conditional:

    def __init__(self, condtion, if_true, if_false=None):
        self.condition = condtion
        self.if_true = if_true
        self.if_false = if_false

    def evaluate(self, scope):
        cond = self.condition.evaluate(scope)
        res = Number(0)
        if cond.value:
            expr = self.if_true
        else:
            expr = self.if_false
        if expr:
            for term in expr:
                res = term.evaluate(scope)
            return res
        else:
            return Number(0)

    def accept(self, visitor):
        return visitor.visit_conditional(self)


class Print:

    def __init__(self, expr):
        self.expr = expr

    def evaluate(self, scope):
        res = self.expr.evaluate(scope)
        print(res.value)
        return res

    def accept(self, visitor):
        return visitor.visit_print(self)


class Read:

    def __init__(self, name):
        self.name = name

    def evaluate(self, scope):
        inp = int(input())
        scope[self.name] = Number(inp)
        return Number(inp)

    def accept(self, visitor):
        return visitor.visit_read(self)


class FunctionCall:

    def __init__(self, fun_expr, args):
        self.fun_expr = fun_expr
        self.args = args

    def evaluate(self, scope):
        function = self.fun_expr.evaluate(scope)
        call_scope = Scope(scope)
        for name, arg in zip(function.args, self.args):
            call_scope[name] = arg.evaluate(scope)
        return function.evaluate(call_scope)

    def accept(self, visitor):
        return visitor.visit_function_call(self)


class Reference:

    def __init__(self, name):
        self.name = name

    def evaluate(self, scope):
        return scope[self.name]

    def accept(self, visitor):
        return visitor.visit_reference(self)


class BinaryOperation:

    operation = {'+': lambda x, y: x.value + y.value,
                 '-': lambda x, y: x.value - y.value,
                 '*': lambda x, y: x.value * y.value,
                 '/': lambda x, y: x.value // y.value,
                 '%': lambda x, y: x.value % y.value,
                 '==': lambda x, y: int(x.value == y.value),
                 '!=': lambda x, y: int(x.value != y.value),
                 '<': lambda x, y: int(x.value < y.value),
                 '<=': lambda x, y: int(x.value <= y.value),
                 '>=': lambda x, y: int(x.value >= y.value),
                 '>': lambda x, y: int(x.value > y.value),
                 '&&': lambda x, y: int(x.value and y.value),
                 '||': lambda x, y: int(x.value or y.value)}

    def __init__(self, lhs, op, rhs):
        self.op = op
        self.lhs = lhs
        self.rhs = rhs

    def evaluate(self, scope):
        left = self.lhs.evaluate(scope)
        right = self.rhs.evaluate(scope)
        return Number(self.operation[self.op](left, right))

    def accept(self, visitor):
        return visitor.visit_binary_operation(self)


class UnaryOperation:

    operation = {'-': lambda x: -x.value,
                 '!': lambda x: int(not x.value)}

    def __init__(self, op, expr):
        self.op = op
        self.expr = expr

    def evaluate(self, scope):
        return Number(self.operation[self.op](self.expr.evaluate(scope)))

    def accept(self, visitor):
        return visitor.visit_unary_operation(self)
