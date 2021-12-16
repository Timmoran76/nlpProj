import math
import json
import string
import csv
import sys

df = {}
idf = {}

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
def main(source_file):
    # Load JSON data and extract the JSON
    source_json = json.load(source_file)
    raw_data = source_json

    artCount = 0
    commWords = getCommonWords()

    accuracies = []

    #total # of non-common words in dataset (not unique)
    totalWs = 0
    tf = {}
    for element in raw_data:
        
        docWords = []
        dwfs = {}
        docWs = 0
        
        article = element['article']
        words = article.split(sep=' ')

        for word in words:
            docWs += 1
            (nword, _) = clean(word)            

            if nword.lower() not in commWords and "'s" not in nword:
                if nword not in docWords:
                    docWords.append(nword)
                
                totalWs += 1
                if nword in dwfs:
                    dwfs[nword] += 1
                else:
                    dwfs[nword] = 1

        #build df dict which has # of unique appearances in articles
        for dw in docWords:
            if dw in df:
                df[dw] += 1
            else:
                df[dw] = 1

        #build tf dict that has document frequency
        for k in dwfs:
            tf[(k,artCount)] = dwfs[k] / float(docWs)

        artCount += 1
    #build idf dict
    for word in df:
        idf[word] = math.log(float(artCount) / (df[word] + 1))

    aCtr = 0
    prevPunc = True
    #score words based on our three dicts
    for elem in raw_data:
        ourTags = []
        artTags = []
        tf_idf = {}

        title = element['title']
        title = title.lower()

        article = elem['article']
        words = article.split(sep=' ')

        if 'keywords' in elem:
            if elem['keywords']:
                artTags = elem['keywords'].split(',')

        for word in words:
            (nword, currPunc) = clean(word)

            if nword.lower() not in commWords and "'s" not in nword:
                score = tf[(nword,aCtr)]*idf[nword]
                if len(nword) > 0:
                    firstChar = nword[0]
                    if firstChar.isupper():
                        #is proper noun
                        if not prevPunc:
                            if nword not in tf_idf:
                                tf_idf[nword] = score

            prevPunc = currPunc

        scores = dict(sorted(tf_idf.items(),key=lambda item: item[1],reverse=True))
        sCtr = 0
        noneCtr = 0
        for s in scores: 
            if(sCtr < len(artTags)):
                if(len(s) > 0 and ' ' not in s and not s.isnumeric()):
                    ourTags.append(s.lower())
                    sCtr += 1
            elif(len(artTags) == 0):
                if noneCtr < 5:
                    ourTags.append(s.lower())
                    noneCtr += 1

        if aCtr < 30:
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

        aCtr += 1

    if len(accuracies) > 0:
        return (sum(accuracies)/len(accuracies))
    else:
        return "No Accuracy Available"

if __name__ == "__main__":
    source_file = open('articles2.json')

    if len(sys.argv) > 1:
        source_file = open(sys.argv[1])

    acc = main(source_file)
    print("Our Current Accuracy is " + str(acc))