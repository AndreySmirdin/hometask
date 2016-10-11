#!/usr/bin/env python3

# Шаблон для домашнѣго задания
# Рѣализуйте мѣтоды с raise NotImplementedError

class Scope:

    """Scope - представляет доступ к значениям по именам
    (к функциям и именованным константам).
    Scope может иметь родителя, и если поиск по имени
    в текущем Scope не успешен, то если у Scope есть родитель,
    то поиск делегируется родителю.
    Scope должен поддерживать dict-like интерфейс доступа
    (см. на специальные функции __getitem__ и __setitem__)
    """

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

    """Number - представляет число в программе.
    Все числа в нашем языке целые."""

    def __init__(self, value):
        self.value = value

    def evaluate(self, scope):
        return self


class Function:

    """Function - представляет функцию в программе.
    Функция - второй тип поддерживаемый языком.
    Функции можно передавать в другие функции,
    и возвращать из функций.
    Функция состоит из тела и списка имен аргументов.
    Тело функции это список выражений,
    т. е.  у каждого из них есть метод evaluate.
    Во время вычисления функции (метод evaluate),
    все объекты тела функции вычисляются последовательно,
    и результат вычисления последнего из них
    является результатом вычисления функции.
    Список имен аргументов - список имен
    формальных параметров функции."""

    def __init__(self, args, body):
        self.args = args
        self.body = body

    def evaluate(self, scope):
        res = Number(0)
        for expr in self.body:
            res = expr.evaluate(scope)
        return res


class FunctionDefinition:

    """FunctionDefinition - представляет определение функции,
    т. е. связывает некоторое имя с объектом Function.
    Результатом вычисления FunctionDefinition является
    обновление текущего Scope - в него
    добавляется новое значение типа Function."""

    def __init__(self, name, function):
        self.name = name
        self.function = function

    def evaluate(self, scope):
        scope[self.name] = self.function
        return self.function

class Conditional:

    """
    Conditional - представляет ветвление в программе, т. е. if.
    """

    def __init__(self, condtion, if_true, if_false=None):
        self.condition = condtion
        self.if_true = if_true
        self.if_false = if_false

    def evaluate(self, scope):
        cond = self.condition.evaluate(scope)
        res = Number(0)
        if cond.value:
            for tr in self.if_true:
                res = tr.evaluate(scope)
            return res
        elif self.if_false:
            for fal in self.if_false:
                res = fal.evaluate(scope)
            return res

class Print:

    """Print - печатает значение выражения на отдельной строке."""

    def __init__(self, expr):
        self.expr = expr;

    def evaluate(self, scope):
        res = self.expr.evaluate(scope)
        print(res.value)
        return res

class Read:

    """Read - читает число из стандартного потока ввода
     и обновляет текущий Scope.
     Каждое входное число располагается на отдельной строке
     (никаких пустых строк и лишних символов не будет).
     """

    def __init__(self, name):
        self.name = name

    def evaluate(self, scope):
        inp = int(input())
        scope[self.name] = Number(inp)
        return Number(inp)

class FunctionCall:

    """
    FunctionCall - представляет вызов функции в программе.
    В результате вызова функции должен создаваться новый объект Scope,
    являющий дочерним для текущего Scope
    (т. е. текущий Scope должен стать для него родителем).
    Новый Scope станет текущим Scope-ом при вычислении тела функции.
    """

    def __init__(self, fun_expr, args):
        self.fun_expr = fun_expr
        self.args = args
    def evaluate(self, scope):
        function = self.fun_expr.evaluate(scope)
        call_scope = Scope(scope)
        for name, arg in zip(function.args, self.args):
            call_scope[name] = arg.evaluate(scope)
        return function.evaluate(call_scope)

class Reference:

    """Reference - получение объекта
    (функции или переменной) по его имени."""

    def __init__(self, name):
        self.name = name

    def evaluate(self, scope):
        return scope[self.name]


class BinaryOperation:

    """BinaryOperation - представляет бинарную операцию над двумя выражениями.
    Результатом вычисления бинарной операции является объект Number.
    Поддерживаемые операции:
    “+”, “-”, “*”, “/”, “%”, “==”, “!=”,
    “<”, “>”, “<=”, “>=”, “&&”, “||”."""

    def __init__(self, lhs, op, rhs):
        self.op = op
        self.lhs = lhs
        self.rhs = rhs
        self.operation = {'+': lambda x, y: x.value + y.value,
                         '-': lambda x, y: x.value - y.value,
                         '*': lambda x, y: x.value * y.value,
                         '/': lambda x, y: x.value / y.value,
                         '%': lambda x, y: x.value % y.value,
                         '==': lambda x, y: int(x.value == y.value),
                         '!=': lambda x, y: int(x.value != y.value),
                         '<': lambda x, y: int(x.value < y.value),
                         '<=': lambda x, y: int(x.value <= y.value),
                         '>=': lambda x, y: int(x.value >= y.value),
                         '>': lambda x, y: int(x.value > y.value),
                         '&&': lambda x, y: int(x.value and y.value),
                         '||': lambda x, y: int(x.value or y.value)}

    def evaluate(self, scope):
        res = Number(self.operation[self.op](self.lhs.evaluate(scope), self.rhs.evaluate(scope)))
        return res


class UnaryOperation:

    """UnaryOperation - представляет унарную операцию над выражением.
    Результатом вычисления унарной операции является объект Number.
    Поддерживаемые операции: “-”, “!”."""

    def __init__(self, op, expr):
        self.op = op
        self.expr = expr
        self.operation = {'-': lambda x: (-1)*x.value,
                          '!': lambda x: int(not(bool(x.value)))}
        
    def evaluate(self, scope):
        return Number(self.operation[self.op](self.expr.evaluate(scope)))


def example():
    parent = Scope()
    parent["foo"] = Function(('hello', 'world'),
                             [Print(BinaryOperation(Reference('hello'),
                                                    '+',
                                                    Reference('world')))])
    parent["bar"] = Number(10)
    scope = Scope(parent)
    assert 10 == scope["bar"].value
    scope["bar"] = Number(20)
    assert scope["bar"].value == 20
    print('It should print 2: ', end=' ')
    FunctionCall(FunctionDefinition('foo', parent['foo']),
[Number(5), UnaryOperation('-', Number(3))]).evaluate(scope)

def my_test1(): #положительное число возведем в квадрат, отрицательное в куб
    scope = Scope()
    Read("n").evaluate(scope)
    ans = Conditional( BinaryOperation(Reference("n"), ">", Number(0)),
                      [BinaryOperation(Reference("n"), '*', Reference("n"))],
                      [BinaryOperation(BinaryOperation(Reference("n"), '*', Reference("n")), "*", Reference("n"))])
    p = Print(ans)
    p.evaluate(scope)

def my_test2(): #вычисление факториала
    scope = Scope()
    Read("n").evaluate(scope)
    scope["ans"] = Number(1)
    cond = Conditional(BinaryOperation(Reference("a"), ">", Number(1)),
            [FunctionCall(Reference("factorial"),[BinaryOperation(Reference("a"), "-", Number(1))])],
            [Number(1)])
    func = Function("a", [BinaryOperation(cond, "*", Reference("a"))])
    definition = FunctionDefinition("factorial", func)
    p = Print(FunctionCall(definition, [Reference("n")]))
    p.evaluate(scope)


if __name__ == '__main__':
    #example()
    #my_test(1)
    my_test2()
