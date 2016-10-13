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
            expr = self.if_true
        else:
            expr = self.if_false
        if expr:
            for term in expr:
                res = term.evaluate(scope)
            return res
        else:
            return Number(0)


class Print:

    """Print - печатает значение выражения на отдельной строке."""

    def __init__(self, expr):
        self.expr = expr

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


class UnaryOperation:

    """UnaryOperation - представляет унарную операцию над выражением.
    Результатом вычисления унарной операции является объект Number.
    Поддерживаемые операции: “-”, “!”."""
    operation = {'-': lambda x: -x.value,
                 '!': lambda x: int(not x.value)}

    def __init__(self, op, expr):
        self.op = op
        self.expr = expr

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


def my_test1():  # Положительное число возводится в квадрат,
                # отрицательное в куб.
    print("Введите число. Положительное будет возведено в квадрат,"
          "отрицательное в куб: ")
    scope = Scope()
    Read("n").evaluate(scope)
    scope["sq"] = BinaryOperation(
        Reference("n"), '*', Reference("n")).evaluate(scope)
    ans = Conditional(BinaryOperation(Reference("n"), '>', Number(0)),
                      [Reference("sq")],
                      [BinaryOperation(Reference("sq"), '*', Reference("n"))])
    p = Print(ans)
    p.evaluate(scope)


def my_test2():  # Вычисление факториала.
    scope = Scope()
    scope["n"] = Number(6)
    cond = Conditional(BinaryOperation(Reference("a"), ">", Number(1)), [FunctionCall(
        Reference("f"), [BinaryOperation(Reference("a"), "-", Number(1))])], [Number(1)])
    func = Function("a", [BinaryOperation(cond, "*", Reference("a"))])
    defin = FunctionDefinition("f", func)
    assert FunctionCall(defin, [Reference("n")]).evaluate(scope).value == 720


def my_test3():  # Поделим нацело нечетное число на 2. Если число четно
            # то т.к., значение if_false не указано, то результат это 0.
    print("Введите нечетное число, оно будет поделено нацело на 2: ")
    scope = Scope()
    Read("n").evaluate(scope)
    cond = Conditional(
        BinaryOperation(
            BinaryOperation(
                Reference("n"), "%", Number(2)), "==", Number(1)), [
            BinaryOperation(
                Reference("n"), "/", Number(2))], [])
    Print(cond).evaluate(scope)


def my_test4():  # Тест scope`а. Результатом должно быть число 35,
                # потому что значение а берется из parent, а b из child.
    print("Результатом должно быть 35 ")
    parent = Scope()
    child = Scope(parent)
    parent["a"] = Number(30)
    parent["b"] = Number(50)
    child["b"] = Number(5)
    Print(BinaryOperation(Reference("a"), "+", Reference("b"))).evaluate(child)


def my_test5():  # Деление двух чисед, если делитель не 0.
    print("Введите делимое и делитель ")
    scope = Scope()
    Read("a").evaluate(scope)
    Read("b").evaluate(scope)
    cond = Conditional(BinaryOperation(Reference("b"), "==", Number(0)),
                       [],
                       [BinaryOperation(Reference("a"), "/", Reference("b"))])
    Print(cond).evaluate(scope)

if __name__ == '__main__':
    example()
    my_test1()
    my_test2()
    my_test3()
    my_test4()
    my_test5()
