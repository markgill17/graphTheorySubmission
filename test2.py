def shunt(infix):

    specials = {'*': 50, '.': 40, '|': 30}

    pofix = ""
    stack = ""

    for c in infix:
        if c == '(':
            stack = stack+c
        elif c == ')':
            while stack[-1] != '(':
                pofix = pofix + stack[-1]
                stack = stack[:-1]
            stack = stack[:-1]
        elif c in specials:
            while stack and specials.get(c, 0) <= specials.get(stack[-1], 0):
                pofix, stack = pofix + stack[-1], stack[:-1]
            stack = stack + c
        else:
            pofix = pofix + c

    while stack:
        pofix, stack = pofix + stack[-1], stack[:-1]

    return pofix

class state:
    label = None
    edge1 = None
    edge2 = None

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
            # push new nfa to the stack
            nfastack.append(nfa(initial, accept))

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
    set.add(state)

    # check if state has arrows labelled e from it
    if state.label is None:


def match(infix, string):
    """Matches string to infix regular expression"""

    # Shunt and compie the regular expression
    postfix = shunt(infix)
    nfa = compile(postfix)

    # The current set of states and the next set set of states
    current = set()
    next = set()

    # Loop through each character in the string
    for s in string:

# a few tests
infixes = ["a.b.c*", "a.(b|d).c*", "(a.(b|d))*", "a.(b.b)*.c"]
strings = ["", "abc", "abbc", "abad", "abbbc"]

for i in infixes:
    for s in strings:
        print(match(i, s), i, s)
