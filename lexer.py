from tokens import (
    Integer,
    Float,
    Operation,
    Declaration,
    Variable,
    Boolean,
    Comparison,
    Reserved,
)

class Lexer:
    digits = "0123456789"
    operations = "+-*/()="
    letters = "abcdefghijklmnopqrstuvwxyz"
    stopwords = [" "]
    declarations = ["make"]
    boolean = ["and", "or", "not"]
    comparisors = ["?=", "!=", "<", ">", "<=", ">="]
    special_characters = "?>!=<"
    reserved = ["if", "elif", "else", "do", "while", "show"]

    def __init__(self, text):
        self.text = text
        self.idx = 0
        self.tokens = []
        self.char = self.text[self.idx]
        self.token = None

    def tokenize(self):
        while self.idx < len(self.text):
            # Extracting Numbers
            if self.char in Lexer.digits:
                self.token = self.extract_number()

            # Extracting Operations
            elif self.char in Lexer.operations:
                self.token = Operation(self.char)
                self.move()

            # Skipping Stopwords
            elif self.char in Lexer.stopwords:
                self.move()
                continue

            # Extracting Words
            elif self.char in Lexer.letters:
                word = self.extract_word()
                if word in Lexer.declarations:
                    self.token = Declaration(word)
                elif word in Lexer.boolean:
                    self.token = Boolean(word)
                elif word in Lexer.reserved:
                    self.token = Reserved(word)
                else:
                    self.token = Variable(word)

            # Extracting Comparisons
            elif self.char in Lexer.special_characters:
                comparison_op = ""
                while self.char in Lexer.special_characters and (self.idx < len(self.text)):
                    comparison_op += self.char
                    self.move()
                self.token = Comparison(comparison_op)
            
            self.tokens.append(self.token)
        return self.tokens

    def extract_number(self):
        number = ""
        isFloat = False
        while (self.char in Lexer.digits or self.char == ".") and (self.idx < len(self.text)):
            if self.char == ".":
                isFloat = True
            number += self.char
            self.move()
        return Integer(number) if not isFloat else Float(number)
    
    def extract_word(self):
        word = ""
        while (self.char in Lexer.letters or self.char in Lexer.digits) and (self.idx < len(self.text)):
            word += self.char
            self.move()
        return word

    def move(self):
        self.idx += 1
        if self.idx < len(self.text):
            self.char = self.text[self.idx]
