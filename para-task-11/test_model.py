from model import *
import pytest
import sys
import io

def get_v(n):
    sys.stdout = io.StringIO()
    Print(n).evaluate(None)
    return int(sys.stdout.getvalue(None))

class TestBinaryOperation:

    def test_sum(self):
        assert(get_v(BinaryOperation(Number(7), "+", Number(3))) == 10)
        
    def test_difference(self): 
        assert(BinaryOperation(Number(7), "-", Number(3)).evaluate(None).value == 4)
        
    def test_multiplication(self):
        assert(BinaryOperation(Number(7), "*", Number(3)).evaluate(None).value == 21)
        
    def test_division(self):
        assert(BinaryOperation(Number(7), "/", Number(3)).evaluate(None).value == 2)
        
    def test_mod(self):
        assert(BinaryOperation(Number(7), "%", Number(3)).evaluate(None).value == 1)
        
    def test_equal(self):
        assert(BinaryOperation(Number(7), "==", Number(3)).evaluate(None).value == 0)
        
    def test_not_equal(self):
        assert(BinaryOperation(Number(7), "!=", Number(3)).evaluate(None).value == 1)
        
    def test_less(self):
        assert(BinaryOperation(Number(7), "<", Number(3)).evaluate(None).value == 0)
        
    def test_more(self):
        assert(BinaryOperation(Number(7), ">", Number(3)).evaluate(None).value == 1)
        
    def test_less_or_equal(self):
        assert(BinaryOperation(Number(7), "<=", Number(3)).evaluate(None).value == 0)
        
    def test_more_or_equal(self):
        assert(BinaryOperation(Number(7), ">=", Number(7)).evaluate(None).value == 1)
        
    def test_and(self):
        assert(BinaryOperation(Number(7), "&&", Number(0)).evaluate(None).value == 0)
        
    def test_or(self):
        assert(BinaryOperation(Number(1), "||", Number(7)).evaluate(None).value == 1)
        
        
class TestUnaryOperation:

    def test_minus(self):
        assert(UnaryOperation("-", Number(5)).evaluate(None).value == -5)
        
    def test_not(self):
        assert(UnaryOperation("!", Number(5)).evaluate(None).value == 0)
        
        
class TestConditional:

    def test_cond1(self):
        ans = Conditional(BinaryOperation(Number(3), ">", Number(0)),
                  [Number(1)],
                  [])
        assert(ans.evaluate(None).value == 1)
        
    def test_cond2(self):
        ans = Conditional(BinaryOperation(Number(3), "*", Number(0)),
                  [],
                  [Number(2)])
        assert(ans.evaluate(None).value == 2)
        
    def test_cond3(self):
        ans = Conditional(BinaryOperation(Number(3), "*", Number(0)),
                  [],
                  [BinaryOperation(UnaryOperation("-", Number(2)), "+", BinaryOperation(Number(3), "*", Number(-7)))])
        assert(ans.evaluate(None).value == -23)
        
    def test_cond4(self):
        ans = Conditional(Number(0), None, None)
        assert(ans.evaluate(None).value == 0)


class TestReference:

    def test_reference(self):
        scope = Scope()
        scope["a"] = Number(10)
        scope["b"] = Number(20)
        assert(BinaryOperation(Reference("a"), "+", Reference("b")).evaluate(scope).value == 30)
        
        
class TestScope:

    def test_scope(self):
        parent = Scope()
        child = Scope(parent)
        parent["a"] = Number(30)
        parent["b"] = Number(50)
        child["b"] = Number(5)
        assert(BinaryOperation(Reference("a"), "+", Reference("b")).evaluate(child).value == 35)
        
        
class TestFuction:

    def test_function(self):
        scope = Scope()
        scope["n"] = Number(6)
        cond = Conditional(BinaryOperation(Reference("a"), ">", Number(1)), [
                           FunctionCall(Reference("f"), [
                              BinaryOperation(Reference("a"), "-", Number(1))])], [
                           Number(1)])
        func = Function("a", [BinaryOperation(cond, "*", Reference("a"))])
        defin = FunctionDefinition("f", func)
        assert FunctionCall(defin, [Reference("n")]).evaluate(scope).value == 720
        
        


