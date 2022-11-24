""" Class to transform a NFA into a DFA """

from Automaton import Automaton


class DFA:
    """A class used to represent a DFA

    See also https://en.wikipedia.org/wiki/Deterministic_finite_automaton

    Attributes
    ----------
    dfa : Automaton
        the DFA represented by the class instance
    """

    def __init__(self, nfa: Automaton):
        self.dfa = Automaton(nfa.SIGMA)
        self.build_dfa(nfa)

    def get_dfa(self):
        return self.dfa

    def print_dfa(self):
        self.dfa.print_automaton()

    def build_dfa(self, nfa: Automaton):
        """Builds a DFA from a given NFA using powerset construction.

        See also https://en.wikipedia.org/wiki/Powerset_construction

        Parameters
        ----------
        nfa : Automaton
            The NFA to be converted

        Returns
        -------
        Automaton
            the converted Automaton
        """
        # initialize DFA
        dfa = Automaton(nfa.SIGMA)
        dfa.set_start_state(1)

        # start state of the DFA is the ε-closure of the NFA start state
        epsilon_sets = dict()
        epsilon_starts = nfa.get_e_reachable_states(nfa.INIT_STATE)
        epsilon_sets[nfa.INIT_STATE] = epsilon_starts

        # keep track of added/reached states
        all_states = dict()
        all_states[1] = epsilon_starts

        # add first powerset-state to stack for processing
        state_stack = [[1, epsilon_starts]]
        if nfa.FINAL_STATES[0] in epsilon_starts:
            dfa.add_final_state(1)

        # index is the state numbering of the new DFA
        index = 2
        while len(state_stack) != 0:
            # get current state
            [state_index, state] = state_stack.pop()

            # compute all successors s of q ∈ S in the NFA, where S is the current powerset-state `state`
            for char in dfa.SIGMA:
                # get successors
                reachable = nfa.get_goals_by_key(state, char)

                # compute the ε-closure of s and save them in epsilon_sets to save computation later
                for s in list(reachable):
                    epsilon_sets[s] = nfa.get_e_reachable_states(s)
                    # append all new reachable states to `reachable` powerset-state
                    reachable = reachable.union(epsilon_sets[s])
                # skip, if no states are reachable
                if len(reachable) != 0:
                    # copy next state number
                    goal = index
                    # add a new state, if reachable powerset-state is not considered yet
                    if reachable not in all_states.values():
                        state_stack.append([index, reachable])
                        all_states[index] = reachable
                        index += 1
                    # else, get existing goal of created powerset-state `reachable`
                    else:
                        goal = [key for key, val in all_states.items() if val == reachable][0]
                    # add `reachable` powerset-state as a final state, if any state in the powerset-state
                    # is a final state in the given NFA
                    if nfa.FINAL_STATES[0] in reachable:
                        dfa.add_final_state([key for key, val in all_states.items() if val == reachable])
                    # add transition from created state to goal state, with the current char
                    dfa.add_transition(state_index, goal, char)

        self.dfa = dfa