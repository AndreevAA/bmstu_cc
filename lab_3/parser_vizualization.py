class Node:
    def __init__(self, name):
        self.name = name
        self.children = []

class Parser:

    def __init__(self, input):
        self.input = input
        self.i = 0
        self.program()
        self.node = Node

    def program(self):
        if self.block():
            print('program')
            return True
        else:
            return False


    def error(self):
        print('Syntax error on ', self.i)
        exit()

    def get_current_token(self):
        if self.i < len(self.input):
            return self.input[self.i]
        return None

    def operators_list(self, node):
        if self.operator(node):
            print('operator')
            if self.tail():
                print('tail')
                return True
            self.error()
        self.error()


    def block(self, node):
        if self.get_current_token() == '{':
            self.i = self.i + 1
            if self.get_current_token() == '}':
                print('block')
                return True
            elif self.operators_list(node):
                print('operator_list')
                if self.get_current_token() == '}':
                    self.i = self.i + 1
                    print('block')
                    return True
                else:
                    self.error()
            self.error()

    def operator(self, node):
        current_token = self.get_current_token()
        if current_token.isalpha():
            self.i += 1
            node.children.append(Node('identifier'))
            if self.get_current_token() == ':=':
                self.i += 1
                if self.expression(node):
                    node.children.append(Node('expression'))
                    return True
                self.error()
            self.error()
        elif self.block():
            return True
        else:
            return self.error()

    def primary(self, node):
        current_token = self.get_current_token()
        if current_token == 'p' or current_token.isdigit():
            self.i += 1
            node.children.append(Node('primary'))
            return True
        if current_token == '(':
            self.i += 1
            if self.expression(node):
                node.children.append(Node('expression'))
                if self.get_current_token() == ')':
                    self.i += 1
                    return True
        self.error()

    def factor(self, node):
        current_token = self.get_current_token()
        if current_token in ('abs', 'not'):
            self.i += 1
            node.children.append(Node('abs or not'))
            if self.primary(node):
                return True
            self.error()
        if self.primary(node):
            while True:
                if self.get_current_token() == '**':
                    self.i += 1
                    if self.primary(node):
                        return True
                    self.error()
                else:
                    break
        return True

    def term(self, node):
        if self.factor(node):
            node.children.append(Node('factor'))
            while True:
                current_token = self.get_current_token()
                if current_token in ('*', '/', 'mod', 'rem'):
                    self.i += 1
                    node.children.append(Node(current_token))
                    if self.factor(node):
                        return True
                    self.error()
                else:
                    break
            return True

    def simple_expression(self, node):
        if self.get_current_token() in ('-', '+'):
            self.i += 1
            node.children.append(Node('un add operation'))
        if self.term(node):
            node.children.append(Node('term'))
        while True:
            current_token = self.get_current_token()
            if current_token in ('+', '-', '&'):
                self.i += 1
                node.children.append(Node(current_token))
                if self.term(node):
                    return True
                self.error()
            else:
                break
        return True

    def expression(self):
        node = Node('expression')
        if self.relation():
            print('relation')
            node.children.append(Node('relation'))
            if self.get_current_token() in ('and', 'or', 'xor'):
                self.i += 1
                print('logic operation')
                node.children.append(Node('logic operation'))
                if self.relation():
                    print('relation')
                    node.children.append(Node('relation'))
                    return node
                self.error()
            return True
        else:
            self.error()

    def relation(self):
        node = Node('relation')
        if self.simple_expression():
            print('simple expression')
            node.children.append(Node('simple expression'))
            if self.get_current_token() in ('<', '<=', '==', '/>', '>=', '>'):
                self.i += 1
                print('relation operation')
                node.children.append(Node('relation operation'))
                if self.simple_expression():
                    print('simple expression')
                    node.children.append(Node('simple expression'))
                    return node
                self.error()
            return True
        else:
            self.error()

    def tail(self):
        node = Node('tail')
        if self.get_current_token() == ';':
            self.i += 1
            if self.operator():
                print('operator')
                node.children.append(Node('operator'))
                if self.tail():
                    print('tail')
                    node.children.append(Node('tail'))
                    return node
                self.error()
            self.error()
        return node
