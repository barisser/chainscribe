import hashlib


def iterate_elements(elements):
    x = []
    for i in range(len(elements)/2):
        hasha = elements[i*2]
        if i * 2 + 1 < len(elements):
            hashb = elements[i*2+1]
        else:
            hashb = ""
        newhash = hashlib.sha256(hasha + hashb).hexdigest()
        x.append(newhash)
    return x


def tree(elements):
    elements = [hashlib.sha256(str(x)).hexdigest() for x in elements]
    while len(elements) > 1:
        elements = iterate_elements(elements)
    return elements[0]
