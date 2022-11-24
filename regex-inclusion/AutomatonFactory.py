""" 
    Static Class for generating basic structures for an epsilon-NFA 


"""

from Automaton import Automaton


class AutomatonFactory:
    """A static class to create simple, empty, choice, concatenation or star automata.

    Construction as seen in https://en.wikipedia.org/wiki/Thompson%27s_construction

    IMPORTANT: as described in the article above, every automaton has exactly one final state qf,
    which is not co-accessible from any other state.
    """

    @staticmethod
    def default_automaton(inp):
        """Creates a simple 2-state automaton with a transition on 'inp'

        Parameters
        ----------
        inp : str
            Transition string or letter.

        Returns
        -------
        Automaton
            the created automaton
        """
        q = 1
        f = 2
        a = Automaton()
        a.set_start_state(q)
        a.add_final_state(f)
        a.add_transition(q, f, inp)

        return a

    @staticmethod
    def empty_automaton():
        """Creates a simple 2-state automaton with an empty transition

        Returns
        -------
        Automaton
            the created automaton
        """
        q = 1
        f = 2
        a = Automaton()
        a.set_start_state(q)
        a.add_final_state(f)
        a.add_transition(q, f, Automaton.epsilon())

        return a

    @staticmethod
    def choice_automaton(ns: Automaton, nt: Automaton):
        """Creates a choice automaton from two exisiting automata

        In Python Regex a choice is represented as a|b

        Parameters
        ----------
        ns : Automaton
            the first automaton to be merged
        nt : Automaton
            the second automaton to be merged

        Returns
        -------
        Automaton
            the choice automaton
        """
        # for a choice automaton the start state of ns is one after q
        q = 1

        [ns, next_state] = ns.shift_automaton(q + 1)
        [nt, f] = nt.shift_automaton(next_state)

        union_a = Automaton()
        union_a.set_start_state(q)
        union_a.add_final_state(f)
        union_a.add_transition(q, ns.INIT_STATE, Automaton.epsilon())
        union_a.add_transition(q, nt.INIT_STATE, Automaton.epsilon())
        union_a.add_transition(ns.FINAL_STATES[0], f, Automaton.epsilon())
        union_a.add_transition(nt.FINAL_STATES[0], f, Automaton.epsilon())

        # copy transitions from ns and nt respectively
        union_a.add_transitions_from_dict(ns.DELTA)
        union_a.add_transitions_from_dict(nt.DELTA)

        return union_a

    @staticmethod
    def concat_automaton(ns: Automaton, nt: Automaton):
        """Creates a concatenation automaton from two exisiting automata

        In Python Regex a concatenation is represented as ab

        Parameters
        ----------
        ns : Automaton
            the first automaton to be merged
        nt : Automaton
            the second automaton to be merged

        Returns
        -------
        Automaton
            the concatenation automaton
        """
        # for concatenation q and start state of ns are one and the same
        q = 1

        [ns, next_state] = ns.shift_automaton(q)
        # end state of ns and beginning state of nt are merged by having the same state number
        [nt, next_state] = nt.shift_automaton(next_state-1)

        # next_state is the state that follows N(t), however the last state of N(t) is also f
        f = next_state - 1

        concat_a = Automaton()
        concat_a.set_start_state(q)
        concat_a.add_final_state(f)
        # concat_a.add_transition(ns.FINAL_STATES[0], nt.INIT_STATE, Automaton.epsilon())

        # copy transitions from ns and nt respectively
        concat_a.add_transitions_from_dict(ns.DELTA)
        concat_a.add_transitions_from_dict(nt.DELTA)

        return concat_a

    @staticmethod
    def star_automaton(ns: Automaton):
        """Creates a star automaton from two exisiting automata

        In Python Regex a star is represented as a*

        Parameters
        ----------
        ns : Automaton
            the automaton to be repeated

        Returns
        -------
        Automaton
            the star automaton
        """
        # for a star automaton the start state of ns is one after q
        q = 1

        [ns, f] = ns.shift_automaton(q + 1)

        star_a = Automaton()
        star_a.set_start_state(q)
        star_a.add_final_state(f)
        star_a.add_transition(q, ns.INIT_STATE, Automaton.epsilon())
        star_a.add_transition(q, f, Automaton.epsilon())
        star_a.add_transition(ns.FINAL_STATES[0], f, Automaton.epsilon())
        star_a.add_transition(ns.FINAL_STATES[0], ns.INIT_STATE, Automaton.epsilon())

        # copy transitions from ns
        star_a.add_transitions_from_dict(ns.DELTA)

        return star_a
