import typing


from test_recurtion import TestRecurtionController
from test_opn import TestOPNController
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
            TestRecurtionController("tests.json").start()
            TestOPNController("tests_recurtion.json").start()
        elif play == 2:
            # code = "-5+5+7**9 - abs(14 + 12) > 20"#input("Code: ")
            code = "(a + b) * (c + d) - e"
            root_node = Parser().parse_expr((StaticAnalyzer(code)._tokens), 0)
            tree = Tree(root_node)
            tree.render(picture_name = "parse_tree")
            print(" ".join(map(str, root_node.content)))
        else:
            exit()

main()


def test(id_d, out_d):
      tree = parse_expr(tokenize(id_d), 0)
      res = " ".join(map(str,tree.content))
      return "|" + id_d + "|" + out_d + "|" + res + "|" + str(out_d == res) + "|"

