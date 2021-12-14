import math
import json
import string
import csv

# Load JSON data and extract the JSON
source_file = open('articles2.json')
source_json = json.load(source_file)
raw_data = source_json

allFreqs = {}

# Remove punctuation and special characters from a word, and convert whole
# word to lowercase
def clean(word):
    word = word.rstrip()
    
    if "\xa0" in word:
        #print(word)
        word = word.replace("\xa0","")

    if "-\xa0" in word:
        #print(word)
        word = word.replace("-\xa0","")

    if '"' in word:
        word = word.replace('"','')

    hasPunc = False
    for char in word:
        if char in string.punctuation:
            if char == '.':
                hasPunc = True
            if char != '-':
                word = word.replace(char,'')
        if char == '\\':
            word = word.replace(char,'')

    return (word, hasPunc)

def getCommonWords():
    words = []
    with open('english-word-list-total.csv') as csvFile:
        reader = csv.reader(csvFile,delimiter=';')
        ctr = 0
        for line in reader:
            if ctr >= 4 and ctr <= 350:
                words.append(line[1])
            ctr += 1
    return words

#find frequencies of words across all corpus 
def buildFreqs():
    commWords = getCommonWords()

    #total # of non-common words in dataset (not unique)
    totalWs = 0

    for element in raw_data:

        article = element['article']
        words = article.split(sep=' ')

        for word in words:
            (nword, _) = clean(word)

            if nword not in commWords and "'s" not in nword:
                #print(word)
                totalWs += 1
                if nword in allFreqs:
                    allFreqs[nword] += 1
                else:
                    allFreqs[nword] = 1

    #convert to relative frequency
    for k in allFreqs:
        allFreqs[k] = allFreqs[k] / float(totalWs)

def main():
    buildFreqs()
    
    commWords = getCommonWords()
    articleCtr = 0
    
    accuracies = []
    octr = -1
    # Iterate over JSON elements in raw_data
    for element in raw_data:
        octr += 1
        title = element['title']
        title = title.lower()

        #total # of non-common words in article (not unique)
        aWords = 0

        wordFreqs = {}
        ourTags = []
        artTags = []
        # Convert article string to list of cleaned words
        article = element['article']
        if 'keywords' in element:
            if element['keywords']:
                artTags = element['keywords'].split(',')
        #Conver article tags to list, checking first if there are tags
        words = article.split(sep=' ')
        for word in words:
            #if previous word had punctuation
            (word, _) = clean(word)

            if word not in commWords and "'s" not in word:
                if word in wordFreqs:
                    wordFreqs[word] += 1
                else:
                    wordFreqs[word] = 1

            aWords += 1

        #% increase in frequency of word in article compared to frequency in corpus as a whole
        wInc = {}
        relFreqs = {}

        for k in wordFreqs:
            #convert to relative frequency
            relFreqs[k] = wordFreqs[k] / float(aWords)
            wInc[k] = relFreqs[k] / allFreqs[k]
            
        # "sort" wInc dictionary
        freqs = dict(sorted(wInc.items(),key=lambda item: item[1],reverse=True))
        fCtr = 0
        for f in freqs: 
            if(fCtr < len(artTags)):
                if(len(f) > 0 and ' ' not in f and not f.isnumeric() and wordFreqs[f] > 2):
                    ourTags.append(f.lower())
                    fCtr += 1

        if octr < 50:
            print(ourTags)

        # Compare generated list to source list
        correct = 0
        for tag in artTags:
            if tag[0] == ' ':
                tag = tag[1:]
            if tag.lower() in ourTags:
                correct += 1
            
        if len(artTags) > 0:
            accuracies.append(correct/len(artTags))

        articleCtr += 1

    return (sum(accuracies)/len(accuracies))

if __name__ == "__main__":
    acc = main()
    print("Our Current Accuracy is " + str(acc))