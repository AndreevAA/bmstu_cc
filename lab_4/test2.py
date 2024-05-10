def make_parse_lexem(lexem: str):
    def parse_lexem(lexems: typing.List[str], startPos: int):
        if startPos >= len(lexems):
            return None
        if lexems[startPos] == lexem:
            tree = Node(lexem)
            tree.parent_id = startPos
            tree.child_id = startPos + 1
            return tree
        return None
    return parse_lexem


def make_choice(rules):
    def combinator(lexems: typing.List[str], startPos: int):
        for rule in rules:
            node = rule(lexems, startPos)
            if not node:
                continue
            return node

        return None
    return combinator


def make_combine(rules, actions = None):
    def combinator(lexems: typing.List[str], startPos: int):
        tree = Node('<proxy>')
        curPos = startPos
        for rule in rules:
            node = rule(lexems, curPos)
            if not node:
                return None

            tree.add_child_node(node)
            curPos = node.child_id
        return tree

    def action_wrapper(lexems: typing.List[str], startPos: int):
        tree = combinator(lexems, startPos)
        if tree and actions:
            tree.content = actions(*tree.children)
        return tree

    return action_wrapper


def parse_mult_op(lexems: typing.List[str], startPos: int) -> typing.Optional[Node]:
    tree = make_choice([
        make_parse_lexem('*'),
        make_parse_lexem('!'),
        make_parse_lexem('mod'),
        make_parse_lexem('rem'),
    ])(lexems, startPos)
    if not tree:
        return None

    # tree.name = '<мультипликативная операция>'
    return tree


def parse_unar(lexems: typing.List[str], startPos: int) -> typing.Optional[Node]:
    tree = make_choice([
        make_parse_lexem('+'),
        make_parse_lexem('-'),
    ])(lexems, startPos)
    if not tree:
        return None

    # tree.name = '<унарная аддитивная операция>'
    return tree


def parse_bin_op(lexems: typing.List[str], startPos: int) -> typing.Optional[Node]:
    tree = make_choice([
        make_parse_lexem('+'),
        make_parse_lexem('-'),
        make_parse_lexem('&'),
    ])(lexems, startPos)
    if not tree:
        return None

    # tree.name = '<бинарная аддитивная операция>'
    return tree


def parse_rel_op(lexems: typing.List[str], startPos: int) -> typing.Optional[Node]:
    tree = make_choice([
        make_parse_lexem('<'),
        make_parse_lexem('<='),
        make_parse_lexem('='),
        make_parse_lexem('/>'),
        make_parse_lexem('>'),
        make_parse_lexem('>='),
    ])(lexems, startPos)
    if not tree:
        return None

    # tree.name = '<операция отношения>'
    return tree


def parse_log_op(lexems: typing.List[str], startPos: int) -> typing.Optional[Node]:
    tree = make_choice([
        make_parse_lexem('and'),
        make_parse_lexem('or'),
        make_parse_lexem('xor'),
    ])(lexems, startPos)
    if not tree:
        return None
    # tree.name = '<логическая операция>'
    return tree


def parse_id(lexems: typing.List[str], startPos: int) -> typing.Optional[Node]:
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


def parse_num(lexems: typing.List[str], startPos: int) -> typing.Optional[Node]:
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


def parse_first(lexems: typing.List[str], startPos: int) -> typing.Optional[Node]:
    tree = make_choice([
        make_combine([
            make_parse_lexem('('),
            parse_expr,
            make_parse_lexem(')'),
        ], actions=lambda a,b,c: b.content),
        parse_id,
        parse_num,
    ])(lexems, startPos)
    if not tree:
        return None

    tree.name = 'Primary'
    return tree


def parse_mnoz(lexems: typing.List[str], startPos: int) -> typing.Optional[Node]:
    tree = make_choice([
        make_combine([
            make_parse_lexem('abs'),
            parse_first,
        ], actions=lambda a, b: [a.name] + b.content),
        make_combine([
            make_parse_lexem('not'),
            parse_first,
        ], actions=lambda a, b: [a.name] + b.content ),
        make_combine([
            parse_first,
            make_parse_lexem('**'),
            parse_first
        ], actions=lambda a, b, c: [b.name] + a.content + c.content),
        parse_first
    ])(lexems, startPos)
    if not tree:
        return None

    tree.name = 'Factor'
    return tree


def parse_slag(lexems: typing.List[str], startPos: int):
    tree = make_choice([
        make_combine([
            parse_mnoz,
            parse_mult_op,
            parse_slag
        ], actions=lambda a, b, c: [b.name] + a.content + c.content),
        parse_mnoz
    ])(lexems, startPos)
    if not tree:
        return None

    tree.name = 'Term'
    return tree

def parse_smpl_stmt2(lexems: typing.List[str], startPos: int) -> typing.Optional[Node]:
    tree = make_choice([
        make_combine([
            parse_slag,
            parse_bin_op,
            parse_smpl_stmt2
        ], actions=lambda a, b, c: [b.name] + a.content + c.content),
        parse_slag
    ])(lexems, startPos)
    if not tree:
        return None

    tree.name = 'Simple Expression 2'
    return tree

def parse_smpl_stmt(lexems: typing.List[str], startPos: int) -> typing.Optional[Node]:
    tree = make_choice(
        [
            make_combine([
                parse_unar,
                parse_smpl_stmt2
            ], actions=lambda a, b: [a.name, 0] + b.content),
            parse_smpl_stmt2
        ]
    )(lexems, startPos)
    if not tree:
        return None

    tree.name = 'Simple Expression'
    return tree


def parse_rel(lexems: typing.List[str], startPos: int) -> typing.Optional[Node]:

    tree = make_choice(
        [
            make_combine([
                parse_smpl_stmt,
                parse_rel_op,
                parse_rel
            ], actions=lambda a, b, c: [b.name] + a.content + c.content),
            parse_smpl_stmt
        ]
    )(lexems, startPos)
    if not tree:
        return None
    tree.name = 'Relation'
    return tree


def parse_expr(lexems: typing.List[str], startPos: int) -> typing.Optional[Node]:
    tree = make_choice(
        [
            make_combine([
                parse_rel,
                parse_log_op,
                parse_expr
            ], actions=lambda rel, logop, expr: logop.name + rel.content + expr.content),
            parse_rel
        ]
    )(lexems, startPos)
    if not tree:
        return None

    tree.name = "Expression"

    return tree

