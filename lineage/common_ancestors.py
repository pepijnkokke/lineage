import json
import sys

def readJson(filename):
    """read list of tuples {url,name,child},
    return a dictionary {url : {name,child}}"""
    f = open(filename)
    ss = f.read().split('\n')
    dct = dict()
    for n in range (0,len(ss)):
        nthDict = json.loads(ss[n])
        urlField = nthDict['url']
        del nthDict['url']
        dct[urlField] = nthDict
    return dct

def commonAncestors(person1,person2):
    """compare two dictionaries of ancestors,
    return the names of common ancestors"""
    common = person1.keys() & person2.keys()
    return [ ancestor['name'][0] for ancestor 
              in [ person1[c] for c in common 
                   if person1[c]['child'] != person2[c]['child']
                 ]
           ]


if __name__=="__main__":

    if len(sys.argv) < 3:
        print("usage: python common_ancestors.py <person1.>jl <person2>.jl")
    else:
        person1 = readJson(sys.argv[1])
        person2 = readJson(sys.argv[2])

        print(commonAncestors(person1,person2))