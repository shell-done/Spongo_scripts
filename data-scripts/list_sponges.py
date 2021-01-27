with open("data.csv") as f:
    lines = [l.rstrip("\n") for l in f.readlines()]

    sponges = {}
    files = set([])
    for i,l in enumerate(lines):
        if i <= 0:
            continue

        params = l.split(";")

        specy = params[2]
        sponges[specy] = sponges.get(specy, 0) + 1
        files = files.union(set([params[8]]))

    for n,c in sponges.items():
        print("[%s] : %d" % (n, c))

    print("Images : %d" % len(files))

