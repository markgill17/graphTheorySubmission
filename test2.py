def shunt(infix):
    # special characters for regular expressions and their precedence
    specials = {'*': 50, '.': 40, '+': 30, '-': 30, '|': 20}

    # this will be the output
    pofix = ""
    # the operater stack
    stack = ""

    # loop through the string, one character at a time
    for c in infix:
        # if there is an open bracket, push to the stack
        if c == '(':
            stack = stack + c
        # if there is a closing bracket, pop from the stack
        elif c == ')':
            while stack[-1] != '(':
                pofix = pofix + stack[-1]
                stack = stack[:-1]
            stack = stack[:-1]
        # if it's an operator, push to stack after popping lower or
        # equal precedence operators from the top of the stack into output
        elif c in specials:
            while stack and specials.get(c, 0) <= specials.get(stack[-1], 0):
                pofix, stack = pofix + stack[-1], stack[:-1]
            stack = stack + c
        else:
            pofix = pofix + c
    # pop all remaining operators from stack to output
    while stack:
        pofix, stack = pofix + stack[-1], stack[:-1]

    # return postfix
    return pofix

# this shows the states of the arrows
# None is used for E arrows
class state:
    label = None
    edge1 = None
    edge2 = None

# an NFA is represented by its initial and accept states
class nfa:
    initial = None
    accept = None

    def __init__(self, initial, accept):
        self.initial = initial
        self.accept = accept


def compile(pofix):
    nfastack = []

    for c in pofix:
        if c == '.':
            # pop the nfa's off the stack
            nfa2 = nfastack.pop()
            nfa1 = nfastack.pop()
            # commit first nfa's accept state to the second's initial
            nfa1.accept.edge1 = nfa2.initial
            # push nfa to the stack
            newnfa = nfa(nfa1.initial, nfa2.accept)
            nfastack.append(newnfa)
        elif c == '|':
            # pop 2 nfa's off the stack
            nfa2 = nfastack.pop()
            nfa1 = nfastack.pop()
            # create a new initial state, connect it to initial states of the 2 nfa's popped from the stack
            initial = state()
            initial.edge1 = nfa1.initial
            initial.edge2 = nfa2.initial
            # create a new accept state, connect it to accept states
            # of the 2 nfa's popped from the stack, to the new state
            accept = state()
            nfa1.accept.edge1 = accept
            nfa2.accept.edge2 = accept
            # push new nfa to the stack
            newnfa = nfa(initial, accept)
            nfastack.append(newnfa)

        elif c == '*':
            # pop a single nfa from the stack
            nfa1 = nfastack.pop()
            # create a new initial and accept state
            initial = state()
            accept = state()
            # join the new initial state to nfa1's initial state and the new accept state
            initial.edge1 = nfa1.initial
            initial.edge2 = accept
            # join the old accept state to the new accept state and nfa1's initial state
            nfa1.accept.edge1 = nfa1.initial
            nfa1.accept.edge2 = accept
            # push new nfa to the stack
            newnfa = nfa(initial, accept)
            nfastack.append(newnfa)

        else:
            # create new initial and accept states
            accept = state()
            initial = state()
            # join the initial state to the accept state using an arrow labelled c
            initial.label = c
            initial.edge1 = accept
            # push new nfa to the stack
            nfastack.append(nfa(initial, accept))

    # nfastack should only have a single nfa on it at this point
    return nfastack.pop()


def follows(state):
    """Return the set of states that can be reached from state following e arrows"""
    # create a new set, with state as its only member
    states = set()
    states.add(state)

    # check if state has arrows labelled e from it
    if state.label is None:
        # check if edge1 is a state
        if state.edge1 is not None:
            # if there's an edge1, follow it
            states |= follows(state.edge1)
        # check if edge1 is a state
        if state.edge2 is not None:
            # if there's an edge2, follow it
            states |= follows(state.edge2)

    return states


def match(infix, string):
    """Matches string to infix regular expression"""

    # Shunt and compie the regular expression
    postfix = shunt(infix)
    nfa = compile(postfix)

    # The current set of states and the next set set of states
    current = set()
    next = set()

    # add the initial state to the current state
    current |= follows(nfa.initial)

    # Loop through each character in the string
    for s in string:
        # loop through the current set of states
        for c in current:
            # check if that state is labelled s
            if c.label == s:
                # add the edge1 state to the next set
                next |= follows(c.edge1)
        # set current to next, and clear out next
        current = next
        next = set()

    # check if the accept state is in the set of current states
    return nfa.accept in current


# a few tests
infixes = ["a.b.c*", "a.(b|d).c*", "(a.(b|d))*", "a.(b.b)*.c*"]
strings = ["", "abc", "abbc", "abcc", "abad", "abbbc"]

# ZIP Method
for exp, string in zip(infixes, strings):
 print(match(exp, string), exp, string)
#print(list(zip(infixes,strings)))

#for i in infixes:
 #   for s in strings:
  #      print(match(i, s), i, s)
