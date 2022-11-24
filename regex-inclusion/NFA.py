""" Class to create a NFA from a given regular expression """

from AutomatonFactory import AutomatonFactory


class NFA:
    """A class used to represent a DFA

    See also https://en.wikipedia.org/wiki/Nondeterministic_finite_automaton

    Attributes
    ----------
    nfa : Automaton
        the NFA represented by the class instance
    """
    def __init__(self, regex):
        self.nfa_stack = []
        self.op_stack = []
        self.nfa = None
        self.star = '*'
        self.choice = '|'
        self.concat = '&'
        self.operators = [self.star, self.concat, self.choice]
        self.regex = regex
        self.alphabet = [chr(i) for i in range(33, 127)]
        self.alphabet.extend(
            ['−', 'Å', '°', 'µ', 'μ', 'Â', '∞', '¢', '∑', '·', 'Δ', 'γ', '∼', 'α', 'β', '≥', '′', '×', '±', 'Њ',
             u'\u202B', u'\u202C', 'ע', 'ω', 'λ', 'π', '→', 'θ', '•', 'À', 'º', '∈', 'Ϯ', 'ϭ', 'þ', '˚', 'Ϫ', 'σ', 'χ',
             '²', '≤', 'τ', '', '¼', 'à', '〈', '〉', 'Ã', 'δ', 'ζ', 'ο', 'Ν', 'Π', 'ψ', 'ε', 'Ι', 'Σ', 'Κ', 'ι', 'Ζ',
             'Χ', 'Φ', 'ν', 'Γ', 'ξ', 'η', 'Λ', 'Μ', 'Υ', 'υ', 'Θ', 'Τ', 'Ξ', 'Ε', 'φ', 'Ω', 'Η', 'ρ', 'Ψ', 'Ο', 'Ρ',
             'κ', 'Ͻ', 'Ͼ', '£', '≈'])
        self.build_nfa()

    def get_nfa(self):
        return self.nfa

    def print_nfa(self):
        self.nfa.print_automaton()

    def build_nfa(self):
        """Builds a NFA from a given regular expression (in shunting yard format) using thompson's construction.

        See also https://en.wikipedia.org/wiki/Thompson%27s_construction


        Returns
        -------
        Automaton
            the converted Automaton
        """
        lang = set()
        escaped = False
        command = False
        escaped_class = False
        char_store = ''
        for char in self.regex:
            if escaped_class:
                if char == ']' and char_store[-1] != '\\':
                    char_store += char
                    lang.add(char_store)
                    self.nfa_stack.append(AutomatonFactory.default_automaton(char_store))
                    char_store = ''
                    escaped_class = False
                else:
                    char_store += char
            elif command:
                if char == 'e':
                    self.nfa_stack.append(AutomatonFactory.empty_automaton())
                elif char == '[':
                    escaped_class = True
                    char_store = '!['
                else:
                    lang.add('!' + char)
                    self.nfa_stack.append(AutomatonFactory.default_automaton('!' + char))
                command = False
            elif char == '!' and not escaped:
                if escaped:
                    lang.add(char)
                    self.nfa_stack.append(AutomatonFactory.default_automaton(char))
                else:
                    command = True
            elif char == '\\' and not escaped:
                escaped = True
            elif char in self.operators and not escaped:
                if len(self.nfa_stack) < 1:
                    raise Exception("Can't apply %s on empty NFA stack" % char)
                if char == self.star:
                    nfa = self.nfa_stack.pop()
                    self.nfa_stack.append(AutomatonFactory.star_automaton(nfa))
                elif len(self.nfa_stack) < 2:
                    raise Exception("Can't apply %s on less than two NFAs" % char)
                elif char == self.choice:
                    nfa1 = self.nfa_stack.pop()
                    nfa2 = self.nfa_stack.pop()
                    self.nfa_stack.append(AutomatonFactory.choice_automaton(nfa2, nfa1))
                elif char == self.concat:
                    nfa1 = self.nfa_stack.pop()
                    nfa2 = self.nfa_stack.pop()
                    self.nfa_stack.append(AutomatonFactory.concat_automaton(nfa2, nfa1))
                else:
                    raise Exception("Unhandled operator %s!" % char)
            elif char in self.alphabet or escaped:
                if escaped and char == 'e':
                    self.nfa_stack.append(AutomatonFactory.empty_automaton())
                else:
                    lang.add(char)
                    self.nfa_stack.append(AutomatonFactory.default_automaton(char))
                escaped = False
            else:
                raise Exception("Unrecognized letter %s! Consider adding it to your alphabet." % char)

        if len(self.nfa_stack) > 1:  # invalid regex
            raise Exception("Invalid regex.")
        self.nfa = self.nfa_stack.pop()
        self.nfa.SIGMA = lang
