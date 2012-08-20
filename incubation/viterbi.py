class Trac(object):
    def __init__(self, prob, v_path, v_prob):
        self.prob   = prob
        self.v_path = v_path # int[]
        self.v_prob = v_prob # double


"""
V(0, k) = P(y_0, k) * start_prob(k)
V(t, k) = P(y_t, k) * max_x_for_all_S(transition_prob(x, k) * V(t-1, x))


returns a viterbi path for given observations
"""
def forwardViterbi(observations, states, start_prob, transition_prob, emission_prob):
    T = [None] * len(states)

    for state in range(len(states)):
        T[state] = Trac(start_prob[state], [state], start_prob[state])
    
    for output in observations:
        U = [None] * len(states)
        for next_state in range(len(states)):
            next_trac = Trac(0, [], 0.0)

            for source_state in range(len(states)):
                p = emission_prob[source_state][output] * transition_prob[source_state][next_state]
                source_trac = T[source_state]

                next_trac.prob += source_trac.prob * p

                if source_trac.v_prob * p > next_trac.v_prob:
                    next_trac.v_path = source_trac.v_path[:]
                    next_trac.v_path.append(next_state)
                    next_trac.v_prob = source_trac.v_prob * p

            U[next_state] = next_trac
        T = U

    # apply sum/max to the final states:
    final_trac = Trac(0, [], 0.0)
    for state in range(len(states)):
        trac = T[state]

        final_trac.prob += trac.prob # FIXME

        if trac.v_prob > final_trac.v_prob:
            final_trac.v_path = trac.v_path
            final_trac.v_prob = trac.v_prob

    print "Probability of the whole system: ", final_trac.prob
    print ' --> '.join(map(lambda x: states[x], final_trac.v_path))
    print "Probability of the state:", final_trac.v_prob


def test():
    states = ["Rainy", "Sunny"]
    start_prob = [0.6, 0.4]
    observations = [0, 1, 2, 1, 2]
    transition_prob = [[0.7, 0.3], [0.4, 0.6]]
    emission_prob   = [[0.1, 0.4, 0.5], [0.6, 0.3, 0.1]]

    print "\nStates: "
    print states
    print "\nObservations: "
    print observations
    print "\nStart prob: "
    print start_prob
    print "\nTransition prob:"
    print transition_prob
    print "\nEmission prob:"
    print emission_prob

    forwardViterbi(observations, states, start_prob, transition_prob, emission_prob)

test()
