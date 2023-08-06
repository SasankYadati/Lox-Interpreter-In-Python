from abc import ABC
from Static import Static
from Token import Token

class Expr(ABC):
    pass

class Binary(Expr):
    def __init__(self, left:Expr, operator:Token, right:Expr):
        self.left = left
        self.operator = operator
        self.right = right

class Unary(Expr):
    def __init__(self, operator:Token, right:Expr):
        self.operator = operator
        self.right = right