from ast import literal_eval

grammar_filename = 'g1.txt'


class Grammar:

    def __init__(self, grammar_filename):
        self.start_grammar, self.grammar = {}, {}

        if self.__upload_from_the_file(grammar_filename) == 0:
            self.set_grammar_to_start_grammar()
            print("Success: grammar file upload")
        else:
            print("Error: grammar file upload")

    def set_grammar_to_start_grammar(self):
        self.grammar = self.start_grammar

    # Uploading grammar from the file
    def __upload_from_the_file(self, grammar_filename):
        grammar_filename = open(grammar_filename)

        try:
            for _ in grammar_filename:
                left_term, right_term = (_.strip()).split('=')
                left_term, right_term = left_term.strip(), right_term.strip()

                if left_term in self.start_grammar:
                    self.start_grammar[left_term].add(right_term)
                else:
                    self.start_grammar[left_term] = {right_term}
            return 0
        except Exception:
            return -1

    # Output grammar
    def output_grammar(self):
        for left_term in sorted(self.grammar):
            for right_term in sorted(self.grammar[left_term]):
                print(left_term, '=', *right_term)

    # Is term non-terminal
    def __is_non_terminal(self, terminal):
        if terminal.isupper():
            return True
        return False

    # Finding non-terminals in the right terms
    def __get_non_terminals(self):
        non_terminals = sorted(self.grammar)

        for left_term in sorted(self.grammar):
            for right_term in sorted(self.grammar[left_term]):
                for alfa in right_term:

                    # Alfa non terminal (uppercase)
                    if self.__is_non_terminal(alfa):
                        if not non_terminals.__contains__(alfa):
                            non_terminals.append(alfa)

        return non_terminals

    # Finding all parent non-terminals
    def __get_parent_non_terminals(self, non_terminals):
        parent_non_terminals = {()}

        # parent_non_terminals from left side terminals
        for tmp_non_terminal in non_terminals:
            # Is tmp_non_terminal on the left side of grammar
            if self.grammar.keys().__contains__(tmp_non_terminal):
                # Right side by the key
                tmp_value = self.grammar[tmp_non_terminal]

                for right_term in tmp_value:
                    # Not terminals of tmp_non_terminal with children on the right side
                    if not any(tmp_nt in non_terminals for tmp_nt in right_term):
                        parent_non_terminals.add(tmp_non_terminal)

        # Removing initialized ()
        parent_non_terminals.remove(())

        # parent_non_terminals from right side terminals
        start_parent_non_terminals_length = len(parent_non_terminals)

        while True:
            start_len_parent = len(parent_non_terminals)
            for tmp_non_terminal in non_terminals:
                if self.grammar.keys().__contains__(tmp_non_terminal):
                    for r_product in self.grammar[tmp_non_terminal].copy():
                        cnt = 0
                        for alpha in r_product:
                            if non_terminals.__contains__(alpha):
                                if parent_non_terminals.__contains__(alpha):
                                    cnt = 1
                                else:
                                    cnt = 0
                                    break
                        if cnt == 1:
                            parent_non_terminals.add(tmp_non_terminal)
            if start_len_parent == len(parent_non_terminals):
                break

        return parent_non_terminals

    # Do right term contains only parent non-terminals
    def __right_term_contains_only_parent_non_terminals(self, non_terminals, parent_non_terminals, right_term):
        state = False

        for alfa in right_term:
            if non_terminals.__contains__(alfa):
                if parent_non_terminals.__contains__(alfa):
                    state = True
                else:
                    return False

        return state

    # Deleting parent non terminal
    def delete_parent_non_terminal(self):

        # Getting all non-terminals
        non_terminals = self.__get_non_terminals()

        # Getting all parent non terminals
        parent_non_terminals = self.__get_parent_non_terminals(non_terminals)

        # Deleting l_terms
        for left_term in sorted(self.grammar):
            if not (parent_non_terminals.__contains__(left_term)):
                self.grammar.pop(left_term)

        # Deleting r_terms
        for left_term in sorted(self.grammar):
            tmp_value = self.grammar[left_term].copy()

            for right_term in tmp_value:
                for alpha in right_term:
                    if non_terminals.__contains__(alpha):
                        if not parent_non_terminals.__contains__(alpha):
                            self.grammar[left_term].remove(right_term)

    # Getting all unreachable_non_terminals
    def __get_unreachable_non_terminals(self, non_terminals):
        unreachable_non_terminals = {()}
        unreachable_non_terminals.add(list(self.grammar)[0])
        unreachable_non_terminals.remove(())

        while True:
            unreachable_non_terminals_len = len(unreachable_non_terminals)
            for l_product in sorted(self.grammar):
                if unreachable_non_terminals.__contains__(l_product):
                    for r_product in sorted(self.grammar[l_product]):
                        for alpha in r_product:
                            if non_terminals.__contains__(alpha):
                                unreachable_non_terminals.add(alpha)

            if unreachable_non_terminals_len == len(unreachable_non_terminals):
                break

        return unreachable_non_terminals

    # Deleting unreachable non-terminals
    def delete_unreachable_non_terminals(self):

        # Getting all non-terminals
        non_terminals = self.__get_non_terminals()

        # Getting all unreachable_non_terminals
        unreachable_non_terminals = self.__get_unreachable_non_terminals(non_terminals)

        # Deleting unreachable
        for left_term in sorted(self.grammar):
            if not unreachable_non_terminals.__contains__(left_term):
                self.grammar.pop(left_term)


grammar = Grammar(grammar_filename)

print("Исходная грамматика")
grammar.output_grammar()

print("Удаление непорождающих грамматика")
grammar.set_grammar_to_start_grammar()
grammar.delete_parent_non_terminal()
grammar.output_grammar()

print("Удаление недостижимых нетерминалов")
grammar.set_grammar_to_start_grammar()
grammar.delete_unreachable_non_terminals()
grammar.output_grammar()



