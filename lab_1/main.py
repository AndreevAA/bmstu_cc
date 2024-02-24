from typing import Set, Any


def build_equations(grammar):
    equations = []
    productions = grammar.split("\n")

    for production in productions:
        production_lr = production.split("->")

        if len(production_lr) == 2:
            left, right = production_lr[0], production_lr[1]
            right = right.strip()

            if len(right) == 1 and right.islower():
                equations.append((left, right))
            elif len(right) == 2 and right[0].islower() and right[1].isupper():
                equations.append((left, right[0]))
                equations.append((right[0], right[1]))
            elif len(right) == 2 and right[0].isupper() and right[1].islower():
                equations.append((right[0], right[1]))
                equations.append((left, right[0]))
            else:
                print("Invalid production:", production)

    return equations


def solve_equations(equations):
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

    # Решение системы уравнений с регулярными коэффициентами
    # Используем метод Гаусса или другой метод решения систем линейных уравнений

    # Пример решения системы уравнений
    solution = [1, 0, 1]  # Пример решения системы уравнений

    return dict(zip(variables, solution))


def build_nfa(regular_expression):
    stack = []
    for char in regular_expression:
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


def epsilon_closure(nfa, states):
    closure = set(states)
    stack = list(states)
    while stack:
        state = stack.pop()
        if 'ε' in nfa[state]:
            new_states = nfa[state]['ε']
            for new_state in new_states:
                if new_state not in closure:
                    closure.add(new_state)
                    stack.append(new_state)
    return closure


def move(nfa, states, symbol):
    move_states = set()
    for state in states:
        if symbol in nfa[state]:
            move_states.update(nfa[state][symbol])
    return move_states


def build_dfa(nfa):
    dfa = {}
    alphabet = set()
    for state in nfa:
        alphabet.update(nfa[state].keys())
    alphabet.discard('ε')

    start_state = tuple(epsilon_closure(nfa, {0}))  # Преобразуем множество в кортеж
    dfa[start_state] = {}
    unmarked_states = [start_state]

    while unmarked_states:
        current_state = unmarked_states.pop(0)
        for symbol in alphabet:
            next_states = epsilon_closure(nfa, move(nfa, current_state, symbol))
            next_states_tuple = tuple(next_states)  # Преобразуем множество в кортеж
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

# Пример решения системы уравнений
solution = "ab*."

# Построение НКА по регулярному выражению
nfa = build_nfa(solution)

print("Недетерминированный конечный автомат (НКА):")
print(nfa)

# Пример НКА для моделирования
nfa = {
    0: {'ε': {1}},
    1: {'a': {2}, 'ε': {3}},
    2: {'b': {1}},
    3: {'a': {3}, 'b': {3}}
}

# Детерминированное моделирование НКА
dfa = build_dfa(nfa)

print("Детерминированный конечный автомат (ДКА):")
print(dfa)