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

print(compile("ab.cd.|"))
print(compile("aa.*"))