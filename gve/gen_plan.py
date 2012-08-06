OUTPUT_FILE = "plan.h"

"""
r0 = (mask0 & 0x80) ? 0 : SELECT(a, mask0 & 0x0f)
r1 = (mask1 & 0x80) ? 0 : SELECT(a, mask1 & 0x0f)
...
r15 = (mask15 & 0x80) ? 0 : SELECT(a, mask15 & 0x0f)
"""
def generate(f):

    strides = []

    f.write('const __m128i Masks [] = {\n')

    for i in range(256):
        vals = [0, 0, 0, 0, i]
        target_offset = 0
        stride = 0
        for j in range(4):
            span_in_bytes = (i >> (j*2)) & 3
            span_in_bytes += 1

            stride += span_in_bytes
            
            for k in range(span_in_bytes):
                vals[j] |= target_offset << (8*k)
                target_offset += 1

            for k in range(span_in_bytes, 4):
                vals[j] |= 0x80 << (8*k)
        strides.append(stride)

        f.write('    {{0x{1:08x}{0:08x}, 0x{3:08x}{2:08x}}}'.format(*vals))
        if i == 255:
            f.write('  //{4}\n'.format(*vals))
        else:
            f.write(', //{4}\n'.format(*vals))
    f.write('};\n')
    
    f.write('const int Strides [] = {\n')

    for i in range(256):
        f.write('    {0},\t//{1}\n'.format(*(strides[i], i,)))
    f.write('};\n')

fd = open('plan.h', 'w')
generate(fd )
