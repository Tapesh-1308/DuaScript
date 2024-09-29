from tokens import (
    Integer,
    Float,
    Reserved
)
class Interpreter:
    def __init__(self, tree, base):
        self.tree = tree
        self.data = base

    def read_INTEGER(self, value):
        return int(value)
    
    def read_FLOAT(self, value):
        return float(value)
    
    def read_VARIABLE(self, value):
        variable = self.data.read(value)
        variable_type = variable.type

        return getattr(self, f"read_{variable_type}")(variable.value)
    

    def compute_binary(self, left, operator, right):
        left_type = "VARIABLE" if str(left.type).startswith("VARIABLE") else left.type
        right_type = "VARIABLE" if str(right.type).startswith("VARIABLE") else right.type

        if operator.value == "=":
            left.type = f"VARIABLE({right_type})"
            self.data.write(left, right)
            return self.data.read_all() 

        left_value = getattr(self, f"read_{left_type}")(left.value)
        right_value = getattr(self, f"read_{right_type}")(right.value)

        if operator.value == "+":
            output = left_value + right_value
        elif operator.value == "-":
            output = left_value - right_value
        elif operator.value == "*":
            output = left_value * right_value
        elif operator.value == "/":
            output = left_value / right_value
        elif operator.value == ">":
            output = 1 if left_value > right_value else 0
        elif operator.value == "<":
            output = 1 if left_value < right_value else 0
        elif operator.value == ">=":
            output = 1 if left_value >= right_value else 0
        elif operator.value == "<=":
            output = 1 if left_value <= right_value else 0
        elif operator.value == "?=":
            output = 1 if left_value == right_value else 0
        elif operator.value == "!=":
            output = 1 if left_value != right_value else 0
        elif operator.value == "and":
            output = 1 if left_value and right_value else 0
        elif operator.value == "or":
            output = 1 if left_value or right_value else 0

        return Float(output) if (left_type == "FLOAT" or right_type == "FLOAT") else Integer(output)
    
    def compute_unary(self, operator, right):
        right_type = "VARIABLE" if str(right.type).startswith("VARIABLE") else right.type
        right_value = getattr(self, f"read_{right_type}")(right.value)

        if operator.value == "+":
            output = right_value
        elif operator.value == "-":
            output = -right_value
        elif operator.value == "not":
            output = 0 if right_value else 1
        else:
            output = right_value
        return Float(output) if right_type == "FLOAT" else Integer(output)

    def interpret(self, tree=None):
        if tree is None:
            tree = self.tree
        if isinstance(tree, list):
            if isinstance(tree[0], Reserved):
                if tree[0].value == "if":
                    for idx, condition in enumerate(tree[1][0]):
                        eval_condition = self.interpret(condition)
                        if eval_condition.value == 1:
                            return self.interpret(tree[1][1][idx])
                    if len(tree[1]) == 3:
                        return self.interpret(tree[1][2])
                    else:
                        return
                elif tree[0].value == "while":
                    while self.interpret(tree[1][0]).value == 1:
                        self.interpret(tree[1][1])
                    return

        # unary operation
        if isinstance(tree, list) and len(tree) == 2:
            expression = tree[1]
            if isinstance(expression, list):
                return self.interpret(expression)
            return self.compute_unary(tree[0], expression)
        
        # no operation
        elif not isinstance(tree, list):
            return tree

        else:
            # Post Order Traversal

            # left subtree
            left_node = tree[0]
            if isinstance(left_node, list):
                left_node = self.interpret(left_node)

            # right subtree
            right_node = tree[2]
            if isinstance(right_node, list):
                right_node = self.interpret(right_node)
            
            # root node
            operator = tree[1]
            return self.compute_binary(left_node, operator, right_node)