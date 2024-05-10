import typing


from test import TestController
from parser_opn import Parser
from tree import Tree
from analyzer import StaticAnalyzer

def main():
    # code = "-5+5+7**9 - abs(14 + 12) > 20"
    # # print(tokenize(code))
    # print(StaticAnalyzer(code)._tokens)
    # # print(tokenize(code) == StaticAnalyzer(code)._tokens)
    # # print(StaticAnalyzer(code)._ast)
    # root_node = Parser().parse_expr((StaticAnalyzer(code)._tokens), 0)

    # tree = Tree(root_node)
    # tree.render(picture_name = "parse_tree")
    while True:
        play = int(input("0/1/2 (Exit/Tests/Terminal input)"))

        if play == 1:
            TestController("tests.json").start()
        elif play == 2:
            code = input("Code: ")
            root_node = Parser().parse_expr((StaticAnalyzer(code)._tokens), 0)
            tree = Tree(root_node)
            tree.render(picture_name = "parse_tree")
        else:
            exit()

main()


def test(id_d, out_d):
      tree = parse_expr(tokenize(id_d), 0)
      res = " ".join(map(str,tree.content))
      return "|" + id_d + "|" + out_d + "|" + res + "|" + str(out_d == res) + "|"

