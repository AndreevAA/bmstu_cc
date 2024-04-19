from graphviz import Digraph as C
from graphviz import Digraph as C

class M:
    def __init__(self, input):
        self.tmp_node_cnt = 0
        self.input = input
        self.i = 0
        self.graph = C()
        self.program()
        

    def program(self):
        node = 'program'
        if self.block():
            self.graph.node(node)
            self.graph.edge(node, 'block')
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

    def generate_unique_node_name(self, base_name):
        self.tmp_node_cnt += 1
        return f'{base_name}_{self.tmp_node_cnt}'


    def block(self):
        if self.get_current_token() == '{':
            self.i += 1
            if self.get_current_token() == '}':
                self.graph.node('block_end')
                self.graph.edge('block', 'block_end')
                print('block')
                return True
            elif self.operators_list():
                self.graph.node('operator_list')
                self.graph.edge('block', 'operator_list')
                if self.get_current_token() == '}':
                    self.i += 1
                    self.graph.node('block_end')
                    self.graph.edge('block', 'block_end')
                    print('block')
                    return True
                else:
                    self.error()
            self.error()

    def operators_list(self):
        if self.operator():
            self.tmp_node_cnt += 1
            node_name = f'operator_{self.tmp_node_cnt}'
            self.graph.node(node_name)
            self.graph.edge('operator_list', node_name)
            print('operator')
            if self.tail():
                self.tmp_node_cnt += 1
                tail_name = f'tail_{self.tmp_node_cnt}'
                self.graph.node(tail_name)
                self.graph.edge('operator_list', tail_name)
                print('tail')
                return True
            self.error()
        self.error()

    def operator(self):
        if self.get_current_token().isalpha():
            self.i += 1
            if self.get_current_token() == ':=':
                self.i += 1
                if self.expression():
                    self.tmp_node_cnt += 1
                    node_name = f'expression_{self.tmp_node_cnt}'
                    self.graph.node(node_name)
                    self.graph.edge('operator', node_name)
                    return True
                self.error()
            self.error()
        elif self.block():
            return True
        else:
            return self.error()

    def factor(self, parent_node):
        if self.get_current_token() in ('abs', 'not'):
            self.i += 1
            if self.primary(parent_node):
                return True
            self.error()
        if self.primary(parent_node):
            while self.get_current_token() == '**':
                self.i += 1
                if self.primary(parent_node):
                    continue
                else:
                    self.error()
            return True

    def primary(self, parent_node):
        if self.get_current_token() == 'p' or self.get_current_token().isdigit():
            self.i += 1
            self.tmp_node_cnt += 1
            node_name = f'primary_{self.tmp_node_cnt}'
            self.graph.node(node_name)
            self.graph.edge(parent_node, node_name)
            print('primary')
            return True
        if self.get_current_token() == '(':
            self.i += 1
            if self.expression(parent_node):
                self.tmp_node_cnt += 1
                node_name = f'expression_{self.tmp_node_cnt}'
                self.graph.node(node_name)
                self.graph.edge(parent_node, node_name)
                print('expression')
                if self.get_current_token() == ')':
                    self.i += 1
                    return True
            self.error()




    def expression(self):
        if self.relation():
            node_name = self.generate_unique_node_name('relation')
            self.graph.node(node_name)
            self.graph.edge('expression', node_name)
            print('relation')
            if self.get_current_token() in ('and', 'or', 'xor'):
                self.i += 1
                node_name = self.generate_unique_node_name('logic_operation')
                self.graph.node(node_name)
                self.graph.edge('expression', node_name)
                print('logic operation')
                if self.relation():
                    node_name = self.generate_unique_node_name('relation')
                    self.graph.node(node_name)
                    self.graph.edge('expression', node_name)
                    print('relation')
                    return True
                self.error()
            return True
        else:
            self.error()

    def relation(self):
        node_relation = self.generate_unique_node_name('relation')
        self.graph.node(node_relation)
        if self.simple_expression(node_relation):
            if self.get_current_token() in ('<', '<=', '==', '/>', '>=', '>'):
                self.i += 1
                node_rel_op = self.generate_unique_node_name('relation_operation')
                self.graph.node(node_rel_op)
                self.graph.edge(node_relation, node_rel_op)
                if self.simple_expression(node_relation):
                    return True
                self.error()
            return True
        else:
            self.error()

    def term(self, parent_node):
        if self.factor(parent_node):
            while self.get_current_token() in ('*', '/', 'mod', 'rem'):
                self.i += 1
                if self.factor(parent_node):
                    continue
                else:
                    self.error()
            return True

    def simple_expression(self, parent_node):
        if self.get_current_token() in ('-', '+'):
            self.i += 1
            node_un_add_op = self.generate_unique_node_name('un_add_operation')
            self.graph.node(node_un_add_op)
            self.graph.edge(parent_node, node_un_add_op)
        if self.term(parent_node):
            while self.get_current_token() in ('+', '-', '&'):
                self.i += 1
                node_bin_add_op = self.generate_unique_node_name('bin_add_operation')
                self.graph.node(node_bin_add_op)
                self.graph.edge(parent_node, node_bin_add_op)
                if self.term(parent_node):
                    continue
                else:
                    self.error()
            return True
        else:
            self.error()



    def tail(self):
        if self.get_current_token() == ';':
            self.i += 1
            if self.operator():
                self.graph.node('operator')
                self.graph.edge('tail', 'operator')
                print('operator')
                if self.tail():
                    self.graph.node('tail')
                    self.graph.edge('tail', 'tail')
                    print('tail')
                    return True
                self.error()
            self.error()
        return True

    def render_tree(self):
        self.graph.render('parse_tree', format='png', view=True)

