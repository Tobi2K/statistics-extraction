import re

from DFA import *


# Checks whether included (E1) ⊆ includer (E2)
def inclusion(includer: Automaton, included: Automaton):
    """Method to test if two automaton are in an inclusion relation

    This method checks whether included ⊆ includer.
    Parameters
    ----------
    includer : Automaton
        DFA that will be tested as the 'larger' automaton.
    included : Automaton
        DFA that will be tested as the 'smaller' automaton.

    Returns
    -------
    bool
        True if included ⊆ includer, else False
    """
    includer = includer.complement()
    # shift automatons so that state identifiers are unique
    [a2, next_state] = includer.shift_automaton(1)
    [a1, _] = included.shift_automaton(next_state)
    begin = (a1.INIT_STATE, a2.INIT_STATE)  # (p,q)
    # If the alphabet of a1 is not included in a2, a2 cannot include a1
    if not a1.SIGMA.issubset(a2.SIGMA):
        if not a2.contains_command():
            # print("Not included. a1 has letters, not matched by a2 and a2 has no commands.")
            return False
    sigma = a2.SIGMA.union(a1.SIGMA)

    # a1.print_automaton()
    # a2.print_automaton()

    Q = [begin]

    # If the first state is already an accepting state, inclusion is not possible
    if a1.INIT_STATE in a1.FINAL_STATES and a2.INIT_STATE in a2.FINAL_STATES:
        print("Not included. Both automata begin with accepting state.")
        return False

    marked = []

    # iterate over all states in the cross product a2.STATES x a1.STATES
    while len(Q) > 0:
        # currently regarded combined state
        (p, q) = Q.pop()  # (a1, a2)
        # print(p, q)
        # not marked ==> has not been regarded
        if (p, q) not in marked:
            # DFS, by checking every transition for every letter in the combined alphabet
            for letter in sigma:
                # print("letter " + letter)
                a1_letters = []
                if "!" in letter and len(letter) > 1 and len(a1.get_goals_by_key(p, letter)) == 0:
                    # get all transitions, add to list if matches for pattern
                    reg = letter[1:]
                    if reg == 's':
                        reg = r'\s'
                    letters = a1.get_all_transitions(p)
                    # print("letters " + str(letters))
                    for le in letters:
                        if re.match(reg, le):
                            a1_letters.append(le)
                else:
                    a1_letters = [letter]
                # print("letters a1 " + str(a1_letters))
                for let in a1_letters:
                    # check if a transition in a1 is defined
                    goal_a1 = a1.get_goals_by_key(p, let)
                    # print("goal a1 " + str(goal_a1))
                    if len(goal_a1) == 1:
                        # potential transition goal(s) defined in a2
                        goal_a2 = a2.get_goals_by_key(q, let)

                        if len(goal_a2) == 0:
                            a2_letters = []
                            # get all transitions, and find special character
                            letters = a2.get_all_transitions(q)
                            # print("letters " + str(letters))
                            match = let
                            if len(let) > 1 and "!" in let:
                                match = let.replace('!', '\\', 1)
                            # print(match)
                            for le in letters:
                                reg = re.escape(le)
                                if len(le) > 1 and "!" in le:
                                    reg = le.replace('!', '\\', 1)
                                if reg.startswith(r'\[^'):
                                    reg = reg[1:]
                                if re.match(reg, re.escape(match)):
                                    a2_letters.append(le)
                            if len(a2_letters) == 1:
                                goal_a2 = a2.get_goals_by_key(q, a2_letters[0])
                            elif len(a2_letters) == 0:
                                # print("Not included. a1 has letters (e.g. " + match + "), not matched by a2.")
                                return False
                            else:
                                raise Exception("Tried to include a non-deterministic or non-complete automaton.")
                        # print("goal a2 ", goal_a2)
                        # well-defined transition i.e. one state has exactly one letter transition
                        if len(goal_a2) == 1:
                            goal_a1_state = goal_a1.pop()
                            goal_a2_state = goal_a2.pop()
                            # if next state is a combined final state ==> no inclusion
                            if goal_a1_state in a1.FINAL_STATES and goal_a2_state in a2.FINAL_STATES:
                                # print("in goal", (p, q))
                                return False
                            # else append combined goal state to state check and mark current state
                            else:
                                # print("appending ", goal_a1_state, goal_a2_state)
                                Q.append((goal_a1_state, goal_a2_state))
                                marked.append((p, q))
                    # illegal DFA (either non-deterministic i.e >1 transition per state per letter
                    # or non-complete i.e. missing transition for letter
                    elif len(goal_a1) > 1:
                        raise Exception("Tried to include a non-deterministic or non-complete automaton.")
    # if no goal state was found (i.e. no reachable goal exists), a1 is included in a2
    return True
