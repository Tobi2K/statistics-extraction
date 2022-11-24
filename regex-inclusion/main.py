import os
import logging
import time

from NFA import *
from DFA import *

from RegexProcessing import *

from inclusion import inclusion


def get_complete_dfa(inp, output=False):
    nfa = NFA(inp)
    dfa = DFA(nfa.get_nfa())
    complete_dfa = dfa.get_dfa().complete()

    if output:
        print("Regular Expression: ", inp)
        print("NFA: ")
        nfa.print_nfa()
        print("DFA: ")
        dfa.print_dfa()
        print("Complete DFA: ")
        complete_dfa.print_automaton()

    return complete_dfa


def main(begin, end, path):
    """The main utility method to run the inclusion algorithm.

    Parameters
    ----------
    begin : int
        The rule ID the inclusions test should start at.
    end : int
        The rule ID the inclusions test should end at. If end < begin, end will be ignored.

    Returns
    -------
    None
    """
    try:
        os.remove('debug1.log')
    except OSError:
        pass
    try:
        os.rename('debug.log', 'debug1.log')
    except OSError:
        pass

    logging.basicConfig(filename='debug.log', level=logging.DEBUG, filemode='a',
                        format='%(asctime)s | %(levelname)s | %(name)s | %(message)s')
    logging.info("Logging enabled.")
    inclusions = open('inclusion.log', 'a', encoding='utf-8-sig')
    file = open(path, 'r', encoding='utf-8-sig')
    included_count_file = open('included-count.txt', 'w')
    included_rules = open('included-rules.txt', 'w')
    rules = file.read().splitlines()
    upper_bound = end
    if end == -1 or end < begin:
        upper_bound = len(rules)
    rule_id = 0
    full_inclusion_list = []
    for r1 in rules:
        if rule_id < begin:
            full_inclusion_list.append([])
            rule_id += 1
            continue
        if rule_id > upper_bound:
            break
        print("Progress:", rule_id + 1, '/', len(rules), "; rule_id:", rule_id)
        logging.info("r1 (%s): %s", rule_id, r1)
        start = time.time()
        included_ids = []
        included_count = 0
        [r1_processed, no_guarantee] = Regexer.preprocess(r1)
        if no_guarantee:
            logging.info("Rule %s contains ambiguity: %s", rule_id, r1)
        r1_dfa = get_complete_dfa(r1_processed)
        r2_id = 0
        for r2 in rules:
            logging.debug("r2 (%s): %s", r2_id, r2)
            if r2_id == rule_id:
                r2_id += 1
                continue

            [r2_processed, no_guarantee2] = Regexer.preprocess(r2)
            r2_dfa = get_complete_dfa(r2_processed)

            if inclusion(r1_dfa, r2_dfa):
                logging.debug("Rule %s includes %s", rule_id, r2_id)
                included_count += 1
                if no_guarantee2:
                    included_ids.append(str(r2_id) + "?")
                else:
                    included_ids.append(r2_id)
            r2_id += 1

        end = time.time()
        logging.info("Rule %s includes  %s rules. IDs: %s", rule_id, included_count, included_ids)
        inclusions.write(
            "Rule " + str(rule_id) + " includes " + str(included_count) + " rules. IDs: " + str(included_ids) + '\n')
        included_rules.write(str(rule_id) + "  " + str(included_ids) + '\n')
        included_count_file.write(str(rule_id) + "  " + str(included_count) + "  " + str(included_ids) + '\n')
        logging.info("Rule %s took %s seconds", rule_id, (end - start))
        rule_id += 1
        full_inclusion_list.append(included_ids)

    included_rules.close()
    included_count_file.close()
    inclusions.close()
    file.close()
    return full_inclusion_list


if __name__ == '__main__':
    # Parse arguments
    import argparse

    parser = argparse.ArgumentParser(description='Run regular expression inclusion.',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    # general arguments
    parser.add_argument('--begin', type=int, help='ID of rule to begin with.', default=0)
    parser.add_argument('--end', type=int, help='ID of rule to begin with.', default=-1)
    parser.add_argument('--path', type=str, help='Location of the regex list', default='./rMinus.txt')

    args = parser.parse_args()
    #main(args.begin, args.end, args.path)
    [r1_processed, no_guarantee] = Regexer.preprocess(r'a(b|c)a*', True)
    r1_dfa = get_complete_dfa(r1_processed, True)
