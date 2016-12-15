from model import *
import pytest
import sys
from io import StringIO


def get_v(n):
    sys.stdout = StringIO()
    Print(n).evaluate(None)
    res = int(sys.stdout.getvalue())
    return res


class TestPrint:

    def test_print_number(self, monkeypatch):
        monkeypatch.setattr(sys, "stdout", StringIO())
        Print(Number(5)).evaluate(None)
        assert sys.stdout.getvalue() == "5\n"

    def test_print_reference(self, monkeypatch):
        monkeypatch.setattr(sys, "stdout", StringIO())
        scope = Scope()
        scope["a"] = Number(5)
        Print(Reference("a")).evaluate(scope)
        assert sys.stdout.getvalue() == "5\n"


class TestRead:

    def test_read(self, monkeypatch):
        scope = Scope()
        monkeypatch.setattr(sys, "stdin", StringIO("239"))
        Read("n").evaluate(scope)
        assert get_v(Reference("n").evaluate(scope)) == 239


class TestBinaryOperation:

    def test_sum(self):
        assert get_v(BinaryOperation(Number(7),
                                     "+",
                                     Number(3)).evaluate(None)) == 10

    def test_difference(self):
        assert get_v(BinaryOperation(Number(7),
                                     "-",
                                     Number(3)).evaluate(None)) == 4

    def test_multiplication(self):
        assert get_v(BinaryOperation(Number(7),
                                     "*",
                                     Number(3)).evaluate(None)) == 21

    def test_division(self):
        assert get_v(BinaryOperation(Number(7),
                                     "/",
                                     Number(3)).evaluate(None)) == 2

    def test_mod(self):
        assert get_v(BinaryOperation(Number(7),
                                     "%",
                                     Number(3)).evaluate(None)) == 1

    def test_equal(self):
        assert get_v(BinaryOperation(Number(7),
                                     "==",
                                     Number(3)).evaluate(None)) == 0

    def test_not_equal(self):
        assert get_v(BinaryOperation(Number(7),
                                     "!=",
                                     Number(3)).evaluate(None)) == 1

    def test_less(self):
        assert get_v(BinaryOperation(Number(7),
                                     "<",
                                     Number(3)).evaluate(None)) == 0

    def test_more(self):
        assert get_v(BinaryOperation(Number(7),
                                     ">",
                                     Number(3)).evaluate(None)) == 1

    def test_less_or_equal(self):
        assert get_v(BinaryOperation(Number(7),
                                     "<=",
                                     Number(3)).evaluate(None)) == 0

    def test_more_or_equal(self):
        assert get_v(BinaryOperation(Number(7),
                                     ">=",
                                     Number(7)).evaluate(None)) == 1

    def test_and(self):
        assert get_v(BinaryOperation(Number(7),
                                     "&&",
                                     Number(0)).evaluate(None)) == 0

    def test_or(self):
        assert get_v(BinaryOperation(Number(1),
                                     "||",
                                     Number(7)).evaluate(None)) == 1


class TestUnaryOperation:

    def test_minus(self):
        assert get_v(UnaryOperation("-", Number(5)).evaluate(None)) == -5

    def test_not(self):
        assert get_v(UnaryOperation("!", Number(5)).evaluate(None)) == 0


class TestConditional:

    def test_cond_is_true(self):
        ans = Conditional(BinaryOperation(Number(3), ">", Number(0)),
                          [Number(1)],
                          [])
        assert get_v(ans.evaluate(None)) == 1

    def test_cond_is_false(self):
        ans = Conditional(BinaryOperation(Number(3), "*", Number(0)),
                          [],
                          [Number(2)])
        assert get_v(ans.evaluate(None)) == 2

    def test_list_of_operations(self):
        ans = Conditional(BinaryOperation(Number(3), "*", Number(0)),
                          [],
                          [BinaryOperation(UnaryOperation("-", Number(2)), "+",
                           BinaryOperation(Number(3), "*", Number(-7)))])
        assert get_v(ans.evaluate(None)) == -23

    def test_none_true(self):
        ans = Conditional(Number(1), None, None)
        ans.evaluate(None)

    def test_none_false(self):
        ans = Conditional(Number(0), None, None)
        ans.evaluate(None)

    def test_empty_true(self):
        ans = Conditional(Number(1), [], [])
        ans.evaluate(None)

    def test_empty_false(self):
        ans = Conditional(Number(0), [], [])
        ans.evaluate(None)


class TestReference:

    def test_reference(self):
        scope = Scope()
        scope["a"] = Number(10)
        scope["b"] = Number(20)
        assert get_v(BinaryOperation(Reference("a"),
                                     "+",
                                     Reference("b")).evaluate(scope)) == 30


class TestScope:

    def test_scope(self):
        parent = Scope()
        child = Scope(parent)
        parent["a"] = Number(30)
        parent["b"] = Number(50)
        child["b"] = Number(5)
        assert get_v(BinaryOperation(Reference("a"),
                                     "+",
                                     Reference("b")).evaluate(child)) == 35


class TestFuction:

    def test_function_usual(self):
        scope = Scope()
        scope["n"] = Number(6)
        cond = Conditional(BinaryOperation(Reference("a"), ">", Number(1)), [
                           FunctionCall(Reference("f"), [
                               BinaryOperation(Reference("a"),
                                               "-",
                                               Number(1))])], [
                           Number(1)])
        func = Function("a", [BinaryOperation(cond, "*", Reference("a"))])
        d = FunctionDefinition("f", func)
        assert get_v(FunctionCall(d, [Reference("n")]).evaluate(scope)) == 720

    def test_function_empty(self):
        scope = Scope()
        defin = FunctionDefinition('name', Function(['n'], []))
        FunctionCall(defin, [Number(5)]).evaluate(scope)
