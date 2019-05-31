import nltk
import random
import re
import pronouncing
import math

NUMBER_OF_LINES = 6
SAMPLE_SIZE = 50

cmudictEntries = nltk.corpus.cmudict.entries()

LOVE_NOUNS = ["love", "passion"]
LOVE_ADJ = ["beautiful"]

def getLastWord(line):
    lastword = ""
    line = re.sub("[^\w\s]", "", line)
    for word in nltk.word_tokenize(line):
        lastword = word
    return lastword

def getLines():
    lines = []
    with open('trump_debate.txt', 'r', -1,"UTF-8") as fileinput:
        for line in fileinput:
            line = line.lower()
            line = re.sub("[.\\n]", "", line)
            lines.append(line)
    lines.pop(0)
    return lines


random_lines = random.sample(getLines(), SAMPLE_SIZE)

rhymeA = []
rhymeB = []
lines = []


index = 0



rhyming_lines = []
last_words = {}

random_lines = random.sample(getLines(), len(getLines()))

print(random_lines)
for line in random_lines:                      # for each random line
    last_words[line] = getLastWord(line)              # add the last word to the dictionary
for line1, word1 in last_words.items():
    for line2, word2 in last_words.items():
        if word2 != word1 and word2 in pronouncing.rhymes(word1):
            if(line2,line1) in rhyming_lines: continue
            rhyming_lines.append((line1,line2))

print("rhyming_lines:", rhyming_lines)


poem = rhyming_lines[0][0] + "\n" + random_lines[1][0] + "\n" + rhyming_lines[0][1] + "\n" + rhyming_lines[1][1]

print(poem)

for line in lines:
    print(line)
