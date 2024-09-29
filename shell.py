from lexer import Lexer
from parse import Parser
from interpreter import Interpreter
from data import Data

base = Data()

while True:
    # Step #1: Take Input
    text = input("DuaScript > ")

    # Step #2: Tokenize in Lexer
    tokenizer = Lexer(text)
    tokens = tokenizer.tokenize()

    # Step #3: Parse in AST
    parser = Parser(tokens)
    tree = parser.parse()
    
    # Step #4: Interpret in Interpreter
    interpreter = Interpreter(tree, base)
    result = interpreter.interpret()

    if result is not None:
        print(result)