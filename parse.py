class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.idx = 0
        self.token = self.tokens[self.idx]

    def factor(self):
        if self.token.type in ["INTEGER", "FLOAT"]:
            return self.token
        elif self.token.value == "(":
            self.move()
            expression = self.boolean_expression()
            return expression
        elif self.token.value == "not":
            operator = self.token
            self.move()
            right_node = self.boolean_expression()
            return [operator, right_node]
        elif self.token.type.startswith("VARIABLE"):
            return self.token
        elif self.token.value in ["+", "-"]:
            operator = self.token
            self.move()
            right_node = self.boolean_expression()
            return [operator, right_node]

    def term(self):
        left_node = self.factor()
        self.move()

        while self.token.value in ["*", "/"]:
            operator = self.token
            self.move()
            right_node = self.factor()
            self.move()
            left_node = [left_node, operator, right_node]
        return left_node
    
    def comparison_expression(self):
        left_node = self.expression()
        while self.token.type == "COMPARISON":
            operator = self.token
            self.move()
            right_node = self.expression()
            left_node = [left_node, operator, right_node]
        return left_node
    
    def boolean_expression(self):
        left_node = self.comparison_expression()
        while self.token.type == "BOOLEAN":
            operator = self.token
            self.move()
            right_node = self.comparison_expression()
            left_node = [left_node, operator, right_node]
        return left_node

    def expression(self):
        left_node = self.term()
        while self.token.value in ["+", "-"]:
            operator = self.token
            self.move()
            right_node = self.term()
            left_node = [left_node, operator, right_node]
        return left_node

    def variable(self):
        if self.token.type.startswith("VARIABLE"):
            return self.token
    
    def if_statement(self):
        self.move()
        condition = self.boolean_expression()

        if self.token.value == "do":
            self.move()
            action = self.statement()
            return condition, action
        elif self.tokens[self.idx - 1].value == "do":
            action = self.statement()
            return condition, action

    def if_statements(self):
        conditions = []
        actions = []
        if_statement = self.if_statement()

        conditions.append(if_statement[0])
        actions.append(if_statement[1])

        while self.token.value == "elif":
            if_statement = self.if_statement()
            conditions.append(if_statement[0])
            actions.append(if_statement[1])

        if self.token.value == "else":
            self.move()
            self.move()
            else_action = self.statement()

            return [conditions, actions, else_action]

        return [conditions, actions]

    def while_statement(self):
        self.move()
        condition = self.boolean_expression()

        if self.token.value == "do":
            self.move()
            action = self.statement()
            return [condition, action]
        elif self.tokens[self.idx - 1].value == "do":
            action = self.statement()
            return [condition, action]

    def statement(self):
        # variable assignment
        if self.token.type == "DECLARATION":
            self.move()
            left_node = self.variable()
            self.move()
            if self.token.value == "=":
                operation = self.token
                self.move()
                right_node = self.boolean_expression()
                return [left_node, operation, right_node]

        # arithmetic expression
        elif self.token.type in ["INTEGER", "FLOAT", "OPERATION", "not"]:
            return self.boolean_expression()
        
        # if statement
        elif self.token.value == "if":
            return [self.token, self.if_statements()]
    
        # while statement
        elif self.token.value == "while":
            return [self.token, self.while_statement()]
        
        # show statement
        elif self.token.value == "show":
            self.move()
            res = [self.token, self.boolean_expression()]
            return res

    def parse(self):
        return self.statement()

    def move(self):
        self.idx += 1
        if self.idx < len(self.tokens):
            self.token = self.tokens[self.idx]