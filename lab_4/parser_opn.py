import typing 
from node import Node

class Parser:
	def __init__(self):
		pass

	def make_parse_lexem(self, lexem: str):
	    def parse_lexem(lexems: typing.List[str], startPos: int):
	        if startPos < len(lexems) and lexems[startPos] == lexem:
	            return Node(name = lexem, parent_id = startPos, child_id = startPos + 1)
	        return None
	    return parse_lexem

	def attempt_parse(self, lexems: typing.List[str], start_pos: int, parsers: typing.List[typing.Callable[[typing.List[str], int], typing.Optional[Node]]]) -> typing.Optional[Node]:
	    for parser in parsers:
	        result = parser(lexems, start_pos)
	        if result:
	            return result
	    return None

	def parse_with_alternatives(self, lexems: typing.List[str], start_pos: int, alternative_parsers: typing.List[typing.Callable[[typing.List[str], int], typing.Optional[Node]]]) -> typing.Optional[Node]:
	    return self.attempt_parse(lexems, start_pos, alternative_parsers)

	def make_choice(self, alternative_parsers: typing.List[typing.Callable[[typing.List[str], int], typing.Optional[Node]]]) -> typing.Callable[[typing.List[str], int], typing.Optional[Node]]:
	    return lambda lexems, start_pos: self.parse_with_alternatives(lexems, start_pos, alternative_parsers)

	def combinator(self, rules, lexems: typing.List[str], startPos: int):
	    tree = Node('<proxy>')
	    tmp_id = startPos

	    for _ in rules:
	        tmp_node = _(lexems, tmp_id)

	        if tmp_node:
	            tree.add_child_node(tmp_node)
	            tmp_id = tmp_node.child_id
	        else:
	            tree = None
	            break
	    
	    return tree

	def make_combine(self, rules, actions = None):
	    def action_wrapper(lexems: typing.List[str], startPos: int):
	        tree = self.combinator(rules, lexems, startPos)

	        if tree and actions:
	            tree.content = actions(*tree.children)
	        
	        return tree

	    return action_wrapper

	def parse_mult_op(self, lexems, startPos) -> typing.Optional[Node]:
	    tree = self.make_choice([
	        self.make_parse_lexem('*'),
	        self.make_parse_lexem('!'),
	        self.make_parse_lexem('mod'),
	        self.make_parse_lexem('rem'),
	    ])(lexems, startPos)
	    if not tree:
	        return None

	    # tree.name = '<мультипликативная операция>'
	    return tree

	def parse_unar(self, lexems, startPos) -> typing.Optional[Node]:
	    tree = self.make_choice([
	        self.make_parse_lexem('+'),
	        self.make_parse_lexem('-'),
	    ])(lexems, startPos)
	    if not tree:
	        return None

	    # tree.name = '<унарная аддитивная операция>'
	    return tree

	def parse_bin_op(self, lexems, startPos) -> typing.Optional[Node]:
	    tree = self.make_choice([
	        self.make_parse_lexem('+'),
	        self.make_parse_lexem('-'),
	        self.make_parse_lexem('&'),
	    ])(lexems, startPos)
	    if not tree:
	        return None

	    # tree.name = '<бинарная аддитивная операция>'
	    return tree

	def parse_rel_op(self, lexems, startPos) -> typing.Optional[Node]:
	    tree = self.make_choice([
	        self.make_parse_lexem('<'),
	        self.make_parse_lexem('<='),
	        self.make_parse_lexem('='),
	        self.make_parse_lexem('/>'),
	        self.make_parse_lexem('>'),
	        self.make_parse_lexem('>='),
	    ])(lexems, startPos)
	    if not tree:
	        return None

	    # tree.name = '<операция отношения>'
	    return tree

	def parse_log_op(self, lexems, startPos) -> typing.Optional[Node]:
	    tree = self.make_choice([
	        self.make_parse_lexem('and'),
	        self.make_parse_lexem('or'),
	        self.make_parse_lexem('xor'),
	    ])(lexems, startPos)
	    if not tree:
	        return None
	    # tree.name = '<логическая операция>'
	    return tree

	def parse_id(self, lexems, startPos) -> typing.Optional[Node]:
	    if startPos >= len(lexems):
	        return None
	    tree = Node("Name")

	    data = lexems[startPos]
	    if not data.isalpha():
	        return None

	    node = Node(data)
	    node.parent_id = startPos
	    node.child_id = startPos + 1

	    tree.add_child_node(node)

	    tree.content = [data]
	    return tree

	def parse_num(self, lexems, startPos) -> typing.Optional[Node]:
	    if startPos >= len(lexems):
	        return None

	    tree = Node("Numeric literal")

	    try:
	        data = float(lexems[startPos])
	    except:
	        return None

	    node = Node(data)
	    node.parent_id = startPos
	    node.child_id = startPos + 1

	    tree.add_child_node(node)
	    tree.content = [data]

	    return tree

	def parse_first(self, lexems, startPos) -> typing.Optional[Node]:
	    tree = self.make_choice([
	        self.make_combine([
	            self.make_parse_lexem('('),
	            self.parse_expr,
	            self.make_parse_lexem(')'),
	        ], actions=lambda a,b,c: b.content),
	        self.parse_id,
	        self.parse_num,
	    ])(lexems, startPos)
	    if not tree:
	        return None

	    tree.name = 'Primary'
	    return tree

	def parse_mnoz(self, lexems, startPos):
	    tree = self.make_choice([
	        self.make_combine([
	            self.make_parse_lexem('abs'),
	            self.parse_first,
	        ], actions=lambda a, b: [0] + b.content + [a.name]),
	        self.make_combine([
	            self.make_parse_lexem('not'),
	            self.parse_first,
	        ], actions=lambda a, b: [0] + b.content + [a.name]),
	        self.make_combine([
	            self.parse_first,
	            self.make_parse_lexem('**'),
	            self.parse_first
	        ], actions=lambda a, b, c: a.content + c.content + [b.name]),
	        self.parse_first
	    ])(lexems, startPos)
	    if not tree:
	        return None

	    tree.name = 'Factor'
	    return tree

	def parse_slag(self, lexems, startPos):
	    tree = self.make_choice([
	        self.make_combine([
	            self.parse_mnoz,
	            self.parse_mult_op,
	            self.parse_slag
	        ], actions=lambda a, b, c: a.content + c.content + [b.name]),
	        self.parse_mnoz
	    ])(lexems, startPos)
	    if not tree:
	        return None

	    tree.name = 'Term'
	    return tree

	def parse_smpl_stmt2(self, lexems, startPos):
	    tree = self.make_choice([
	        self.make_combine([
	            self.parse_slag,
	            self.parse_bin_op,
	            self.parse_smpl_stmt2
	        ], actions=lambda a, b, c:  a.content + c.content + [b.name]),
	        self.parse_slag
	    ])(lexems, startPos)
	    if not tree:
	        return None

	    tree.name = 'Simple Expression 2'
	    return tree

	def parse_smpl_stmt(self, lexems, startPos):
	    tree = self.make_choice(
	        [
	            self.make_combine([
	                self.parse_unar,
	                self.parse_smpl_stmt2
	            ], actions=lambda a, b: [0] + b.content + [a.name, 0]),
	            self.parse_smpl_stmt2
	        ]
	    )(lexems, startPos)
	    if not tree:
	        return None

	    tree.name = 'Simple Expression'
	    return tree

	def parse_rel(self, lexems, startPos):
	    tree = self.make_choice(
	        [
	            self.make_combine([
	                self.parse_smpl_stmt,
	                self.parse_rel_op,
	                self.parse_rel
	            ], actions=lambda a, b, c: a.content + c.content + [b.name]),
	            self.parse_smpl_stmt
	        ]
	    )(lexems, startPos)
	    if not tree:
	        return None
	    tree.name = 'Relation'
	    return tree

	def parse_expr(self, lexems, startPos):
	    tree = self.make_choice(
	        [
	            self.make_combine([
	                self.parse_rel,
	                self.parse_log_op,
	                self.parse_expr
	                # lambda rel, logop, expr:  logop.name  + rel.content  + expr.content ->
	                # lambda rel, logop, expr:  rel.content + expr.content + logop.name
	            ], actions=lambda rel, logop, expr:  rel.content + expr.content + logop.name),
	            self.parse_rel
	        ]
	    )(lexems, startPos)
	    if not tree:
	        return None

	    tree.name = "Expression"

	    return tree

