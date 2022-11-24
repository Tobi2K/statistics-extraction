""" Static Class to clean and standardize regular expressions """


class Regexer:
    """A static class used to preprocess regular expressions"""

    @staticmethod
    def fill_operators(inp: str):
        """Fills a given regular expression with & for a definitive and more easy processing

        For example, ab will be converted to a&b

        Parameters
        ----------
        inp : str
            The input regular expression to be filled

        Returns
        -------
        str
            filled regular expression
        """
        filled = ''
        char_array = [ch for ch in inp]
        it = iter(range(len(char_array) - 1))
        # list of operators, between which will not be filled
        operator_exemptions = ["&", "|", "*"]
        escaped = False
        for i in it:
            cur_char = char_array[i]
            filled += cur_char
            # finds escaped characters with \ or !
            if (cur_char == '\\' or cur_char == '!') and not escaped:
                escaped = True
                continue
            next_char = char_array[i + 1]

            # get escaped inverted character class (e.g. ![^abc]) and skip it
            if escaped and char_array[i - 1] == '!' and cur_char == '[':
                while next_char != ']' or (next_char == ']' and cur_char == '\\'):
                    filled += next_char
                    next(it)
                    i += 1
                    cur_char = char_array[i]
                    next_char = char_array[i + 1]

            # add a & if a normal character follows and is not a operator
            if escaped and next_char not in operator_exemptions:
                escaped = False
                # don't add & between character and closing brackets
                if next_char != ')' and next_char != ']':
                    filled += '&'
                continue
            # ignore escaped characters
            elif escaped:
                escaped = False
                continue
            
            # if current and next char are not operators, add &
            if cur_char not in operator_exemptions and next_char not in operator_exemptions:
                # don't add & between character and opening or closing brackets
                if cur_char == '(' or next_char == ')':
                    continue
                filled += '&'
                continue
            # but do add a & between * and character
            elif cur_char == '*' and next_char not in operator_exemptions:
                # don't add & between character and opening or closing brackets
                if cur_char == '(' or next_char == ')':
                    continue
                filled += '&'
                continue

        filled += char_array[-1]
        return filled

    @staticmethod
    def get_between(begin, end):
        """Gets all characters between begin and end

        For example, get_between('d', 'f') returns {d, e, f}

        Parameters
        ----------
        begin : str
            The starting character
        end : str
            The last character

        Returns
        -------
        set
            set of characters between 'begin' and 'end'
        """
        num_begin = ord(begin)
        num_end = ord(end)

        # end is larger than begin, cannot create such a range
        if num_begin > num_end:
            raise Exception("Illegal character class!")

        temp_set = set()

        for i in range(num_begin, num_end + 1):
            temp_set.add(chr(i))
        return temp_set

    @staticmethod
    def get_characters_by_command(command):
        """Generates a character set for a regex command

        Parameters
        ----------
        command : str
            the command to be converted

        Returns
        -------
        str
            character set for command
        """
        char_set = set()
        # not representable --> add as command
        if command in ['s', 'S', 'D', 'W']:
            char_set.add('!' + command)
        # get all numbers
        elif command == 'd':
            char_set = Regexer.get_between('0', '9')
        # get all numbers, letters and _
        elif command == 'w':
            char_set = Regexer.get_between('a', 'z')
            char_set = char_set.union(Regexer.get_between('A', 'Z'))
            char_set = char_set.union(Regexer.get_between('0', '9'))
            char_set.add('_')

        return char_set

    @staticmethod
    def generate_character_class(char_class):
        """Splits a character class into an or-string

        This can be something like [a-c] which will be converted to (a|b|c)

        Parameters
        ----------
        char_class : str
            The class of characters to be concatenated

        Returns
        -------
        str
            repeated qualifier
        """
        or_set = set()
        char_array = [ch for ch in char_class]
        it = iter(range(len(char_array)))
        # in the inversion case (e.g [^abc]), add special command for future comparison
        if char_array[0] == '^':
            return '![' + char_class + ']'
        for i in it:
            if (i + 1) < len(char_array):
                next_char = char_array[i + 1]
                # check for escaping
                if char_array[i] == '\\':
                    # generates characters for special commands
                    if next_char in ['d', 'D', 's', 'S', 'w', 'W']:
                        or_set = or_set.union(Regexer.get_characters_by_command(next_char))
                    # ignores \e i.e. our epsilon
                    elif next_char != 'e':
                        # escape special characters
                        if char_array[i] in ['.', '^', '$', '+', '?', '{', '}', '[', ']', '\\', '*', '|', '(', ')']:
                            or_set.add('\\' + next_char)
                        else:
                            or_set.add(next_char)
                    next(it)
                # detected a range and gets all characters between
                elif next_char == '-' and not (i + 2) == len(char_array):
                    or_set = or_set.union(Regexer.get_between(char_array[i], char_array[i + 2]))
                    next(it)
                    next(it)
                    i += 2
                else:
                    # replace space with \s
                    if char_array[i] == ' ':
                        or_set.add('!s')
                    else:
                        # escape special character
                        if char_array[i] in ['.', '^', '$', '+', '?', '{', '}', '[', ']', '\\', '*', '|', '(', ')']:
                            or_set.add('\\' + char_array[i])
                        else:
                            or_set.add(char_array[i])
            else:
                if not char_array[i] == ' ':
                    # escape special character
                    if char_array[i] in ['.', '^', '$', '+', '?', '{', '}', '[', ']', '\\', '*', '|', '(', ')']:
                        or_set.add('\\' + char_array[i])
                    else:
                        or_set.add(char_array[i])
                else:
                    # replace space with \s
                    or_set.add('!s')

        or_string = '('
        while len(or_set) > 0:
            or_string += or_set.pop()
            if len(or_set) > 0:
                or_string += '|'
        or_string += ')'

        return or_string

    @staticmethod
    def generate_repeated_qualifier(limits: str, previous_char):
        """Generates a repeated qualifier for 'previous_char'

        This can be something liek a{2,3} which will be converted to (aa|aaa)

        Parameters
        ----------
        limits : str
            The amount of repetion. Must be a singular number, a number followed by a comma or vice verca
            or two numbers seperated by a comma
        previous_char: str
            The string that will be repeated

        Returns
        -------
        str
            repeated qualifier
        """
        # singular number, repeat input n times
        if not limits.__contains__(','):
            repetitions = int(limits)
            tmp_string = ''
            for i in range(repetitions):
                tmp_string += previous_char

            return tmp_string
        else:
            # split on ,
            split = limits.split(',')
            lower = split[0]
            upper = split[1]
            infinite = False
            # catches {,n}
            if len(lower) == 0:
                lower = 0
            else:
                lower = int(lower)
            # catches {n,}
            if len(upper) != 0:
                upper = int(upper)
            else:
                infinite = True

            if not infinite and lower > upper:
                raise Exception("Lower bound is higher than upper bound!")

            tmp_string = '('
            # generate repetitions from lower to upper
            if not infinite:
                for i in range(upper - lower + 1):
                    if i == 0 and lower == 0:
                        tmp_string += r'\e'
                    for j in range(lower + i):
                        tmp_string += previous_char
                    if i < upper - lower:
                        tmp_string += '|'
            # generate lower repetions and add a repetition with a star
            else:
                repetitions = int(lower)
                for i in range(repetitions + 1):
                    tmp_string += previous_char
                tmp_string += '*'

            tmp_string += ')'
            return tmp_string

    @staticmethod
    def escape(inp: str):
        """Escapes all Python specific regex attributes.

        Converts character classes (e.g. [a-z]), commands (e.g. \\\\d), etc.

        Parameters
        ----------
        inp : str
            Unescaped regular expression, which will be escaped for further preprocessing

        Returns
        -------
        str
            escaped regular expression
        """
        # copy input, as we will trim and edit regex
        regex = inp
        escaped_string = ''
        # '*', '|', '(' and ')' are meta characters, but are not needed to processed in a special way
        meta_char = ['.', '^', '$', '+', '?', '{', '}', '[', ']', '\\']
        command_char = ['d', 'D', 's', 'S', 'w', 'W']
        escaped = False

        # keeps track of open bracket(s) and last added characters for potential repetition
        brackets = []
        bracket_tracker = ''
        last_bracket = ''
        open_bracket = False
        last_chars = ""
        no_guarantee = False

        # split input for iteration
        char_array = [ch for ch in regex]
        it = iter(range(len(char_array)))
        for i in it:
            char = char_array[i]
            # backslash indicates escape of next char
            if char == '\\':
                escaped = True
                continue
            # current char has been escaped by previous backslash
            elif escaped:
                # is a command
                if char in command_char:
                    # ! is our added special 'command' character for commands, that can not easily be represented
                    if char == 's':
                        escaped_string += '!s'
                        last_chars = '!s'
                    else:
                        translations = {
                            'd': '0-9',
                            's': r'\t\n\r\f\v',
                            'w': 'a-zA-Z0-9_',
                            'D': '^0-9',
                            'S': r'^\t\n\r\f\v',
                            'W': '^a-zA-Z0-9_'
                        }
                        # generate character class according to expansion of above dictionary
                        character_class = Regexer.generate_character_class(translations[char])
                        last_chars = character_class
                        escaped_string += character_class
                # check for special character (i.e. e which signifies an epsilon (added manually, not python-esque)
                else:
                    # ! is our added special 'command' character for commands, that can not easily be represented
                    if char in ['e']:
                        escaped_string += '!e'
                        last_chars = '!e'
                    # copy escape character, for possible \. or similar
                    else:
                        escaped_string += '\\'
                        escaped_string += char
                        last_chars = '\\' + char
                        if char in meta_char:
                            regex = regex.replace(char, '', 1)
                escaped = False
            # spaces cannot be handled by future NFA creation. We use or version of \s instead
            elif char == ' ':
                escaped_string += '!s'
                last_chars = '!s'
            # as we use ! as a special character, we need to escape occurences
            elif char == '!':
                escaped_string += '\\!'
                last_chars = '\\!'
            # any char, that is not special
            elif char not in meta_char:
                escaped_string += char
                last_chars = char
                if char == '(':
                    # if a bracket is open, store current bracket and begin a new one
                    if open_bracket:
                        brackets.append(bracket_tracker)
                    bracket_tracker = ''
                    open_bracket = True
                if char == ')':
                    # if a bracket closes and other open brackets exist, add bracket to last open bracket
                    if len(brackets) > 0:
                        tmp = bracket_tracker
                        bracket_tracker = brackets.pop() + tmp
                        last_bracket = tmp + ')'
                    # else close bracket and continue with execution
                    else:
                        bracket_tracker += ')'
                        last_bracket = bracket_tracker
                        last_chars = bracket_tracker
                        open_bracket = False
            # if an unescaped character class begins, split on ] and pass result to generation
            elif char == '[':
                x = regex.split(']', 1)
                regex = x[1]
                char_class = x[0].split('[')[1]
                character_class = Regexer.generate_character_class(char_class)
                last_chars = character_class
                escaped_string += character_class
                to_skip = len(char_class) + 1
                # skip all following chars of the character class
                for j in range(to_skip):
                    next(it)
            # if an unescaped repetion qualifier begins, split on } and generate repeated qualifier
            elif char == '{':
                x = regex.split('}', 1)
                regex = x[1]
                limits = x[0].split('{')[1]
                # remove previously added last_chars, as these will be readded by qualifier generation
                escaped_string = escaped_string[0:-len(last_chars)]
                # if there is an open bracket, remove last_chars from bracket_tracker as well
                if open_bracket:
                    bracket_tracker = bracket_tracker[0:-len(last_chars)]
                repetition = last_chars
                repeated_qualifier = Regexer.generate_repeated_qualifier(limits, repetition)
                last_chars = repeated_qualifier
                escaped_string += repeated_qualifier
                to_skip = len(limits) + 1
                # skip all following chars of the repeated qualifier
                for j in range(to_skip):
                    next(it)
            # convert s+ to ss* and watch for potential open or immediately closed brackets
            elif char == '+':
                if last_chars != "":
                    if last_chars[-1] == ')' or open_bracket:
                        if len(last_chars) == 1:
                            last_chars = last_bracket
                        bracket_tracker += last_chars + '*'
                    escaped_string += last_chars + '*'

                    last_chars = ""
                else:
                    escaped_string += char_array[i - 1] + '*'
            # escape . (match all) with our command !
            elif char == '.':
                escaped_string += '!.'
                last_chars = '!.'
            # convert a? to (epsilon | a)
            elif char == '?':
                if i < len(char_array) - 1:
                    # skip lookahead assertions, but set no_guarantee to True, as this is not an exact transformation
                    if char_array[i + 1] == '!' or char_array[i + 1] == '=' or char_array[i + 1] == ':':
                        # ignore if lookahead assertion is not correct e.g., a?=b is not correct, while a(?=b) is
                        if char_array[i-1] == '(':
                            next(it)
                            if not char_array[i + 1] == ':':
                                no_guarantee = True
                            continue
                # check if last char was a singular closing bracket
                if last_chars[-1] == ')' and len(last_chars) == 1:
                    last_chars = last_bracket
                    # shorten bracket_tracker as the last_chars will be added again
                    bracket_tracker = bracket_tracker[0:-len(last_chars)]
                # check if a bracket is still open
                elif open_bracket and not last_chars[-1] == ')':
                    bracket_tracker = bracket_tracker[0:-len(last_chars)]
                # last_chars is a completed bracket
                elif last_chars[-1] == ')':
                    bracket_tracker = bracket_tracker[0:-len(last_chars)]
                escaped_string = escaped_string[0:-len(last_chars)]
                # generate epsilon | a string
                epsilon_or = r'(!e|' + last_chars + ')'
                last_chars = epsilon_or
                escaped_string += epsilon_or
            # if ^ or $ exists, no guarantee can be given and use may be illegal
            elif char == '^':
                no_guarantee = True
                if not i == 0:
                    raise Exception("Illegal use of ^! Not at the beginning of the line.")
            elif char == '$':
                no_guarantee = True
                if not i == (len(char_array) - 1):
                    raise Exception("Illegal use of $! Not at the end of the line.")
            # update bracket_tracker, if a bracket is open
            if open_bracket:
                bracket_tracker += last_chars

        return escaped_string, no_guarantee

    @staticmethod
    def shunting_yard(regex, operators=None):
        """Converts a given regular expression into shunting yard form

        The given regular expression needs to be escaped and have filled operators (i.e. & or | between all
        characters). The shunting yard algorithm transforms a given expression from infix-notation to
        postfix-notation. For example, a|b becomes ab|. See also:
        https://gregorycernera.medium.com/converting-regular-expressions-to-postfix-notation-with-the-shunting-yard-algorithm-63d22ea1cf88
        https://en.wikipedia.org/wiki/Shunting_yard_algorithm

        Parameters
        ----------
        regex : str
            the regular expression to be transformed
        operators: list
            optional operator list

        Returns
        -------
        str
            transformed regular expression
        """
        if operators is None:
            operators = ['*', '&', '|']

        # output stack
        output = []
        # operator stack
        operator = []
        escaped = False
        command = False
        # tracks a current capture class
        capture_class = ''
        for char in regex:
            # check for non-escaped command symbols
            if char == '!' and not escaped:
                command = True
                capture_class = '!'
                output.append('!')
            elif command:
                # add command and potentially start capturing capture_class
                if len(capture_class) == 1:
                    if not char == '[':
                        output.append(char)
                        command = False
                        capture_class = ''
                        continue
                    output.append('[')
                    capture_class += char
                else:
                    # append finished capture class
                    if char == ']':
                        output.append(']')
                        command = False
                        capture_class = ''
                    # add to capture class
                    else:
                        output.append(char)
                        capture_class += char
            # add escaped char
            elif char == '\\' and not escaped:
                output.append(char)
                escaped = True
            # append simple char or command that has been escpaed
            elif (char not in operators and char != '(' and char != ')') or escaped:
                output.append(char)
                escaped = False
            # handle operators
            elif char in operators:
                # empty operator stack => add operator to stack
                if len(operator) == 0:
                    operator.append(char)
                    continue
                while len(operator) > 0:
                    # always add after opening bracket
                    if operator[-1] == '(':
                        operator.append(char)
                        break
                    # pop all operators while precedence of stack operators is lower or equal
                    elif operators.index(operator[-1]) <= operators.index(char):
                        temp = operator.pop()
                        output.append(temp)
                        if len(operator) == 0:
                            operator.append(char)
                            break
                    # else append operator to operator stack
                    else:
                        operator.append(char)
                        break
            # always add opening bracket to operator stack
            elif char == '(':
                operator.append(char)
            # pop all operators, until corresponding opening bracket is found
            elif char == ')':
                while 1:
                    top = operator.pop()
                    if top == '(':
                        break
                    else:
                        output.append(top)
        # remaining operator stack should be added in reverse order (i.e. order of appearance)
        operator.reverse()
        for op in operator:
            output.append(op)

        return ''.join(output)

    @staticmethod
    def preprocess(regex, steps=False):
        """Converts a given Python-style regex string into a formal-esque regular expression defintion.

        Parameters
        ----------
        regex : str
            The regular expression string to be processed.
        steps: bool
            Whether to print sub-step results

        Returns
        -------
        [str, bool]
            [normalized, no_guarantee] where 'normalized' is the converted regular expression
            and 'no_guarantee' indicates whether some assumptions had to be made
        """
        [escaped, no_guarantee] = Regexer.escape(regex)
        filled = Regexer.fill_operators(escaped)
        normalized = Regexer.shunting_yard(filled)

        if steps:
            print("Escaped string: ", escaped)
            print("Operator-filled string: ", filled)
            print("Shunting-yard string: ", normalized)

        return normalized, no_guarantee
