# File Name: FeatureExractor.py
# --------------------------------------
# Developers: Himanshu Thakur
#             Krutarh Joshi
#             
# --------------------------------------
# This module extracts various numerical
# features from the essays which will be
# used further to train the system to 
# predict the score for the new essay.
# ---------------------------------------
import xlrd
import nltk
import enchant
import language_check

# Function Name: getEssays
# ---------------------------------------
# This function uses the xlrd package (
# package for reading excel files) to get
# the column of training essays from the 
# file thus storing them in a list and 
# returns the same.
# --------------------------------------- 
def getEssays():
 workbook = xlrd.open_workbook("training_set_rel3.xls","rU")
 essays = []
 sheet = workbook.sheet_by_name("training_set")
 entry = sheet.col_values(2, start_rowx = 1,end_rowx = 100)
 for i in range(len(entry)):
        tempString = ""
        tempString = entry[i].encode("ascii","ignore")
        essays.append(tempString)
 return essays
                    
    
# Function Name: sents
# ----------------------------------------
# The sents function uses the nltk package
# and tokenize each essay in to sentences 
# and returns sentence tokens.
# ----------------------------------------   
def sents():
    essays = getEssays()
    sentTokens = [None]*len(essays)
    for i in range(len(essays)):
        sentence = nltk.sent_tokenize(essays[i])
        sentTokens[i] = sentence
    return sentTokens

# Function Name: getSentLength
# ------------------------------------------
# This function computes number of sentences
# in each essay.
# ------------------------------------------
def getSentLength():
    sentences = sents()
    numSents = []
    for i in range(len(sentences)):
        numSents.append(len(sentences[i]))
    return numSents

# Function Name: makeTokens
# -------------------------------------------
# The makeTokens function takes each sentence
# of each essay as the argument and returns
# its word tokens.
# -------------------------------------------
def makeTokens(essay):
    tokens = nltk.word_tokenize(essay)
    return tokens

# Function Name: tokenizedEssays
# ---------------------------------------------
# This is a wrapper function for the makeTokens
# function and returns a list of word tokens
# for each essay.
# ---------------------------------------------
def tokenizedEssays():
    senTokenizedEssays = sents()
    tokenizedEssays = [None]*len(senTokenizedEssays)
    for i in range(len(senTokenizedEssays)):
        sentToken = senTokenizedEssays[i]
        listOfTokens = []
        for j in range(len(sentToken)):
            wordTokens = makeTokens(sentToken[j])
            for k in range(len(wordTokens)):
                listOfTokens.append(wordTokens[k])

        tokenizedEssays[i] = listOfTokens

    return tokenizedEssays

# Function Name: removePunct
# ---------------------------------------
# The function removes punctuations from
# the word tokens of each essay.
# ---------------------------------------
def removePunct():
    vocabWithPunct = tokenizedEssays()
    punctFreeVocab = [None]*len(vocabWithPunct)
    punctList = [".",",",":",";","/","?","[","]","{","}","!","@","#","$","%","^","*","(",")","+","-","'"]
    for i in range(len(vocabWithPunct)):
        punctFreeVocab[i] = [w for w in vocabWithPunct[i] if w.lower() not in punctList]

    return punctFreeVocab
# Function Name: removeStopWords
# ---------------------------------------
# This function rips apart the stop words
# from each essyas.
# ---------------------------------------
def removeStopWords(vocab):
    from nltk.corpus import stopwords
    stopWords = nltk.corpus.stopwords.words("english")
    stpWrdsFreeTokens  = [w for w in vocab if w.lower() not in stopWords]
    return stpWrdsFreeTokens

# Function Name: stopWordsFreeEssays
# ---------------------------------------
# Wrapper function for removeStopWords
# ---------------------------------------
def stopWordsFreeEssays():
    punctFreeVocab  = removePunct()
    validWords = [None]*len(punctFreeVocab)
    for i in range(len(punctFreeVocab)):
        validWords[i] = removeStopWords(punctFreeVocab[i])
    
    return validWords

# Function Name: getWordCount
# ---------------------------------------
# This function returns the number of 
# words per essay.
# ---------------------------------------
def getWordCount():
    totalWords = stopWordsFreeEssays()
    numWords = []
    for i in range(len(totalWords)):
        numWords.append(len(totalWords[i]))
    
    return numWords

# Function Name: vocabLength()
# ---------------------------------------
# This function makes the vocabulary for
# each essay and computes its length and
# returns it.
# ---------------------------------------
def vocabLength():
    allWords = stopWordsFreeEssays()
    vocab = []
    for i in range(len(allWords)):
        vocab.append(len(set(allWords[i])))

    return vocab

# Function Name: lexicalDiversity()
# --------------------------------------------
# This function computes the Lexical Diversity
# for each essay.
# ---------------------------------------------
def lexicalDiversity():
    totalLength = getWordCount()
    setLength = vocabLength()
    lexDiv = [None] * len(totalLength)
    for i in range(len(totalLength)):
        lexDiv[i] = float(setLength[i])/float(totalLength[i])
        
    return lexDiv
    
# Function Name: vocabError
# ---------------------------------------
# The vocabError funciton calculates the
# spelling mistakes and returns the count
# of same for each essay.
# ---------------------------------------
def vocabError():
    totalWords = stopWordsFreeEssays()
    enchantDict = enchant.Dict("en_US")
    misspelledWords = []
    for i in range(len(totalWords)):
        wrongWords = 0
        for j in range(len(totalWords[i])):
            if enchantDict.check(totalWords[i][j]) == False:
                wrongWords += 1

        misspelledWords.append(wrongWords)

    return misspelledWords
    
# Function Name: getAvrgWrdLength
# ---------------------------------------
# Returns average word length per essay.
# ---------------------------------------
def getAvgWrdLength():
    essayTokens = stopWordsFreeEssays()
    avgWordLength = []
    for i in range(len(essayTokens)):
        avg = 0.0
        totalWordLength = 0.0
        for j in range(len(essayTokens[i])):
            totalWordLength += len(essayTokens[i][j])

        avg = totalWordLength/len(essayTokens[i])
        avgWordLength.append((avg))
    
    return avgWordLength

def grammarCheck():
    sentences = sents()
    tool = language_check.LanguageTool("en-US")
    grammarErrors = [None] * len(sentences)
    for i in range(len(sentences)):
        for j in range(len(sentences[i])):
            match = tool.check(sentences[i][j])
        grammarErrors[i] = len(match)

    return grammarErrors
        
    

def postag():
    #print "postagging"
    tokens= tokenizedEssays()
    posTagged = [None]*len(tokens)
    for i in range(len(tokens)):
        posTagged[i] = nltk.pos_tag(tokens[i])

    return posTagged


# Function Name: getCounts
# ------------------------------------------
# Gets all the calculated numbers per essay
# for each extracted feature and returns the
# numbers for each feature per essay.
# 
# This function is basically used in other 
# module to get the counts at once to other 
# module with ease.
# -------------------------------------------
def getCounts():
    wrdCount = getWordCount()
    sents = getSentLength()
    avgWrdLength = getAvgWrdLength()
    misspelled = vocabError()
    lexDiv = lexicalDiversity()
    gramError = grammarCheck()

    posTaggedWords = postag()
    nounCount = []
    adjectiveCount = []
    adverbCount = []
    verbCount = []
    for i in range(len(posTaggedWords)):
        aC,nC,adC,vC = [0]*4
        for j in range(len(posTaggedWords[i])):
            if (posTaggedWords[i][j][1] in ["JJ","JJR","JJS"]):
                aC+=1
            elif (posTaggedWords[i][j][1] in ["NN","NNS","NNP","NNPS"]):
                nC+=1
            elif (posTaggedWords[i][j][1] in ["RB","RBR","RBS"]):
                adC+=1
            elif (posTaggedWords[i][j][1] in ["VB","VBD","VBG","VBN","VBP","VBZ"]):
                vC+=1
        adjectiveCount.append(aC)
        nounCount.append(nC)
        adverbCount.append(adC)
        verbCount.append(vC)

    return wrdCount,sents,avgWrdLength,misspelled,lexDiv,adjectiveCount,nounCount,adverbCount,verbCount,gramError


        
