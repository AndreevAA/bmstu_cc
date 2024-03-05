import numpy as np
import pygraphviz as pgv

def epsilon_closure(nfa, states):
    epsilon_states = set(states)
    stack = list(epsilon_states)

    while stack:
        current_state = stack.pop()
        if 'ε' in nfa[current_state]:
            for state in nfa[current_state]['ε']:
                if state not in epsilon_states:
                    epsilon_states.add(state)
                    stack.append(state)

    return epsilon_states

def move(nfa, states, symbol):
    next_states = set()
    for state in states:
        if symbol in nfa[state]:
            next_states.update(nfa[state][symbol])
    return next_states

def nfa_to_dfa(nfa):
    dfa = {}
    alphabet = set()
    start_state = frozenset(epsilon_closure(nfa, {'start'}))
    dfa[start_state] = {}
    stack = [start_state]

    while stack:
        current_states = stack.pop()
        for symbol in nfa['alphabet']:
            alphabet.add(symbol)
            next_states = frozenset(epsilon_closure(nfa, move(nfa, current_states, symbol)))
            dfa[current_states][symbol] = next_states
            if next_states not in dfa:
                dfa[next_states] = {}
                stack.append(next_states)

    return dfa, alphabet

# Пример НКА
nfa = {
    'alphabet': {'a', 'b'},
    'start': {'q0'},
    'q0': {'ε': {'q1'}},
    'q1': {'a': {'q1'}, 'b': {'q2'}},
    'q2': {'a': {'q1'}}
}

# Детерминированное моделирование НКА
dfa, alphabet = nfa_to_dfa(nfa)

# Вывод полученного ДКА
print("Детерминированный конечный автомат (ДКА):")
for state in dfa:
    print(state, dfa[state])
print("Алфавит:", alphabet)

# Отрисовка полученного ДКА в Graphviz
def construct_dfa_graph(dfa):
    G = pgv.AGraph(strict=False, directed=True)

    for state in dfa:
        for symbol in dfa[state]:
            target_state = dfa[state][symbol]
            G.add_edge(str(state), str(target_state), label=symbol)

    return G

dfa_graph = construct_dfa_graph(dfa)
dfa_graph.layout(prog='dot')
dfa_graph.draw('dfa.png')