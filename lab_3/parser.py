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
