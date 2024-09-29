class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __repr__(self):
        return str(self.value)
    
class Integer(Token):
    def __init__(self, value):
        super().__init__("INTEGER", value)

class Float(Token):
    def __init__(self, value):
        super().__init__("FLOAT", value)

class Operation(Token):
    def __init__(self, value):
        super().__init__("OPERATION", value)

class Declaration(Token):
    def __init__(self, value):
        super().__init__("DECLARATION", value)

class Variable(Token):
    def __init__(self, value):
        super().__init__("VARIABLE(?)", value)

class Boolean(Token):
    def __init__(self, value):
        super().__init__("BOOLEAN", value)

class Comparison(Token):
    def __init__(self, value):
        super().__init__("COMPARISON", value)

class Reserved(Token):
    def __init__(self, value):
        super().__init__("RESERVED", value)