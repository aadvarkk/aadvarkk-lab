#BOF

class SA(object):
    def __init__(self, txt):
        sa  = []

        for i in range(len(txt)):
            suffix = txt[i:]
            pos    = i
            sa.append((suffix, pos))
        sa.sort(lambda x, y: x[0] < y[0])

        self._txt   = txt
        self._sa    = sa

    def find_substr(self, ss):
        high = len(self._sa)
        low  = 0
        while low <= high:
            mid = (high + low)/2
            suffix = self._sa[mid][0]

            comparison = suffix[:len(ss)]

            if comparison > ss:
                high = mid - 1
            elif comparison < ss:
                low = mid + 1
            else:
                return self._sa[mid][1]

        return None



sa = SA('abcdesgssss')

print sa.find_substr('cdef')

#EOF
