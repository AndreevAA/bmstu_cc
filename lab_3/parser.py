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
