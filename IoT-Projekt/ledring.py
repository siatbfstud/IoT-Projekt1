def color(r, g, b):
    for i in range(12):
        np[i] = (r, g, b)
    np.write()


def clear():
    for i in range(12):
        np[i] = (0, 0, 0)
        np.write()