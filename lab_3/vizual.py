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

    def __error(self):
        self.render_tree()
        print('Syntax error on ', self.i)
        exit()

    def __get_current_token(self):
        if self.i < len(self.input):
            return self.input[self.i]

    def __block(self, parent_node):
        block_node = self.__create_new_node(parent_id = parent_node.id, id=self.__get_new_node_id(), value='block')

        if self.__get_current_token() == '{':
            left_brack_node = self.__create_new_node(parent_id = block_node.id, id=self.__get_new_node_id(), value='{')
            #self.node_lst.append(left_brack_node)
            self.i += 1

            if self.__get_current_token() == '}':
                right_brack_node = self.__create_new_node(parent_id = block_node.id, id=self.__get_new_node_id(), value='}')
                #self.node_lst.append(right_brack_node)
                print("block", self.__get_current_token())
                return True

            elif self.__operators_list(block_node):
                if self.__get_current_token() == '}':
                    right_brack_node = self.__create_new_node(parent_id = block_node.id, id=self.__get_new_node_id(), value='}')
                    #self.node_lst.append(right_brack_node)
                    print("block", self.__get_current_token())
                    return True
                else:
                    self.__error()
            self.__error()

    def __operators_list(self, parent_node):
        __operators_list_node = self.__create_new_node(parent_id = parent_node.id, id=self.__get_new_node_id(), value='operators_list')
        #self.node_lst.append(__operators_list_node)
        
        if self.__operator(__operators_list_node):
            print("operator", self.__get_current_token())

            if self.__tail(__operators_list_node):
                print("tail", self.__get_current_token())
                return True

            self.__error()
        self.__error()

    def __operator(self, parent_node):
        operator_node = self.__create_new_node(parent_id = parent_node.id, id=self.__get_new_node_id(), value='operator_node')
        #self.node_lst.append(operator_node)

        if self.__get_current_token().isalpha():
            operator_node_value = self.__create_new_node(parent_id = operator_node.id, id=self.__get_new_node_id(), value=self.__get_current_token())
            #self.node_lst.append(operator_node_value)
            print("operator", self.__get_current_token())
            self.i += 1
            if self.__get_current_token() == ':=':
                operator_node_value = self.__create_new_node(parent_id = operator_node.id, id=self.__get_new_node_id(), value=':=')
                #self.node_lst.append(operator_node_value)
                print("operator", self.__get_current_token())
                self.i += 1
                if self.__expression(operator_node):
                    return True
                self.__error()
            self.__error()
        elif self.__block(operator_node):
            return True
        else:
            return self.__error()

    def __factor(self, parent_node):
        factor_node = self.__create_new_node(parent_id = parent_node.id, id=self.__get_new_node_id(), value='factor_node')
        #self.node_lst.append(factor_node)

        print("factor", self.__get_current_token())

        if self.__get_current_token() in ('abs', 'not'):
            factor_node_value = self.__create_new_node(parent_id = factor_node.id, id=self.__get_new_node_id(), value=self.__get_current_token())
            #self.node_lst.append(factor_node_value)
            self.i += 1
            if self.__primary(factor_node):
                return True
            self.__error()
        if self.__primary(factor_node):
            while self.__get_current_token() == '**':
                factor_node_value = self.__create_new_node(parent_id = factor_node.id, id=self.__get_new_node_id(), value=self.__get_current_token())
                #self.node_lst.append(factor_node_value)
                self.i += 1
                if self.__primary(factor_node):
                    continue
                else:
                    self.__error()
            return True
        else:
            factor_node_value = self.__create_new_node(parent_id = factor_node.id, id=self.__get_new_node_id(), value=self.__get_current_token())
            #self.node_lst.append(factor_node_value)
            self.i += 1
            if self.__primary(factor_node):
                return True
            self.__error()

    def __primary(self, parent_node):
        primary_node = self.__create_new_node(parent_id = parent_node.id, id=self.__get_new_node_id(), value='primary_node')
        #self.node_lst.append(primary_node)

        if self.__get_current_token() == 'p' or self.__get_current_token().isdigit():
            primary_node_value = self.__create_new_node(parent_id = primary_node.id, id=self.__get_new_node_id(), value=self.__get_current_token())
            #self.node_lst.append(primary_node_value)
            self.i += 1
            
            print("primary", self.__get_current_token())
            return True
        if self.__get_current_token() == '(':
            primary_node_value = self.__create_new_node(parent_id = primary_node.id, id=self.__get_new_node_id(), value=self.__get_current_token())
            #self.node_lst.append(primary_node_value)
            self.i += 1
            if self.__expression(primary_node):
                print("expression", self.__get_current_token())
                if self.__get_current_token() == ')':
                    primary_node_value = self.__create_new_node(parent_id = primary_node.id, id=self.__get_new_node_id(), value=self.__get_current_token())
                    #self.node_lst.append(primary_node_value)
                    self.i += 1
                    return True
            self.__error()

    def __expression(self, parent_node):
        expression_node = self.__create_new_node(parent_id = parent_node.id, id=self.__get_new_node_id(), value='expression_node')
        #self.node_lst.append(expression_node)

        if self.__relation(expression_node):
            print("relation", self.__get_current_token())
            if self.__get_current_token() in ('and', 'or', 'xor'):
                expression_node_value = self.__create_new_node(parent_id = expression_node.id, id=self.__get_new_node_id(), value=self.__get_current_token())
                #self.node_lst.append(expression_node_value)
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
        #self.node_lst.append(relation_node)
        
        if self.__simple_expression(relation_node):
            if self.__get_current_token() in ('<', '<=', '==', '/>', '>=', '>'):
                relation_node_value = self.__create_new_node(parent_id = relation_node.id, id=self.__get_new_node_id(), value=self.__get_current_token())
                #self.node_lst.append(relation_node_value)
                self.i += 1

                if self.__simple_expression(relation_node):
                    return True
                self.__error()
            return True
        else:
            self.__error()

    def __term(self, parent_node):
        term_node = self.__create_new_node(parent_id = parent_node.id, id=self.__get_new_node_id(), value='term_node')
        #self.node_lst.append(term_node)

        if self.__factor(term_node):
            while self.__get_current_token() in ('*', '/', 'mod', 'rem'):
                term_node_value = self.__create_new_node(parent_id = term_node.id, id=self.__get_new_node_id(), value=self.__get_current_token())
                #self.node_lst.append(term_node_value)
                self.i += 1

                if self.__factor(term_node):
                    continue
                else:
                    self.__error()
            return True

    def __simple_expression(self, parent_node):
        simple_expression_node = self.__create_new_node(parent_id = parent_node.id, id=self.__get_new_node_id(), value='simple_expression_node')
        #self.node_lst.append(simple_expression_node)

        if self.__get_current_token() in ('-', '+'):
            simple_expression_node_value = self.__create_new_node(parent_id = simple_expression_node.id, id=self.__get_new_node_id(), value=self.__get_current_token())
            #self.node_lst.append(simple_expression_node_value)
            self.i += 1
        if self.__term(simple_expression_node):
            while self.__get_current_token() in ('+', '-', '&'):
                simple_expression_node_value = self.__create_new_node(parent_id = simple_expression_node.id, id=self.__get_new_node_id(), value=self.__get_current_token())
                #self.node_lst.append(simple_expression_node_value)
                self.i += 1
                
                if self.__term(simple_expression_node):
                    continue
                else:
                    self.__error()
            return True
        else:
            self.__error()

    def __tail(self, parent_node):
        if self.__get_current_token() == ';':
            tail_node = self.__create_new_node(parent_id = parent_node.id, id=self.__get_new_node_id(), value=';')
            #self.node_lst.append(tail_node)
        
            self.i += 1
            if self.__operator(parent_node):
                print("operator", self.__get_current_token())
                if self.__tail(parent_node):
                    print("tail", self.__get_current_token())
                    return True
                self.__error()
            self.__error()
        return True

    def render_tree(self):
        print(self.node_lst)

        for _ in self.node_lst:
            _.draw(self.graph)

        self.graph.render('parse_tree', format='png', view=True)