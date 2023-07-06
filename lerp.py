def lerp2_1d(a,b,t):
    return (b - a) * t + a

def lerp2(a,b,t):
    return ((b[0] - a[0]) * t + a[0], (b[1] - a[1]) * t + a[1])

def lerp3(a,b,c,t):
    return lerp2(lerp2(a,b,t),lerp2(b,c,t),t)

def lerp4(a, b, c, d, t):
    return lerp2(lerp3(a,b,c,t),lerp3(b,c,d,t),t)
