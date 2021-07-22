#!/usr/bin/python
import gkeepapi
import os
from collections import Counter
from config import SECRET_KEY, NOTESHOME
keep = gkeepapi.Keep()
success = keep.resume('mcnamaracommadavid@gmail.com', SECRET_KEY)
n = 1
titles = []
os.system("rm -rf " + NOTESHOME + "/*.gk")

def getTitle(t):
    nl = t.index("\n")
    while nl == 0:
        try:
            t = t[nl+1:]
            nl = t.index("\n")
        except ValueError:
            tt = t
            if tt in titles:
                tt = tt + " (" + str(Counter(titles)[tt]) + ")"
            titles.append(tt)
            return tt
            break
    tt = t[:nl]
    if tt in titles:
        tt = tt + " (" + str(Counter(titles)[tt]) + ")"
    titles.append(tt)
    return tt


for i in keep.all():
    content = str(i)
    filename = getTitle(content) + ".gk"
    if n < 10:
        nn = "0" + str(n)
    else:
        nn = str(n)
    finalfn = nn + "_"
    for char in filename:
        if char == "/":
            finalfn += "|"
        elif char == " ":
            finalfn += "_"
        else:
            finalfn += char
    finalfn = NOTESHOME + finalfn
    with open(finalfn, 'w+') as file:
        file.write(content)
    n = n + 1
