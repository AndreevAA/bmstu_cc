from typing import *
import json
from parser_opn import Parser
from tree import Tree
from analyzer import StaticAnalyzer 
from node import Node
from prettytable import PrettyTable
from test import Test

class TestOPNController:

    def __init__(self, file_path: str):
        self.results = []
        # self.load_tests_from_json(file_path)

        # for _ in self.test_cases:
        #     print(_)

        self.tests = [
    (
        "Книжный пример", 
        "(a + b) * (c + d) - e",
        "a b + c d + * e -"
        ),
    (
        "Составной пример", 
        "-5+5+7**9 - abs(14 + 12) > 20",
        "0 5.0 - 5.0 7.0 9.0 ** 14.0 12.0 + abs - + + 20.0 >"
        ),
    (
        "Простое сложение",
        "x + y",
        "x y +"
    ),
    (
        "Модуль 1",
        "abs(x)",
        "x abs"
    ),
    (
        "Модуль 2",
        "abs(x + y)",
        "x y + abs"
    ),
    (
        "Умножение и вычитание", 
        "abs(x - y * z)",
        "x y z * - abs"
    ),
    (
        "Сложные арифметические операции",
        "abs((x + y) * z - v)",
        "x y + z * v - abs"
    ),
    (
        "Арифметические операции с переменными",
        "a + abs(b * c) - e",
        "a b c * abs e - +"
    ),
    (
        "Арифметические операции с переменными и скобками",
        "abs((a + b) * (c - d))",
        "a b + c d - * abs"
    ),
    (
        "Комбинация арифметических операций",
        "abs(a * b) + d - e",
        "a b * abs d e - +"
    ),
    (
        "Комбинация арифметических операций со скобками", 
        "abs((a * b)) + c - e",
        "a b * abs c e - +"
    ),
    (
        "Комбинация арифметических операций с переменными",
        "a + abs(b * c) - e",
        "a b c * abs e - +"
    ),
    (
        "Комплексные арифметические операции",
        "abs((a + b) * c) - e",
        "a b + c * abs e -"
    ),
    (
        "Комбинация арифметических операций с переменными",
        "a - abs(b * c) + e",
        "a b c * abs e + -"
    )
    ]

        # def convert_to_json(data):
        #     tests = []
        #     for test in data:
        #         test_dict = {
        #             "name": test[0],
        #             "arrange": test[1],
        #             "act": test[2],
        #             "assert": "",
        #             "conclusion": ""
        #         }
        #         tests.append(test_dict)
            
        #     with open("tests.json", "w") as file:
        #         json.dump(tests, file, indent=4)

        # convert_to_json(data)

    # def load_tests_from_json(self, file_path: str) -> List[Test]:
    #     with open(file_path, 'r') as file:
    #         test_data = json.load(file)

    #     test_cases = []
    #     for test_case in test_data:
    #         test_name = test_case['name']
    #         input_data = test_case['arrange']
    #         output_data = test_case['act']
    #         right_result = test_case['assert']
    #         conclusion = ''

    #         test_case = Test(test_name, input_data, output_data, right_result, conclusion)
    #         test_cases.append(test_case)

    #     self.test_cases = test_cases

    # def start(self):
    #     for i in range(len(self.test_cases)):
    #         root_node = Parser().parse_expr((StaticAnalyzer(self.test_cases[i].input_data)._tokens), 0)
    #         self.test_cases[i].output_data = " ".join(map(str, root_node.content))
    #         self.test_cases[i].conclusion = str(self.test_cases[i].output_data == self.test_cases[i].right_result)
    #         print(self.test_cases[i].input_data, " | output:", self.test_cases[i].output_data, " | right", self.test_cases[i].right_result, self.test_cases[i].conclusion)
            
    def start(self):
        x = PrettyTable()

        # Данные для вывода в таблице:
        x.field_names = ["Test name", "Input data", "Output data", "Right data", "Status"]

        for _ in self.tests:
            root_node = Parser().parse_expr((StaticAnalyzer(_[1])._tokens), 0)
            output_data = " ".join(map(str, root_node.content))

            conclusion = output_data == _[2]

            self.results.append(Test(
                _[0],  _[1], output_data, _[2], conclusion))

            tree = Tree(root_node)
            tree.render(picture_name = str("test_opn_" + _[0]))

            x.add_row([_[0], _[1], output_data, _[2], conclusion])
            # print(_[0], " | ", _[1], " | ", output_data, " | ", _[2]," | ", conclusion)

        # Настройка отображения таблицы:
        x.align["Test name"] = "l" # Выравнивание текста в столбце
        x.align["Input data"] = "l" # Выравнивание текста в столбце
        x.align["Output data"] = "l" # Выравнивание текста в столбце
        x.align["Right data"] = "l" # Выравнивание текста в столбце
        x.align["Status"] = "l" # Выравнивание текста в столбце
        x.border = True # Отображать границы таблицы
        x.header = True # Отображать заголовок таблицы
        x.padding_width = 1 # Отступ между ячейками

        print(x)
