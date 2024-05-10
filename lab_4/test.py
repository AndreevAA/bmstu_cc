from typing import *
import json
from parser import Parser
from tree import Tree
from analyzer import StaticAnalyzer 
from node import Node
from prettytable import PrettyTable

class Test:
    def __init__(self, name, input_data, output_data, right_result, conclusion):
        self.name = name
        self.input_data = input_data
        self.output_data = output_data
        self.right_result = right_result
        self.conclusion = conclusion
