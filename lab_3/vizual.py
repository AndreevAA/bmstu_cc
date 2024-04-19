from graphviz import Digraph as C
from graphviz import Digraph as C

class Node:
    def __init__(self, parent_id, id, value):
        self.parent_id = parent_id
        self.id = id
        self.value = value

    def draw(self, graph):
        graph.node(str(self.id), str(self.value))
        
        if self.parent_id is not None:
            graph.edge(str(self.parent_id), str(self.id))

class M:
    def __init__(self, input):
        self.node_lst = list()

        self.node_cnt = 0
        self.input = input
        self.i = 0
        self.graph = C()
        self.program()

    def __get_new_node_id(self):
        self.node_cnt += 1
        return self.node_cnt
        
    def __get_start_node(self):
        return Node(parent_id = None, id=self.__get_new_node_id(), value='program')

    def program(self):
        start_node = self.__get_start_node()
        self.node_lst.append(start_node)
        
        if self.block(start_node):
            return True
        return False

    def error(self):
        self.render_tree()
        print('Syntax error on ', self.i)
        exit()

    def get_current_token(self):
        if self.i < len(self.input):
            return self.input[self.i]

    def block(self, parent_node):
        block_node = Node(parent_id = parent_node.id, id=self.__get_new_node_id(), value='block')
        self.node_lst.append(block_node)

        if self.get_current_token() == '{':
            left_brack_node = Node(parent_id = block_node.id, id=self.__get_new_node_id(), value='{')
            self.node_lst.append(left_brack_node)
            self.i += 1

            if self.get_current_token() == '}':
                right_brack_node = Node(parent_id = block_node.id, id=self.__get_new_node_id(), value='}')
                self.node_lst.append(right_brack_node)
                print("block", self.get_current_token())
                return True

            elif self.operators_list(block_node):
                if self.get_current_token() == '}':
                    right_brack_node = Node(parent_id = block_node.id, id=self.__get_new_node_id(), value='}')
                    self.node_lst.append(right_brack_node)
                    print("block", self.get_current_token())
                    return True
                else:
                    self.error()
            self.error()

    def operators_list(self, parent_node):
        operators_list_node = Node(parent_id = parent_node.id, id=self.__get_new_node_id(), value='operators_list')
        self.node_lst.append(operators_list_node)
        
        if self.operator(operators_list_node):
            print("operator", self.get_current_token())

            if self.tail(operators_list_node):
                print("tail", self.get_current_token())
                return True

            self.error()
        self.error()

    def operator(self, parent_node):
        operator_node = Node(parent_id = parent_node.id, id=self.__get_new_node_id(), value='operator_node')
        self.node_lst.append(operator_node)

        if self.get_current_token().isalpha():
            operator_node_value = Node(parent_id = operator_node.id, id=self.__get_new_node_id(), value=self.get_current_token())
            self.node_lst.append(operator_node_value)
            print("operator", self.get_current_token())
            self.i += 1
            if self.get_current_token() == ':=':
                operator_node_value = Node(parent_id = operator_node.id, id=self.__get_new_node_id(), value=':=')
                self.node_lst.append(operator_node_value)
                print("operator", self.get_current_token())
                self.i += 1
                if self.expression(operator_node):
                    return True
                self.error()
            self.error()
        elif self.block(operator_node):
            return True
        else:
            return self.error()

    def factor(self, parent_node):
        factor_node = Node(parent_id = parent_node.id, id=self.__get_new_node_id(), value='factor_node')
        self.node_lst.append(factor_node)

        print("factor", self.get_current_token())

        if self.get_current_token() in ('abs', 'not'):
            factor_node_value = Node(parent_id = factor_node.id, id=self.__get_new_node_id(), value=self.get_current_token())
            self.node_lst.append(factor_node_value)
            self.i += 1
            if self.primary(factor_node):
                return True
            self.error()
        if self.primary(factor_node):
            while self.get_current_token() == '**':
                factor_node_value = Node(parent_id = factor_node.id, id=self.__get_new_node_id(), value=self.get_current_token())
                self.node_lst.append(factor_node_value)
                self.i += 1
                if self.primary(factor_node):
                    continue
                else:
                    self.error()
            return True
        else:
            factor_node_value = Node(parent_id = factor_node.id, id=self.__get_new_node_id(), value=self.get_current_token())
            self.node_lst.append(factor_node_value)
            self.i += 1
            if self.primary(factor_node):
                return True
            self.error()

    def primary(self, parent_node):
        primary_node = Node(parent_id = parent_node.id, id=self.__get_new_node_id(), value='primary_node')
        self.node_lst.append(primary_node)

        if self.get_current_token() == 'p' or self.get_current_token().isdigit():
            primary_node_value = Node(parent_id = primary_node.id, id=self.__get_new_node_id(), value=self.get_current_token())
            self.node_lst.append(primary_node_value)
            self.i += 1
            
            print("primary", self.get_current_token())
            return True
        if self.get_current_token() == '(':
            primary_node_value = Node(parent_id = primary_node.id, id=self.__get_new_node_id(), value=self.get_current_token())
            self.node_lst.append(primary_node_value)
            self.i += 1
            if self.expression(primary_node):
                print("expression", self.get_current_token())
                if self.get_current_token() == ')':
                    primary_node_value = Node(parent_id = primary_node.id, id=self.__get_new_node_id(), value=self.get_current_token())
                    self.node_lst.append(primary_node_value)
                    self.i += 1
                    return True
            self.error()

    def expression(self, parent_node):
        expression_node = Node(parent_id = parent_node.id, id=self.__get_new_node_id(), value='expression_node')
        self.node_lst.append(expression_node)

        if self.relation(expression_node):
            print("relation", self.get_current_token())
            if self.get_current_token() in ('and', 'or', 'xor'):
                expression_node_value = Node(parent_id = expression_node.id, id=self.__get_new_node_id(), value=self.get_current_token())
                self.node_lst.append(expression_node_value)
                self.i += 1
                print("logic operation", self.get_current_token())

                if self.relation(expression_node):
                    print("relation", self.get_current_token())
                    return True
                self.error()
            return True
        else:
            self.error()

    def relation(self, parent_node):
        relation_node = Node(parent_id = parent_node.id, id=self.__get_new_node_id(), value='relation_node')
        self.node_lst.append(relation_node)
        
        if self.simple_expression(relation_node):
            if self.get_current_token() in ('<', '<=', '==', '/>', '>=', '>'):
                relation_node_value = Node(parent_id = relation_node.id, id=self.__get_new_node_id(), value=self.get_current_token())
                self.node_lst.append(relation_node_value)
                self.i += 1

                if self.simple_expression(relation_node):
                    return True
                self.error()
            return True
        else:
            self.error()

    def term(self, parent_node):
        term_node = Node(parent_id = parent_node.id, id=self.__get_new_node_id(), value='term_node')
        self.node_lst.append(term_node)

        if self.factor(term_node):
            while self.get_current_token() in ('*', '/', 'mod', 'rem'):
                term_node_value = Node(parent_id = term_node.id, id=self.__get_new_node_id(), value=self.get_current_token())
                self.node_lst.append(term_node_value)
                self.i += 1

                if self.factor(term_node):
                    continue
                else:
                    self.error()
            return True

    def simple_expression(self, parent_node):
        simple_expression_node = Node(parent_id = parent_node.id, id=self.__get_new_node_id(), value='simple_expression_node')
        self.node_lst.append(simple_expression_node)

        if self.get_current_token() in ('-', '+'):
            simple_expression_node_value = Node(parent_id = simple_expression_node.id, id=self.__get_new_node_id(), value=self.get_current_token())
            self.node_lst.append(simple_expression_node_value)
            self.i += 1
        if self.term(simple_expression_node):
            while self.get_current_token() in ('+', '-', '&'):
                simple_expression_node_value = Node(parent_id = simple_expression_node.id, id=self.__get_new_node_id(), value=self.get_current_token())
                self.node_lst.append(simple_expression_node_value)
                self.i += 1
                
                if self.term(simple_expression_node):
                    continue
                else:
                    self.error()
            return True
        else:
            self.error()

    def tail(self, parent_node):
        if self.get_current_token() == ';':
            tail_node = Node(parent_id = parent_node.id, id=self.__get_new_node_id(), value=';')
            self.node_lst.append(tail_node)
        
            self.i += 1
            if self.operator(parent_node):
                print("operator", self.get_current_token())
                if self.tail(parent_node):
                    print("tail", self.get_current_token())
                    return True
                self.error()
            self.error()
        return True

    def render_tree(self):
        print(self.node_lst)

        for _ in self.node_lst:
            _.draw(self.graph)

        self.graph.render('parse_tree', format='png', view=True)