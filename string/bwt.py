EOS = '\xff' 
# abracadabra$ --> 5a2b1c1d2r1$

"""
"""
class HeaderRange(object):
    def __init__(self, s):
        freq = {}
        for c in s:
            if c in freq:
                freq[c] += 1
            else:
                freq[c] = 1

        keys = sorted(freq.keys())

        result = {}
        cumulative = 0
        for c in keys:
            result[c] = (cumulative, cumulative+freq[c])
            cumulative += freq[c]

        self._hrange = result

        print 'hrange:', result


    def range(self, c):
        if c in self._hrange:
            return tuple(self._hrange[c])
        else:
            return None


def bwt(s):
    assert EOS == s[-1]

    suffix_details = []

    for i in range(len(s)):
        _next = s[i:]+s[:i]
        suffix_details.append((_next, i))

    suffix_details = sorted(suffix_details)

    bwt = []
    SA = []

    for p in suffix_details:
        bwt.append(p[0][-1])
        SA.append(p[1])

    return bwt, SA

"""
"""
def get_ranks(bwt):
    import copy
    r    = []
    rmap = {}
    for c in bwt:
        rmap[c] = 0
    for c in bwt:
        print 'rank:',c, rmap
        r.append(copy.deepcopy(rmap))
        rmap[c] += 1

    return r



class BWTSearcher(object):
    def __init__(self, _text):
        text = _text + EOS
        _bwt, SA = bwt(text)
        self._bwt = _bwt
        self._SA  = SA
        self._ranks = get_ranks(_bwt)
        self._hrange = HeaderRange(text)

    def _advance(self, _current_range, c):
        s_rank = self._ranks[_current_range[0]][c]
        e_rank = self._ranks[_current_range[1]][c]


        if s_rank >= e_rank:
            return None

        new_range = self._hrange.range(c)

        if new_range is None:
            return None

        print '\t... char:', c, 'rank:',s_rank, e_rank

        return (new_range[0] + s_rank, new_range[1] + e_rank)

    def search(self, query):
        query_position = len(query) - 1

        c = query[query_position]
        _range = self._hrange.range(c)

        if _range is None:
            return False

        query_position -= 1

        while True:
            print 'char:', c, 'range:', _range
            if query_position == -1:
                return True

            c = query[query_position]
            _range = self._advance(_range, c)

            if _range is None:
                return False

            query_position -= 1


#hrange = HeaderRange(s)
#print 'b\'s postion:', hrange.start('b'), hrange.end('b')

text = 'abracadabra'
searcher = BWTSearcher(text)
print searcher.search('dab')

def ibwt(s):

    table = [""]*len(s)

    for i in range(len(s)):
        t = []
        for j in range(len(s)):
            t.append(s[j] + table[j])
        table = sorted(t)

    for r in table:
        if r.endswith(EOS):
            return r[:-1]


"""
#assert ibwt(bwt("^banana")) == "^banana"
#assert ibwt(bwt("^banana")) == "^banana"

#print bwt('SIX.MIXED.PIXIES.SIFT.SIXTY.PIXIE.DUST.BOXES')
"""

#EOF

