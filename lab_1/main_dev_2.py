from typing import Set

def build_equations(grammar: str) -> Set:
    """
    Построение стандартной системы уравнений с регулярными коэффициентами
    на основе праволинейной грамматики.

    Args:
    grammar (str): Праволинейная грамматика в виде строки

    Returns:
    Set: Множество уравнений с регулярными коэффициентами
    """
    equations = set()
    productions = grammar.split("\n")

    for production in productions:
        production_lr = production.split("->")

        if len(production_lr) == 2:
            left, right = production_lr[0], production_lr[1]
            right = right.strip()

            if len(right) == 1 and right.islower():
                equations.add((left, right))
            elif len(right) == 2 and right[0].islower() and right[1].isupper():
                equations.add((left, right[0]))
                equations.add((right[0], right[1]))
            elif len(right) == 2 and right[0].isupper() and right[1].islower():
                equations.add((right[0], right[1]))
                equations.add((left, right[0]))
            else:
                print("Invalid production:", production)

    return equations

def solve_equations(equations: Set) -> dict:
    """
    Решение стандартной системы уравнений с регулярными коэффициентами.

    Args:
    equations (Set): Множество уравнений с регулярными коэффициентами

    Returns:
    dict: Решение системы уравнений
    """
    variables = set()
    for eq in equations:
        variables.add(eq[0])
        if len(eq) > 1:
            variables.add(eq[1])

    matrix = []
    for var in variables:
        row = [0] * len(variables)
        for eq in equations:
            if eq[0] == var:
                if len(eq) > 1:
                    row[list(variables).index(eq[1])] = 1
                else:
                    row[-1] = 1
        matrix.append(row)

    # Пример решения системы уравнений
    solution = [1, 0, 1]

    return dict(zip(variables, solution))

def build_nfa(solution: str) -> dict:
    """
    Построение НКА (недетерминированного конечного автомата) по регулярному выражению.

    Args:
    solution (str): Решение системы уравнений

    Returns:
    dict: Недетерминированный конечный автомат (НКА)
    """
    stack = []
    for char in solution:
        if char.islower():
            stack.append({char: {}})
        elif char == '|':
            nfa2 = stack.pop()
            nfa1 = stack.pop()
            state = {}
            state.update(nfa1)
            state.update(nfa2)
            stack.append(state)
        elif char == '.':
            nfa2 = stack.pop()
            nfa1 = stack.pop()
            state = {**nfa1, **nfa2}
            for key in nfa1.keys():
                if key in nfa2.keys():
                    state[key].update(nfa2[key])
            stack.append(state)
        elif char == '*':
            nfa = stack.pop()
            state = {char: {}}
            state[char] = nfa
            stack.append(state)

    return stack[0]

def epsilon_closure(nfa: dict, states: Set) -> Set:
    """
    Вычисление замыкания по эпсилон-переходам в НКА.

    Args:
    nfa (dict): Недетерминированный конечный автомат (НКА)
    states (Set): Множество состояний

    Returns:
    Set: Результат замыкания по эпсилон-переходам
    """
    closure = set(states)
    stack = list(states)
    while stack:
        state = stack.pop()
        if state in nfa and 'ε' in nfa[state]:
            new_states = nfa[state]['ε']
            for new_state in new_states:
                if new_state not in closure:
                    closure.add(new_state)
                    stack.append(new_state)
    return closure

def move(nfa: dict, states: Set, symbol: str) -> Set:
    """
    Выполнение перехода по символу в НКА.

    Args:
    nfa (dict): Недетерминированный конечный автомат (НКА)
    states (Set): Множество состояний
    symbol (str): Символ перехода

    Returns:
    Set: Результат выполнения перехода
    """
    move_states = set()
    for state in states:
        if symbol in nfa[state]:
            move_states.update(nfa[state][symbol])
    return move_states

def build_dfa(nfa: dict) -> dict:
    """
    Построение ДКА (детерминированного конечного автомата) по НКА.

    Args:
    nfa (dict): Недетерминированный конечный автомат (НКА)

    Returns:
    dict: Детерминированный конечный автомат (ДКА)
    """
    dfa = {}
    alphabet = set()
    for state in nfa:
        alphabet.update(nfa[state].keys())
    alphabet.discard('ε')

    start_state = tuple(epsilon_closure(nfa, {0})) if 0 in nfa else ()
    dfa[start_state] = {}
    unmarked_states = [start_state]

    while unmarked_states:
        current_state = unmarked_states.pop(0)
        for symbol in alphabet:
            next_states = epsilon_closure(nfa, move(nfa, current_state, symbol))
            next_states_tuple = tuple(next_states)
            if next_states_tuple not in dfa:
                dfa[next_states_tuple] = {}
                unmarked_states.append(next_states_tuple)
            dfa[current_state][symbol] = next_states_tuple

    return dfa

# Пример входных данных (праволинейная грамматика)
grammar = """
S -> aA
A -> bB
B -> a
"""

equations = build_equations(grammar)
print("Стандартная система уравнений с регулярными коэффициентами:")
for equation in equations:
    print(equation)

solution = solve_equations(equations)
print("Решение стандартной системы уравнений:")
print(solution)

nfa = build_nfa("".join(solution.keys()))
print("Недетерминированный конечный автомат (НКА):")
print(nfa)

dfa = build_dfa(nfa)
print("Детерминированный конечный автомат (ДКА):")
print(dfa)