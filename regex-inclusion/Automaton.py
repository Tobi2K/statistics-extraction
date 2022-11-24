"""Class representing a single, general Automata. Automaton structure inspired by
https://github.com/sdht0/automata-from-regex/tree/master, however many changes had to be made, due to converting from
Python 2 to Python """


class Automaton:
    """A class used to represent an Automaton

    This can be used as a basis for a NFA or DFA

    Attributes
    ----------
    SIGMA : set
        the input alphabet
    STATES : set
        finite non-empty set of states (numbered from 1 to n)
    INIT_STATE : None | int
        initial state; element of STATES
    DELTA : dict
        state-transition function
    FINAL_STATES : list
        set of final states, (possibly empty) subset of self.STATES
    CURRENT_STATE : None | int
        to keep track while traversing
    """
    def __init__(self, sigma=None):
        if sigma is None:
            sigma = {'0', '1'}
        self.SIGMA = sigma  # input alphabet
        self.STATES = set()  # finite non-empty set of states (numbered from 1 to n)
        self.INIT_STATE = None  # initial state; element of self.STATES
        self.DELTA = dict()  # state-transition function
        self.FINAL_STATES = []  # set of final states, (possibly empty) subset of self.STATES
        self.CURRENT_STATE = None  # to keep track while traversing

    @staticmethod
    def epsilon():
        return "##e##"

    def add_state(self, states):
        """Adds a state to the automaton (without any transition to or from)

        Parameters
        ----------
        states : int | list
            single state or list of states to be added

        Returns
        -------
        None
        """
        if isinstance(states, int):
            states = [states]
        for state in states:
            self.STATES.add(state)

    def set_start_state(self, state):
        """Sets the starting state for the automaton

        Parameters
        ----------
        state : int
            Single state that will be the new start state. May be added to list of states.

        Returns
        -------
        None
        """
        self.INIT_STATE = state
        self.add_state(state)

    def add_final_state(self, states):
        """Adds a state to the final states of the automaton

        Parameters
        ----------
        states : int | list
            single state or list of states to be added

        Returns
        -------
        None
        """
        if isinstance(states, int):  # single state
            states = [states]
        for state in states:
            self.add_state(state)
            if state not in self.FINAL_STATES:
                self.FINAL_STATES.append(state)

    def add_transition(self, origin, goal, inp):
        """Adds a transition from 'origin' to 'goal' on 'inp'

        Parameters
        ----------
        origin : int
            Starting state for the transition
        goal : int
            Goal state for the transition
        inp : str
            Letter(s) to use for the transition

        Returns
        -------
        None
        """
        if isinstance(inp, str):
            inp = {inp}
        self.add_state([origin, goal])

        if origin in self.DELTA:
            self.DELTA[origin][goal] = self.DELTA[origin][goal].union(inp) if goal in self.DELTA[origin] else inp
        else:
            self.DELTA[origin] = {goal: inp}

    def add_transitions_from_dict(self, transitions):
        """Adds transition from an existing transition dictionary

        Parameters
        ----------
        transitions : dict
            Starting state for the transition

        Returns
        -------
        None
        """
        for origin, goal in transitions.items():
            for state in goal:
                self.add_transition(origin, state, goal[state])

    def get_goals_by_key(self, states, key):
        """Get all possible goals from 'states' with the transition 'key'

        Parameters
        ----------
        states : int | list
            Single state or list of states from which to get possible goals
        key : str
            Transition letter or string

        Returns
        -------
        list
            all possible goals from 'states' on 'key'
        """
        if isinstance(states, int):
            states = [states]
        goals = set()
        for state in states:
            if state in self.DELTA:
                for goal in self.DELTA[state]:
                    if key in self.DELTA[state][goal]:
                        goals.add(goal)
        return goals

    def get_e_reachable_states(self, start):
        """Get all possible goals from 'start' on an empty transition (i.e. epsilon)

        Parameters
        ----------
        start : int
            State from which to get possible goals

        Returns
        -------
        list
            all possible goals from 'states' on empty transition
        """
        """
        While (Stack not empty) {
           Pop s, the top element of Stack
           for each state t, with edge s→t {
              if t is not present in states {
                 states=states ∪ {t}
                 Push t on Stack
              }
           }
        }
        """
        reachable_states = set()
        stack = {start}
        while len(stack) != 0:
            current_state = stack.pop()
            reachable_states.add(current_state)
            if current_state in self.DELTA:
                for goal in self.DELTA[current_state]:
                    if Automaton.epsilon() in self.DELTA[current_state][goal] and goal not in reachable_states:
                        stack.add(goal)
        return reachable_states

    def get_all_transitions(self, start):
        """Get all possible transitions from 'start'

        Parameters
        ----------
        start : int
            State from which to get transitions

        Returns
        -------
        list
            all transitions from 'states'
        """
        transitions = set()
        if start in self.DELTA:
            for goal in self.DELTA[start]:
                for key in self.DELTA[start][goal]:
                    transitions.add(key)
        return transitions

    def print_automaton(self):
        """Prints automaton overview

        Returns
        -------
        None
        """
        print("\tQ:", self.STATES)
        print("\tq0: ", self.INIT_STATE)
        print("\tF:", self.FINAL_STATES)
        print("\tδ:")
        for origin, goal in self.DELTA.items():
            for state in goal:
                for char in goal[state]:
                    print("\t\t", origin, "->", state, "with '" + char + "'"),

    def shift_automaton(self, start):
        """Shifts the automaton, starting with 'start' as first state

        'start' must be a number.
        The state numbering will be shifted, so that the first state is numbered as 'start' and the last as 'start' + n

        Parameters
        ----------
        start : int
            Starting number for the new automaton

        Returns
        -------
        [Automaton, int]
            [a, next] where 'a' is the shifted automaton beginning at 'start' and 'next' is the next higher state number
        """
        map_ids = {}
        # for every existing state set new state id and increment tracker
        for i in list(self.STATES):
            map_ids[i] = start
            start += 1
        rebuild = Automaton(self.SIGMA)
        rebuild.set_start_state(map_ids[self.INIT_STATE])
        for s in self.FINAL_STATES:
            rebuild.add_final_state(map_ids[s])
        for origin, goal in self.DELTA.items():
            for state in goal:
                rebuild.add_transition(map_ids[origin], map_ids[state], goal[state])
        return [rebuild, start]

    def reconstruct_automaton(self, new_mapping):
        rebuild = Automaton(self.SIGMA)
        for origin, goal in self.DELTA.items():
            for state in goal:
                rebuild.add_transition(new_mapping[origin], new_mapping[state], goal[state])
        rebuild.set_start_state(new_mapping[self.INIT_STATE])
        for s in self.FINAL_STATES:
            rebuild.add_final_state(new_mapping[s])
        return rebuild

    def complete(self):
        """Completes an automaton

        Completing an automaton means adding transition for all letters in the alphabet.
        These transitions all lead to an inescapble state.

        Returns
        -------
        Automaton
            the complete automaton
        """
        [complete, new_state] = self.shift_automaton(1)
        old_states = list(complete.STATES)
        added = False
        for state in old_states:
            for l1 in complete.SIGMA:
                defined = len(complete.get_goals_by_key(state, l1)) != 0
                if not defined:
                    if added:
                        complete.add_transition(state, new_state, l1)
                    else:
                        complete.add_state(new_state)
                        complete.add_transition(state, new_state, l1)
                        for l2 in complete.SIGMA:
                            complete.add_transition(new_state, new_state, l2)
        return complete

    def complement(self):
        """Complement an automaton

        The complement of an automaton is the original automaton with inverted accepting states.
        This means, formerly accepting states become non-accepting states and vice verca.

        Returns
        -------
        Automaton
            the complement of the automaton
        """
        [complement, _] = self.shift_automaton(1)
        all_states = complement.STATES
        final_states = set(complement.FINAL_STATES)
        non_final_states = all_states.difference(final_states)

        complement.FINAL_STATES = []
        for state in list(non_final_states):
            complement.add_final_state(state)
        return complement

    def contains_command(self):
        """Checks whether the automaton contains commands from preprocessing (e.g. '!s')

        Returns
        -------
        bool
            True if automaton includes commands, False otherwise
        """
        for s in self.SIGMA:
            if '!' in s and len(s) > 1:
                return True
        return False
