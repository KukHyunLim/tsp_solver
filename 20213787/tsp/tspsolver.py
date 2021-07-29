import click
import random
import math
import copy
import csv

@click.command()
@click.option('-t',     default=25, type=click.INT, required=True, help='start temperature default:25')
# @click.option('-p',     type=click.INT, required=True, help='population')
@click.option('-f',     default=100, type=click.INT, required=True, help='total number of fitness evaluations')
@click.option('-c',     default='linear', type=click.STRING, required=False, help='cooling type [linear, exponential, logarithmic]')
def main(t, f, c):
    print(F'Temp: {t} Fitness evaluations: {f} Cooling type: {c}')

    s = copy.deepcopy(getTSP('./a280.tsp'))
    T = t
    for k in range(f):
        s_new = copy.deepcopy(getRandomPath(s))
        if getNewS(s, s_new, T) >= random.random():
            s = copy.deepcopy(s_new)
        T = cool(t, f, c)
    
    f = open('write.csv','w', newline='')
    wr = csv.writer(f)
    for node in s:
      wr.writerow(node[0])
      print(node[0])
    f.close()

    return s


def cool(t, f, c):
    a = 0.1  # 기울기

    if c == 'exponential':
        return t * (a ** f)
    elif c == 'logarithmic':
        return t / math.log(f)
    else:
        return t - (a * f)


def getNewS(s, s_new, T):
    fitNew = fitness(s_new)
    fitOld = fitness(s)
    if fitNew > fitOld:
        print(fitNew)
        return 1.0
    else:
        return math.exp((fitNew - fitOld) / T)


def length(arr1, arr2):
    return math.sqrt((float(arr1[0]) - float(arr2[0]))**2 + (float(arr1[1]) - float(arr2[1]))**2)


def fitness(s):
    pathLength = 0
    for idx, node in enumerate(s):
        if len(s) == (idx+1):
            pathLength = pathLength + length(node[1:], s[0])
        else:
            pathLength = pathLength + length(node[1:], s[idx+1])
    return pathLength


def getRandomPath(s):
    cloneList = copy.deepcopy(s)
    random.shuffle(cloneList)
    return cloneList


def getTSP(file):
    infile = open(file, 'r')

    print(infile)

    Name = infile.readline().strip().split()[1]
    FileType = infile.readline().strip().split()[1]
    Comment = infile.readline().strip().split()[1]
    Dimension = infile.readline().strip().split()[1]
    EdgeWeightType = infile.readline().strip().split()[1]
    infile.readline()

    # Read node list
    nodelist = []
    while True:
        line = infile.readline().strip().split()
        if(line[0] == 'EOF'):
            break
        nodelist.append(line)
    infile.close()

    return nodelist


if __name__ == '__main__':
    main()
