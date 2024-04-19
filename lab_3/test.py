from __future__ import annotations
import IPython
from graphviz import Digraph



class ParseNode:
    data = ""
    children: list[ParseNode]
    from_ = -1
    to_ = -1

    def __init__(self, data) -> None:
        self.data = data
        self.children = []
        pass

    def add_child(self, node: ParseNode):
        if not len(self.children):
            self.from_ = node.from_
        self.to_ = node.to_

        if node.data in ["<proxy>"]:
            for ch in node.children:
                self.add_child(ch)
            return

        self.children.append(node)

    def print(self, tree=None, parent="", id="main"):
        from graphviz import Digraph

        if not tree:
            tree = Digraph()
            tree.node_attr["shape"] = "plain"
        tree.node(id, str(self.data))
        if parent:
            tree.edge(parent, id)

        # print("IN:",  self.data, [ch.data for ch in self.children])
        for i, child in enumerate(self.children):
            child.print(tree, id, id + "." + str(i))
        # print("OUT:",  self.data, [ch.data for ch in self.children])

        return tree


def make_parse_lexem(lexem: str):
    def parse_lexem(lexems: list[str], startPos: int):
        if startPos >= len(lexems):
            return None
        if lexems[startPos] == lexem:
            tree = ParseNode(lexem)
            tree.from_ = startPos
            tree.to_ = startPos + 1
            return tree
        return None

    return parse_lexem


def make_choice(rules):
    def combinator(lexems: list[str], startPos: int):
        for rule in rules:
            node = rule(lexems, startPos)
            if not node:
                continue
            tree = ParseNode("<proxy>")
            tree.add_child(node)
            return tree

        return None

    return combinator


def make_combine(rules):
    def combinator(lexems: list[str], startPos: int):
        tree = ParseNode("<proxy>")
        curPos = startPos
        for rule in rules:
            node = rule(lexems, curPos)
            if not node:
                return None

            tree.add_child(node)
            curPos = node.to_
        return tree

    return combinator


def make_loop(rule):
    def looper(lexems: typing.List[str], startPos: int):
        tree = ParseNode("<proxy>")
        tree.from_ = startPos
        tree.to_ = startPos

        curPos = startPos
        while True:
            node = rule(lexems, curPos)
            if not node:
                break
            curPos = node.to_
            tree.add_child(node)

        return tree

    return looper


def make_optional(rule):
    def ret_empty(pos):
        node = ParseNode("<proxy>")
        node.from_ = pos
        node.to_ = pos
        return node

    def opter(lexems: list[str], startPos: int):
        node = rule(lexems, startPos)
        if not node:
            return ret_empty(startPos)
        return node

    return opter


def parse_rel_op(lexems: list[str], startPos: int) -> ParseNode | None:
    tree = make_choice(
        [
            make_parse_lexem("<"),
            make_parse_lexem("<="),
            make_parse_lexem("="),
            make_parse_lexem(">="),
            make_parse_lexem(">"),
            make_parse_lexem("!="),
        ]
    )(lexems, startPos)
    if not tree:
        return None

    tree.data = "<операция отношения>"
    return tree


def parse_mult_op(lexems: list[str], startPos: int) -> ParseNode | None:
    tree = make_choice(
        [
            make_parse_lexem("*"),
            make_parse_lexem("/"),
            make_parse_lexem("%"),
        ]
    )(lexems, startPos)
    if not tree:
        return None

    tree.data = "<операция типа умножение>"
    return tree


def parse_sum_op(lexems: list[str], startPos: int) -> ParseNode | None:
    tree = make_choice(
        [
            make_parse_lexem("+"),
            make_parse_lexem("-"),
        ]
    )(lexems, startPos)
    if not tree:
        return None

    tree.data = "<операция типа сложение>"
    return tree


def parse_id(lexems: list[str], startPos: int) -> ParseNode | None:
    if startPos >= len(lexems):
        return None
    tree = ParseNode("<идентификатор>")

    data = lexems[startPos]
    if not data.isalpha():
        return None

    node = ParseNode(data)
    node.from_ = startPos
    node.to_ = startPos + 1

    tree.add_child(node)
    return tree


def parse_num(lexems: list[str], startPos: int) -> ParseNode | None:
    if startPos >= len(lexems):
        return None

    tree = ParseNode("<число>")

    try:
        data = float(lexems[startPos])
    except:
        return None

    node = ParseNode(data)
    node.from_ = startPos
    node.to_ = startPos + 1

    tree.add_child(node)
    return tree


def parse_first_exp(lexems: list[str], startPos: int) -> ParseNode | None:
    tree = make_choice(
        [
            make_combine(
                [
                    make_parse_lexem("("),
                    parse_arythmetical_stmt,
                    make_parse_lexem(")"),
                ]
            ),
            parse_id,
            parse_num,
        ]
    )(lexems, startPos)
    if not tree:
        return None

    tree.data = "<первичное выражение>"
    return tree


def parse_multiplier(lexems: list[str], startPos: int) -> ParseNode | None:
    tree = make_combine(
        [
            parse_first_exp,
            make_optional(make_combine([make_parse_lexem("^"), parse_multiplier])),
        ]
    )(lexems, startPos)
    if not tree:
        return None

    tree.data = "<множитель>"
    return tree


def parse_term(lexems: list[str], startPos: int) -> ParseNode | None:
    tree = make_combine(
        [parse_multiplier, make_optional(make_combine([parse_mult_op, parse_term]))]
    )(lexems, startPos)
    if not tree:
        return None

    tree.data = "<терм>"
    return tree


def parse_arythmetical_stmt(lexems: list[str], startPos: int) -> ParseNode | None:
    tree = make_combine(
        [
            make_optional(parse_sum_op),
            parse_term,
            make_loop(
                make_combine(
                    [
                        parse_sum_op,
                        parse_term,
                    ]
                )
            ),
        ]
    )(lexems, startPos)
    if not tree:
        return None

    tree.data = "<арифметическое выражение>"
    return tree


def parse_expr(lexems: list[str], startPos: int) -> ParseNode | None:
    tree = make_combine(
        [
            parse_arythmetical_stmt,
            parse_rel_op,
            parse_arythmetical_stmt,
        ]
    )(lexems, startPos)
    if not tree:
        return None

    tree.data = "<выражение>"

    return tree

def tokenize(code: str):
    tokens = []
    curPos = 0
    while curPos < len(code):
        if code[curPos : min(curPos + 2, len(code))] in ["<=", ">=", "!="]:
            tokens += [code[curPos : min(curPos + 2, len(code))]]
            curPos += 2
        elif code[curPos] in ['+', '-', '*', '/', '%', '<', '=', '>', '(', ')', '{', '}', ';', '^']:
            tokens += [code[curPos]]
            curPos += 1
        elif code[curPos] in [" ", "\t", "\n", "\r"]:
            curPos += 1
        else:
            startpos = curPos
            while curPos < len(code) and (
                code[curPos].isalpha()
                or code[curPos].isnumeric()
                or code[curPos] in ["_", "."]
            ):
                curPos += 1
            tokens += [code[startpos:curPos]]
            if startpos == curPos:
                print("ERROR")
                break
        # print(tokens[-1])
    return tokens

code = "a := 3 ; aaa := p ; { a := p ; x := p and not p } "
print(tokenize(code))
tree = parse_expr(tokenize(code), 0)
# tree.print()

def parse_operator(lexems: list[str], startPos: int) -> ParseNode | None:
    tree = make_combine([parse_id, make_parse_lexem("="), parse_expr])(lexems, startPos)
    if not tree:
        return None

    tree.data = "<оператор>"

    return tree


def parse_operator_list(lexems: list[str], startPos: int) -> ParseNode | None:
    tree = make_combine(
        [
            parse_operator,
            make_loop(
                make_combine(
                    [
                        make_parse_lexem(";"),
                        parse_operator,
                    ]
                )
            ),
            make_parse_lexem(";"),
        ]
    )(lexems, startPos)
    if not tree:
        return None

    tree.data = "<список  операторов>"

    return tree


def parse_block(lexems: list[str], startPos: int) -> ParseNode | None:
    tree = make_combine(
        [
            make_parse_lexem("{"),
            parse_operator_list,
            make_parse_lexem("}"),
        ]
    )(lexems, startPos)
    if not tree:
        return None

    tree.data = "<блок>"

    return tree


def parse_program(lexems: list[str], startPos: int) -> ParseNode | None:
    tree = ParseNode("<выражение>")

    node = parse_block(lexems, startPos)
    if not node:
        return None

    tree.add_child(node)

    return tree

code = """
{
    one = (4 + (6 ^ 11)) > 10;
    two = (0.5 ^ 11 + 13 ^ 0.5) != 1;
}
"""

print(tokenize(code))
tree = parse_program(tokenize(code), 0)
# tree.print()

def render_tree(tree, filename):
    dot = Digraph(comment='Parse Tree')
    
    def add_nodes_edges(tree, parent_id=None, dot=None):
        if dot is None:
            dot = Digraph()
            dot.attr('node', shape='box')

        node_id = str(id(tree))  # Уникальный идентификатор узла

        dot.node(node_id, label=str(tree.data))  # Используем уникальный идентификатор как название узла

        if parent_id is not None:
            dot.edge(parent_id, node_id) 

        for child in tree.children:
            add_nodes_edges(child, node_id, dot)

        return dot

    dot = add_nodes_edges(tree)
    dot.render(filename, format='png', view=True)

render_tree(tree, 'parse_tree')


