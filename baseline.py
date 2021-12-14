import math
import json
import string
import csv

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

def main():
    # Load JSON data and extract the JSON for the first N articles 
    source_file = open('./article-2020.json')
    source_json = json.load(source_file)
    raw_data = source_json

    commWords = getCommonWords()
    articleCtr = 0
    
    accuracies = []
    pAccuracies = []

    prevPunc = True

    # Iterate over JSON elements in raw_data
    for element in raw_data:
        title = element['title']
        title = title.lower()

        wordFreqs = {}
        prnFreqs = {}
        prnTags = []
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
            currPunc = False
            (word, currPunc) = clean(word)

            if word not in commWords and "'s" not in word:
                if word in wordFreqs:
                    wordFreqs[word] += 1
                else:
                    wordFreqs[word] = 1

                if word in title:
                        wordFreqs[word] *= 2

            if len(word) > 0:
                firstChar = word[0]
                if firstChar.isupper():
                    if not prevPunc:
                        word = word.lower()
                        if word in prnFreqs:
                            prnFreqs[word] += 1
                        else:
                            prnFreqs[word] = 1
                        
                        if word in title:
                           prnFreqs[word] *= 2
            
            prevPunc = currPunc
        # "sort" dictionary
        freqs = dict(sorted(wordFreqs.items(),key=lambda item: item[1],reverse=True))
        fCtr = 0
        for f in freqs: 
            if(fCtr < len(artTags)):
                if(len(f) > 0 and ' ' not in f):
                    ourTags.append(f.lower())
                    fCtr += 1

        pFreqs = dict(sorted(prnFreqs.items(),key=lambda item: item[1],reverse=True))
        pCtr = 0
        for f in pFreqs: 
            if(pCtr < len(artTags)):
                prnTags.append(f)
                pCtr += 1

        # Compare generated list to source list
        correct = 0
        pCorrect = 0
        for tag in artTags:
            if tag[0] == ' ':
                tag = tag[1:]
            if tag.lower() in ourTags:
                correct += 1
            if tag.lower() in prnTags:
                pCorrect += 1
        if len(artTags) > 0:
            accuracies.append(correct/len(artTags))
            pAccuracies.append(pCorrect/len(artTags))

        articleCtr += 1

    return (sum(accuracies)/len(accuracies))
    

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

if __name__ == "__main__":
    acc = main()
    print("Our Current Accuracy is " + str(acc))