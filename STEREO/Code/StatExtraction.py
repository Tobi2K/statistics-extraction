import glob
import sys

import ThreadingRule as tr
import Utility as ut
import WrapperEvaluation as we
import loadPaper as pap


# method to extract statistics from the given directory from .json file into a .json file
def extractStatistic(fileName, targetName, fileExtension='.json'):
    if fileExtension not in fileName:
        fileName += fileExtension
    # read in the file
    sentences = []
    if fileExtension == '.json':
        sentences = pap.loadPaper(fileName)  # returns list of sentences
    elif fileExtension == '.tar.gz':
        sentences = pap.loadTarGz(fileName)  # returns list of sentences
    elif fileExtension == '.pdf':
        sentences = pap.loadPdf(fileName)  # returns list of sentences
    else:
        raise NotImplementedError("Unrecognized fileExtension!")
    # read rules
    rPlusList = pap.readRules("rPlus-original")
    # create if necessary json file
    if not ".json" in targetName:
        targetName += ".json"
    pap.createExtractionFile(targetName)
    # apply Rules
    for s in sentences:
        # rule is a tuple: (regex, index)
        match, index = ut.applyRPlus(rPlusList, s)
        while match is not None:
            # if a match is found -> save it in a .json file
            entity = ut.extractEntity(match, s, index)
            pap.updateExtracted(entity, targetName)
            s = s[0: match.start()] + " RPLUS MATCH " + s[match.end():len(s)]
            match, index = ut.applyRPlus(rPlusList, s)


# extracts statistics from the given directory
def extractStatisticDir(dirName, targetName, fileExtension='.json'):
    paths = glob.glob(dirName + "/*" + fileExtension)
    paths = list(map(lambda path: path.replace("\ ", "/"), paths))
    cur = 1
    max_paper = len(paths)
    for path in paths:
        if cur % 10 == 0:
            print('Progress:', cur, 'of', max_paper)
        cur += 1
        extractStatistic(path, targetName, fileExtension)


# sample for evaluation and start the evaluation
def startEvaluation(sampleSize, sType, sourceName, fileType='.json'):
    if sType == "rMinus":
        tr.collectMinusSentences(sampleSize, sourceName, fileType)
    else:
        we.callCollectSamples(sType, sourceName, sampleSize)
    we.evaluation(sType)


'''
possible input: 
    tool -ex|-a|-g -d? sfile tfile fileExtension
    tool -ev|-ae|-ge sampleSize type sfile
tool: statExtraction.py
'''


def main():
    isDirectory = False
    arguments = sys.argv
    try:
        if len(arguments) < 2:
            print("ErrorMessage: Missing arguments.")
            return
        if arguments[2] == "-d":
            isDirectory = True
        if arguments[1] == "-ex":
            if isDirectory:
                extractStatisticDir(arguments[3], arguments[4], arguments[5])
            else:
                extractStatistic(arguments[2], arguments[3], arguments[4])
        elif arguments[1] == "-ev":
            if arguments[3] == "rMinus":
                startEvaluation(int(arguments[2]), arguments[3], arguments[4], arguments[5])
            else:
                startEvaluation(int(arguments[2]), arguments[3], arguments[4])
        else:
            print("Invalid parameter.\n Use -s or ...")
            # maybe define other options for abae or gbce
            pass
    except Exception as se:
        print(sys.last_traceback)
        print(se)
        print("An error occurred. Probably the arguments were incorrect.\n Please use the following format:\n"
              "StatExtraction.py -s|-a|-g -d? source targetFile\n"
              "StatExtraction.py -se|-ae|-ge sampleSize type sfile\n"
              "Please look at the technical report for further information.")


main()
