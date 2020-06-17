import os

def scan(folder):
    list = []

    for root, dirs ,files in os.walk(folder):
        for x in dirs:
            list.append(x)

    return(list)