#!/usr/bin/python3
from glob import glob
from datetime import datetime

files = list(set(glob("data/data/*.jpg")))
files.sort()

prevtime = None
assoc = {}

for i,f in enumerate(files):
    f = f.split("/")[-1]
    time = datetime(int(f[0:4]), int(f[4:6]), int(f[6:8]), int(f[9:11]), int(f[11:13]), int(f[13:15]))

    assoc[time] = f

timestamps = sorted(assoc.keys())


overlaps = []
for i,t in enumerate(timestamps):
    if i == 0:
        continue

    if (t-timestamps[i-1]).total_seconds() < 4:
        overlaps.append((timestamps[i-1], t))

print("Total images : %d" % len(files))
print("Overlaps : %d" % len(overlaps))
for o in overlaps:
    print("%s / %s" % (assoc[o[0]], assoc[o[1]]))