import random

USER_SIZE = 4
ITEM_SIZE = 10
PERM_SIZE = 100
CLICK_RATIO = 0.2

def jaccard_sim(s1, s2):
    numerator = len(s1.intersection(s2))
    denominator = len(s1.union(s2))

    if denominator == 0:
        return 0

    return numerator/float(denominator)

def prepare_user():
    user = []
    for i in range(USER_SIZE):
        items = []
        for j in range(ITEM_SIZE):
            r = random.random()
            if r < CLICK_RATIO:
                items.append(1)
            else:
                items.append(0)
        user.append(items)
    return user
"""
user = prepare_user()
"""
user = range(4)
user[0] = [1,1,0,0,0,1,1]
user[1] = [0,0,1,1,1,0,0]
user[2] = [1,0,0,0,0,1,1]
user[3] = [0,1,1,1,1,0,0]
#"""

def prepare_permutation():
    order = range(ITEM_SIZE)
    permutation = []
    for i in range(PERM_SIZE):
        random.shuffle(order)
        permutation.append(order[:]) # deep copy required!!
    return permutation
"""
permutation = prepare_permutation()
"""
permutation = range(3)
permutation[0] = [0,2,6,5,1,4,3]
permutation[1] = [3,1,0,2,5,6,4]
permutation[2] = [2,3,6,5,0,1,4]
#"""

def signature(p, u):
    rank = 0
    for i in p:
        if u[i] == 1:
            return rank
        rank += 1
    assert False, str(u)




def similarity_org(Ua, Ub):
    assert len(Ua) == len(Ub)

    Ua_sig = set()
    Ub_sig = set()

    for i in range(len(Ua)):
        if Ua[i] == 1:
            Ua_sig.add(i)

        if Ub[i] == 1:
            Ub_sig.add(i)

    return jaccard_sim(Ua_sig, Ub_sig)



def similarity_mh(Ua, Ub):
    global permutation

    Ua_sig = set()
    Ub_sig = set()

    for p in permutation:
        Ua_sig.add(signature(p, Ua))
        Ub_sig.add(signature(p, Ub))

    return jaccard_sim(Ua_sig, Ub_sig)


def hash(i, x):
    return ((i+1)*x+i) % ITEM_SIZE

def signature_hash(h, u):
    m = 999999999999
    for i in range(len(u)):
        if u[i] == 1:
            s = hash(h, i)
            if s < m:
                m = s
    return m


def similarity_mh_hash(Ua, Ub):
    intersection_cnt = 0
    for i in range(PERM_SIZE):
        if signature_hash(i, Ua) == signature_hash(i, Ub):
            intersection_cnt += 1
    return intersection_cnt/float(PERM_SIZE)

def compare(i, j):
    print i, j, ":", similarity_org(user[i], user[j]), similarity_mh(user[i], user[j]), similarity_mh_hash(user[i], user[j])

compare(0, 2)
compare(1, 3)
compare(0, 1)
compare(2, 3)
