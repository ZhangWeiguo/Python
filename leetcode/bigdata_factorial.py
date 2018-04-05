def multi(x,y):
    sx = list(str(x))
    sy = list(str(y))
    sx.reverse()
    sy.reverse()
    sz = [0]*(len(sx)+len(sy))
    k = 0
    for i in sx:
        k1 = k
        for j in sy:
            c = int(i)*int(j)
            if c >= 10:
                c1 = c/10
                c0 = c-c1*10
            else:
                c0 = c
                c1 = 0
            sz[k1] += c0
            sz[k1+1] += c1
            k1 += 1
        k += 1
    sz.reverse()
    z = ""
    begin = False
    for i in sz:
        if not begin:
            if i!= 0:
                begin = True
        if begin:
            z += str(i)
    return z

def fac(n):
    s0 = 1
    for i in range(2,n):
        print s0,i,multi(s0,i)
        s0 = multi(s0,i)
    return s0

print multi(6,4)
print fac(12)

