import numpy as np
import numpy as np
import pygraphviz as pgv

def solve_equations(system, nonterminals):
    A = np.array(system)
    b = np.zeros(len(system))
    b[0] = 1  # Устанавливаем значение для стартового символа

    # Решаем систему уравнений методом наименьших квадратов
    solution = np.linalg.lstsq(A, b, rcond=None)[0]

    # Формируем словарь с решениями для каждого нетерминала
    solutions_dict = {nonterminals[i]: round(solution[i], 2) for i in range(len(nonterminals))}

    return solutions_dict


def identify_terminals_nonterminals(grammar):
    terminals = set()
    nonterminals = set()

    for rule in grammar:
        left, right = rule.split('->')
        left = left.strip()
        right = right.strip().split('|')

        nonterminals.add(left)

        for term in right:
            terms = term.split()
            for t in terms:
                if not t.isupper() and t != '':  # Terminal
                    terminals.add(t)
                elif t.isupper():  # Nonterminal
                    nonterminals.add(t)

    return terminals, nonterminals


def convert_to_equations(grammar):
    equations = []
    nonterminals = set()

    for rule in grammar:
        left, right = rule.split('->')
        left = left.strip()
        right = right.strip().split('|')

        for term in right:
            equation = []
            terms = term.split()

            for t in terms:
                if t.isupper():  # Nonterminal
                    nonterminals.add(t)
                    equation.append(t)
                else:  # Terminal
                    equation.append(t)

            equations.append(equation)

    # Constructing the system of equations
    system = []
    for eq in equations:
        coeff = [1 if x in eq else 0 for x in nonterminals]
        system.append(coeff)

    return system, list(nonterminals)


# Пример праволинейной грамматики
grammar = [
    "S -> a A | b B",
    "A -> a A | b",
    "B -> a B | a"
]

terminals, nonterminals = identify_terminals_nonterminals(grammar)
system, nonterminals = convert_to_equations(grammar)

print("Терминалы:")
print(terminals)

print("\nНетерминалы:")
print(nonterminals)

print("\nСистема уравнений:")
for eq in system:
    print(eq)

solutions = solve_equations(system, nonterminals)
print("\nРешения для нетерминалов:")
for key, value in solutions.items():
    print(f"{key}: {value}")


def construct_nfa(regex_solution):
    G = pgv.AGraph(strict=False, directed=True)

    # Добавляем начальное и конечное состояния
    G.add_node('start', shape='point')
    G.add_node('end', shape='doublecircle')

    # Преобразуем значение regex_solution в строку
    regex_solution = str(regex_solution)

    # Добавляем ребра в НКА
    for i, char in enumerate(regex_solution):
        G.add_node(str(i))
        G.add_edge('start', str(i), label=char)
        if i < len(regex_solution) - 1:
            G.add_edge(str(i), str(i + 1), label='ε')
        else:
            G.add_edge(str(i), 'end', label='ε')

    return G

# Построение НКА по регулярному выражению
regex_solution = list(solutions.values())[0]  # Берем первое решение как регулярное выражение
nfa = construct_nfa(regex_solution)

# Отрисовка НКА в графвиз
nfa.layout(prog='dot')
nfa.draw('nfa.png')
