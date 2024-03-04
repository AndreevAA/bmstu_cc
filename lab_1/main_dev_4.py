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

def epsilon_closure(states, transitions, epsilon='ε'):
    e_closure = set(states)
    stack = list(states)
    while stack:
        state = stack.pop()
        if state in transitions and epsilon in transitions[state]:
            new_states = transitions[state][epsilon]
            for new_state in new_states:
                if new_state not in e_closure:
                    e_closure.add(new_state)
                    stack.append(new_state)
    return frozenset(e_closure)

def nfa_to_dfa(nfa, start_state, final_states):
    dfa_states = {}  # Состояния ДКА
    dfa_transitions = {}  # Переходы ДКА
    dfa_alphabet = set()  # Алфавит ДКА
    dfa_start_state = epsilon_closure({start_state}, nfa)  # Начальное состояние ДКА
    dfa_states[dfa_start_state] = 0  # Нумерация состояний ДКА
    dfa_final_states = set()  # Конечные состояния ДКА

    stack = [dfa_start_state]
    while stack:
        current_state = stack.pop()
        dfa_transitions[current_state] = {}
        for symbol in nfa[list(current_state)[0]]:
            dfa_alphabet.add(symbol)
            next_states = set()
            for state in current_state:
                if state in nfa and symbol in nfa[state]:
                    next_states |= nfa[state][symbol]
            next_state = epsilon_closure(next_states, nfa)
            if next_state:
                if next_state not in dfa_states:
                    dfa_states[next_state] = len(dfa_states)
                    stack.append(next_state)
                dfa_transitions[current_state][symbol] = next_state
                if final_states & next_state:
                    dfa_final_states.add(next_state)

    return dfa_states, dfa_transitions, dfa_alphabet, dfa_start_state, dfa_final_states

# Построение НКА по регулярному выражению
regex_solution = list(solutions.values())[0]  # Берем первое решение как регулярное выражение
nfa = construct_nfa(regex_solution)

# Преобразование НКА в ДКА
dfa_states, dfa_transitions, dfa_alphabet, dfa_start_state, dfa_final_states = nfa_to_dfa(nfa, 'start', {'end'})

# Отрисовка НКА и ДКА в графвиз
nfa.layout(prog='dot')
nfa.draw('nfa.png')

dfa = pgv.AGraph(strict=False, directed=True)
for state, state_id in dfa_states.items():
    dfa.add_node(state_id, label=str(state), shape='circle')
    if state == dfa_start_state:
        dfa.get_node(state_id).attr['shape'] = 'doublecircle'
    if state in dfa_final_states:
        dfa.get_node(state_id).attr['shape'] = 'doublecircle'
        for from_state, transitions in dfa_transitions.items():
            for symbol, to_state in transitions.items():
                dfa.add_edge(dfa_states[from_state], dfa_states[to_state], label=symbol)

dfa.layout(prog='dot')
dfa.draw('dfa.png')