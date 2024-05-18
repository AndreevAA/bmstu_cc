from graphviz import Digraph

class Node:
    def __init__(self, parent_id, id, value):
        self.parent_id = parent_id
        self.id = id
        self.value = value

    def draw(self, graph):
        graph.node(str(self.id), str(self.value))
        
        if self.parent_id is not None:
            graph.edge(str(self.parent_id), str(self.id))


class Parser:

    def __init__(self, input):
        self.output_queue = []  # Для хранения выходной ОПН
        self.node_lst = list()

        self.node_cnt = 0
        self.input = input
        self.i = 0
        self.graph = Digraph()
        self.__program()
        

    
    def __get_new_node_id(self):
        self.node_cnt += 1
        return self.node_cnt
    
    def __create_new_node(self, parent_id, id, value):
        tmp_node = Node(parent_id = parent_id, id=id, value=value)
        self.node_lst.append(tmp_node)

        return tmp_node
        
    def __program(self):
        start_node = self.__create_new_node(parent_id = None, id=self.__get_new_node_id(), value='program')
        
        if self.__block(start_node):
            return True
        return False

    def __get_current_token(self):
        if self.i < len(self.input):
            return self.input[self.i]

    def __block(self, parent_node):
        block_node = self.__create_new_node(parent_id = parent_node.id, id=self.__get_new_node_id(), value='block')

        if self.__get_current_token() == '{':
            left_brack_node = self.__create_new_node(parent_id = block_node.id, id=self.__get_new_node_id(), value='{')
            self.i += 1

            if self.__get_current_token() == '}':
                right_brack_node = self.__create_new_node(parent_id = block_node.id, id=self.__get_new_node_id(), value='}')
                print("block", self.__get_current_token())
                return True

            elif self.__operators_list(block_node):
                if self.__get_current_token() == '}':
                    right_brack_node = self.__create_new_node(parent_id = block_node.id, id=self.__get_new_node_id(), value='}')
                    print("block", self.__get_current_token())
                    self.i += 1
                    return True
                else:
                    self.__error()
            self.__error()

    def __error(self, msg=""):
        print()
        print('ERROR: Syntax error on', self.i, "| elem =", self.input[self.i - 1], "|", msg)
        exit()

    
    def __operators_list(self, parent_node):
        operators_list_node = self.__create_new_node(parent_id=parent_node.id, id=self.__get_new_node_id(), value='operators_list')
        
        if self.__operator(operators_list_node):
            print("operator", self.__get_current_token())
            
            nextTok = self.__get_current_token()

            print ("DET ", nextTok)
            if nextTok != ';':
                self.__error('Error in ;')

            self.__create_new_node(parent_id=operators_list_node.id, id=self.__get_new_node_id(), value=';')
            
            self.i += 1
            self.__operators_list(operators_list_node)
        
        return True

    def __operator(self, parent_node):
        operator_node = self.__create_new_node(parent_id=parent_node.id, id=self.__get_new_node_id(), value='operator_node')

        if self.__get_current_token().isalpha():
            operator_node_value = self.__create_new_node(parent_id=operator_node.id, id=self.__get_new_node_id(), value=self.__get_current_token())
            print("operator", self.__get_current_token())
            self.i += 1

            if self.__get_current_token() == ':=':
                operator_node_value = self.__create_new_node(parent_id=operator_node.id, id=self.__get_new_node_id(), value=':=')
                print("operator", self.__get_current_token())
                self.i += 1

                if self.__expression(operator_node):
                    return True
                
                self.__error('Error in expression')
            
            self.__error('Expected ":=" after identifier')
        elif self.__block(operator_node):
            return True
        elif self.__get_current_token() != ";":
            print(self.__get_current_token())
            # self.__error('Invalid operator')

        


    def __factor(self, parent_node):
        factor_node = self.__create_new_node(parent_id = parent_node.id, id=self.__get_new_node_id(), value='factor_node')
        print("factor", self.__get_current_token())

        if self.__get_current_token() in ('abs', 'not'):
            factor_node_value = self.__create_new_node(parent_id = factor_node.id, id=self.__get_new_node_id(), value=self.__get_current_token())
            self.i += 1

            if self.__primary(factor_node):
                return True
            
            self.__error()
        if self.__primary(factor_node):
            while self.__get_current_token() == '**':
                factor_node_value = self.__create_new_node(parent_id = factor_node.id, id=self.__get_new_node_id(), value=self.__get_current_token())
                self.i += 1
                
                if self.__primary(factor_node):
                    continue
                else:
                    self.__error()
            return True
        else:
            factor_node_value = self.__create_new_node(parent_id = factor_node.id, id=self.__get_new_node_id(), value=self.__get_current_token())
            self.i += 1
            
            if self.__primary(factor_node):
                return True
            
            self.__error()

    def __primary(self, parent_node):
        primary_node = self.__create_new_node(parent_id = parent_node.id, id=self.__get_new_node_id(), value='primary_node')

        if self.__get_current_token() == 'p' or self.__get_current_token().isdigit():
            primary_node_value = self.__create_new_node(parent_id = primary_node.id, id=self.__get_new_node_id(), value=self.__get_current_token())
            self.i += 1
            
            print("primary", self.__get_current_token())
            return True
        if self.__get_current_token() == '(':
            primary_node_value = self.__create_new_node(parent_id = primary_node.id, id=self.__get_new_node_id(), value=self.__get_current_token())
            self.i += 1
            
            if self.__expression(primary_node):
                print("expression", self.__get_current_token())
                
                if self.__get_current_token() == ')':
                    primary_node_value = self.__create_new_node(parent_id = primary_node.id, id=self.__get_new_node_id(), value=self.__get_current_token())
                    self.i += 1
                    
                    return True
            self.__error()

    # Модифицируем методы для работы с ОПН
    def __expression(self, parent_node):
        expression_node = self.__create_new_node(parent_id = parent_node.id, id=self.__get_new_node_id(), value='expression_node')
       
        if self.__relation(expression_node):
            print("relation", self.__get_current_token())
            
            if self.__get_current_token() in ('and', 'or', 'xor'):
                expression_node_value = self.__create_new_node(parent_id = expression_node.id, id=self.__get_new_node_id(), value=self.__get_current_token())
                # После успешного разбора выражения добавляем операторы в ОПН
                self.output_queue.append(self.__get_current_token())
                self.i += 1
                print("logic operation", self.__get_current_token())

                if self.__relation(expression_node):
                    print("relation", self.__get_current_token())
                    return True
                
                self.__error()
            return True
        else:
            self.__error()

    def __relation(self, parent_node):
        relation_node = self.__create_new_node(parent_id = parent_node.id, id=self.__get_new_node_id(), value='relation_node')
        
        if self.__simple_expression(relation_node):
            if self.__get_current_token() in ('<', '<=', '==', '/>', '>=', '>'):
                relation_node_value = self.__create_new_node(parent_id = relation_node.id, id=self.__get_new_node_id(), value=self.__get_current_token())
                self.i += 1

                if self.__simple_expression(relation_node):
                    return True
                
                self.__error()
            return True
        else:
            self.__error()

    def __term(self, parent_node):
        term_node = self.__create_new_node(parent_id = parent_node.id, id=self.__get_new_node_id(), value='term_node')

        if self.__factor(term_node):
            while self.__get_current_token() in ('*', '/', 'mod', 'rem'):
                term_node_value = self.__create_new_node(parent_id = term_node.id, id=self.__get_new_node_id(), value=self.__get_current_token())
                # После успешного разбора терма добавляем операторы в ОПН
                self.output_queue.append(self.__get_current_token())
                self.i += 1

                if self.__factor(term_node):
                    continue
                else:
                    self.__error()
            return True

    def __simple_expression(self, parent_node):
        simple_expression_node = self.__create_new_node(parent_id = parent_node.id, id=self.__get_new_node_id(), value='simple_expression_node')

        if self.__get_current_token() in ('-', '+'):
            simple_expression_node_value = self.__create_new_node(parent_id = simple_expression_node.id, id=self.__get_new_node_id(), value=self.__get_current_token())
            self.i += 1

        if self.__term(simple_expression_node):
            while self.__get_current_token() in ('+', '-', '&'):
                simple_expression_node_value = self.__create_new_node(parent_id = simple_expression_node.id, id=self.__get_new_node_id(), value=self.__get_current_token())
                # После успешного разбора простого выражения добавляем операторы в ОПН
                self.output_queue.append(self.__get_current_token())
                self.i += 1
                
                if self.__term(simple_expression_node):
                    continue
                else:
                    self.__error()
            return True
        else:
            self.__error()

    def render_tree(self):
        print(self.node_lst)

        for _ in self.node_lst:
            _.draw(self.graph)

        self.graph.render('parse_tree', format='png', view=True)

    # Добавляем метод для вывода ОПН
    def get_rpn_output(self):
        return ' '.join(self.output_queue)

tests = [
    # '{ a := 3 ; aaa := p ; { a := p ; x := p and not p ; } ; } ' # верно по 
    """
    {
        a := 3 ;
        aaa := p ;
        { 
            a := p ;
            x := p and not p ;
        } ;
    } 
    """ # верно
    #'{ a := ( abs p and ( 1 ** 25 ) ) }', 
    #'{ a := 1 and - ( + p and 1 ** 2 ** 455 ) }', 
    #'{ c := not ( p mod 5 / ( 2 + 2 ) ) }', 
    #'{ c := abs ( - p + 2 & 4 mod 5 / ( 2 ) ) }', 
    #'{ ll := ( p and - 22 ) }'
]


def main(input_string):
    input_string_split = list(input_string.strip().split())
    print()
    print('Tokens')
    print(input_string_split)
    parser = Parser(input_string_split)
    parser.render_tree()
    print("Обратная польская нотация:", parser.get_rpn_output())

for _ in tests:
    main(_)
# main(tests)