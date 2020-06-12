import numpy as np

d = np.load('test.npy')

print(d)

def differential (data):
    diff = []
    prev = data[1]
    for second in data[1:]:
        deriv = second - prev
        prev = second
        diff.append(deriv)
    return diff

diff = differential(d)
print(diff)