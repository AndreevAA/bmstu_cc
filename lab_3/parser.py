class Parser:

    def __init__(self, input):
        self.input = input
        self.i = 0
        self.program()

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


    def block(self):
        if self.get_current_token() == '{':
            self.i = self.i + 1
            if self.get_current_token() == '}':
                print('block')
                return True
            elif self.operators_list():
                print('operator_list')
                if self.get_current_token() == '}':
                    self.i = self.i + 1
                    print('block')
                    return True
                else:
                    self.error()
            self.error()

    def operators_list(self):
        if self.operator():
            print('operator')
            if self.tail():
                print('tail')
                return True
            self.error()
        self.error()

    def operator(self):
        if self.get_current_token().isalpha():
            self.i = self.i + 1
            print('identifier')
            if self.get_current_token() == ':=':
                self.i = self.i + 1
                if self.expression():
                    print('expression')
                    return True
                self.error()
            self.error()
        elif self.block():
            return True
        else:
            return self.error()

    def primary(self):
        if self.get_current_token() == 'p' or self.get_current_token().isdigit():
            self.i = self.i + 1
            return True
        if self.get_current_token() == '(':
            self.i = self.i + 1
            if self.expression():
                print('expression')
                if self.get_current_token() == ')':
                    self.i = self.i + 1
                    return True
        self.error()
