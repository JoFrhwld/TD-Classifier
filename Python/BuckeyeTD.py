import glob
import sys
from string import join


def hasDictCluster(line):
    ## has td
    if line[1][-1] in ["t","d"]:
        ## exclude preceding vowels
        if line[1][-2][0] not in ["a","e","i","o","u"]:
            return(True)
        ## but include preceding syllabic consonant
        elif line[1][-2][0] == "e" and line[1][-2][1] in ["r","l","m","n"]:
            return(True)
        else:
            return(False)
            
    else:
        return(False)

def getDictSyllables(line):
    pron = line[1]
    nsyl = 0
    for phon in pron:
        if len(phon) == 0:
            break
        elif phon[0] in ["a","e","i","o","u"]:
            nsyl = nsyl + 1
    return(nsyl)

def getSpokenSyllables(line):
    pron = line[2]
    nsyl = 0
    for phon in pron:
        if len(phon) == 0:
            break
        elif phon[0] in ["a","e","i","o","u"]:
            nsyl = nsyl + 1
    return(nsyl)    


def getWordRate(lines, index):
    nDict = getDictSyllables(lines[index])
    nSpoken = getSpokenSyllables(lines[index])
    nPre = 0
    nPost = 0
    for i in range(1,5):
        preline = lines[index-i]
        if preline[0][-1][0] in ["<","{"]:
            break
        else:
            
            nDict = nDict + getDictSyllables(preline)
            nSpoken = nSpoken + getSpokenSyllables(preline)
            nPre = nPre + 1
    for i in range(1,5):
        postline = lines[index+i]
        if postline[0][-1][0] in ["<","{"]:
            break
        else:
            nDict = nDict + getDictSyllables(postline)
            nSpoken = nSpoken + getSpokenSyllables(postline)
            nPost = nPost + 1

    windowBegin = float(lines[index-nPre][0][0])
    windowEnd = float(lines[index+(nPost+1)][0][0])
    windowDur = windowEnd - windowBegin
    rateDict = nDict / windowDur
    rateSpoken = nSpoken / windowDur

    return nDict, nSpoken, nPre, nPost, windowBegin, windowEnd, rateDict, rateSpoken
    
    


wordsFiles = glob.glob("/Users/joseffruehwald/Documents/Classes/Corpora/Buckeye/*/*/*words")

header = [
    "Speaker",
    "Recording",
    "Word",
    "WordBegin",
    "WordEnd",
    "POS",
    "seg",
    "SegTrans",
    "PreSegTrans",
    "FolSegTrans",
    "DictNSyl",
    "NSyl",
    "PreWindow",
    "PostWindow",
    "WindowBegin",
    "WindowEnd",
    "DictRate",
    "Rate",
    "FolWord",
    "Context"
    ]

sys.stdout.write(join(header, "\t") + "\n")

for fi in wordsFiles:

    speaker = fi.split("/")[-3]
    recording = fi.split("/")[-2]
    
    
    f = open(fi)
    lines = f.readlines()
    f.close()

    lines = [line.rstrip().lstrip() for line in lines]
    lines = [[item.lstrip().split(" ") for item in line.split(";")] for line in lines]

    bad = lines[8]
    read = False


    for index in range(len(lines)):
        if read:
            line = lines[index]
            if len(line) <= 1:
                break

            if hasDictCluster(line):
                dictSyl = getDictSyllables(line)
                spSyl = getSpokenSyllables(line)
                #sys.stderr.write(line[0][2] + "\n")

                nDict, nSpoken, nPre, nPost, windowBegin, windowEnd, rateDict, rateSpoken = getWordRate(lines, index)

                seg = line[1][-1]
                preseg = line[1][-2]
                folseg = lines[index+1][1][0]
                folword = lines[index+1][0][-1]

                segTrans = line[2][-1]

                context = lines[max(9, index-5):min(len(lines)-1,index+5)]
                contextWords = [w[0][-1] for w in context]
                contextWords = [w.replace("\n"," ") for w in contextWords]

                pos = line[-1][0]

                wordBegin = line[0][0]
                wordEnd = lines[index+1][0][0]
                
                out = [
                    speaker,
                    recording,
                    line[0][-1],
                    wordBegin,
                    wordEnd,
                    pos,
                    seg,
                    segTrans,
                    preseg,
                    folseg,
                    repr(nDict),
                    repr(nSpoken),
                    repr(nPre),
                    repr(nPost),
                    repr(windowBegin),
                    repr(windowEnd),
                    repr(rateDict),
                    repr(rateSpoken),
                    folword,
                    join(contextWords, " ")
                    ]
                sys.stdout.write(join(out, "\t")+"\n")

                
                
        elif lines[index][0][0] == "#":
            read = True
